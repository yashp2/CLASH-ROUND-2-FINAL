import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from clash.decorators import timer
# from sandbox import views
from django.db.models import Q
from datetime import datetime
import re
from django.http import JsonResponse
from django.core.paginator import Paginator


signals = {
    1: "CTE",
    2: "CTE",
    127: "CTE",
    132: "RE",
    133: "RE",
    134: "RE",
    136: "RE",
    137: "TLE",
    138: "MLE",
    139: "RE",
    158: "TLE",
    152: "TLE",
    159: "MLE",
    153: "MLE",
}


def handler404(request,*args):
    return redirect('clash-home')
def handler403(request,*args):
    return render(request,"rick.html")

@login_required
@timer
def home(request):
    return render(request, "home.html")


@login_required
@timer
def leaderboard(request):
    tester = Player.objects.get(user=request.user)
    obj = SetTime.objects.get(pk=1)
    time = obj.final_time #final time format 2022-02-08 18:30:19+05
    newtime = str(time)
    if request.user.is_authenticated:
        data = []
        rank=0
        counter=0
        for user in Player.objects.order_by("-total_score"):
            data.append(user)
            rank+=1
            if(user==tester):
                counter=rank
        mydata=data
        p=Paginator(mydata,3)
        page_num=request.GET.get('page',1)
        
        try:
            page=p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        return render(request, "leaderboard.html", {"data": data,"rank":counter,"name":tester.user.username,"score":tester.total_score,"items":page, "num":p,"time":newtime})


# @login_required
# @timer
# def leaderboardf(request):
#     if request.user.is_authenticated:
#         data = []
#         for user in Player.objects.order_by("-total_score"):
#             data.append(user)
#         return JsonResponse({"data1":data})

@login_required
@timer
def buffer(request,pk):
    print("buff")
    l1 = []
    lang=""
    for i in Submission.objects.all().filter(p_id=Player.objects.get(user=request.user), q_id=pk):
        l1.append(i)
        break
    if(len(l1)==0):
        s=""
    else:
        s=l1[0].code
        lang=l1[0].language
    return JsonResponse({'key':s,'lang':lang},status=200)

@login_required
@timer
def contest(request):
    tester = Player.objects.get(user=request.user)
    ques = Question.objects.filter(Q(junior=tester.junior) | Q(junior=None))
    obj = SetTime.objects.get(pk=1)
    # time = obj.final_time #final time format 2022-02-08 18:30:19+05
    time = obj.final_time.astimezone() 
    newtime = str(time)
    l_status = []
    for que in ques:
        status = Submission.objects.filter(q_id=que, p_id=tester)
        if len(status) > 0:
            status = status.order_by("-score")
            status = status[0].status
            l_status.append(status)
        else:
            status = "Not Attempted"
            l_status.append(status)
    mylist = zip(ques, l_status)
    # print("hello")
    return render(request, "trial1.html", {"mylist": mylist, "time":newtime})


@login_required
@timer
def question(request, pk):
    ques = Question.objects.get(pk=pk)
    tester = Player.objects.get(user=request.user)
    obj = SetTime.objects.get(pk=1)
    time = obj.final_time #final time format 2022-02-08 18:30:19+05
    newtime = str(time)
    return render(request, "question.html", {"ques": ques,"score":tester.total_score,"time":newtime})


@login_required
@timer
def mysubmission(request, pk):
    l1 = []
    ac=0
    wa=0
    tle=0
    rte=0
    cte=0
    mle=0
    obj = SetTime.objects.get(pk=1)
    time = obj.final_time #final time format 2022-02-08 18:30:19+05
    newtime = str(time)
    for i in Submission.objects.all().filter(
        p_id=Player.objects.get(user=request.user), q_id=pk
    ):
        l1.append(i)
        if(i.status=="RE"):
            rte+=1
        elif(i.status=="AC"):
            ac+=1
        elif(i.status=="WA"):
            wa+=1
        elif(i.status=="TLE"):
            tle+=1
        elif(i.status=="CTE"):
            cte+=1
        else:
            mle+=1
    return render(request, "mysub.html", {"data": l1,"ac":ac,"rte":rte,"wa":wa,"tle":tle,"cte":cte,"mle":mle,"pk":pk,"time":newtime})


def get_upload_path(instance):
    return "User_Data/{0}".format(instance)


def san_saf_error(error,language):

    if language == "py":
        try:
            pattern = re.sub(r'(["])([a-zA-Z0-9_.+-;,]+)(["])','"prog.py"',error)
            find = re.compile(r'line [\d]+')
            num = str(int(((find.findall(pattern))[0].split())[1]) - 39)
            error = re.sub(find,"line "+num, pattern)
        except:
            pass
    elif language=="cpp":
        try:
            error = re.sub(r'U([a-zA-Z0-9_.+-;,]+)([:])','prog.cpp:',error)
        except:
            pass
    else:
        try:
            error = re.sub(r'U([a-zA-Z0-9_.+-;,]+)([:])','prog.c:',error)
        except:
            pass

    return error


@login_required
@timer
def clash_sub(request, pk):
    print(request.POST)
    que = Question.objects.get(pk=pk)
    tester = Player.objects.get(user=request.user)
    tc_count = 0
    correct_tcs = 0
    code = ""
    language = request.POST.get("language")
    s = ""
    obj = SetTime.objects.get(pk=1)
    time = obj.final_time #final time format 2022-02-08 18:30:19+05
    newtime = str(time)
    if request.method == "POST":
        custom=True
        for key in request.POST:
            print(key)
            if(key=="normal"):
                custom=False
        if(custom):
            code = request.POST["input"]
            intake = request.POST["custom_input"]
            print("cust_C")
            s = "User_Data/{0}/cust_input.txt".format(tester.user.username)
            error_code=0
            with open(s, "w+") as inp:
                inp.write(intake)
            with open(s, "r") as inp:
                views.get_code(code, request.user.username, language)
                error_code = views.execute(request.user.username, inp, language)
                # print(f"error code: {error_code}")
                f2 = open(
                    "sandbox/submissions/{}/result.txt".format(tester.user.username),
                    "r",
                )
                result = f2.read()
                f2.close()
                f2 = open(
                "sandbox/submissions/{}/error.txt".format(tester.user.username), "r")
            errors = f2.read()
            errors = san_saf_error(errors, language)
            if(error_code!=0):
                result=errors
            f2.close()
            return JsonResponse({"opt" : result},status=200)
        elif que.junior == tester.junior or que.junior == None:
            code = request.POST["input"]
            views.get_code(code, request.user.username, language)
            cases = []
            check = True
            display_error = ""
            for tc in testcase.objects.filter(q_id=pk):
                tc_count += 1
                error_code = views.execute(request.user.username, tc.tc_input, language)
                if error_code == 0:
                    stat = views.compare(request.user.username, tc.tc_output)
                    if stat:
                        cases.append("Passed")
                        correct_tcs += 1
                    else:
                        cases.append("Failed")
                else:
                    try:
                        if(error_code<0):
                            error_code=128-error_code
                        cases.append(signals[error_code])
                    except:
                        cases.append("Unknown Error")
                    if check:
                        display_error = cases[-1]
                        check = False
            scr = int((100 * correct_tcs) / tc_count)
            views.update_score(scr, pk, tester)
            if correct_tcs == tc_count:
                intake = Submission(
                    q_id=que,
                    p_id=tester,
                    score=scr,
                    code=code,
                    status="AC",
                    language=language,
                )
                que.correct_submissions += 1
            elif error_code == 0:
                intake = Submission(
                    q_id=que,
                    p_id=tester,
                    score=scr,
                    code=code,
                    status="WA",
                    language=language,
                )
            else:
                intake = Submission(
                    q_id=que,
                    p_id=tester,
                    score=scr,
                    code=code,
                    status=display_error,
                    language=language,
                )
            intake.save()
            que.total_submissions += 1
            dec = (que.correct_submissions / que.total_submissions) * 100
            que.accuracy = round(dec, 2)
            que.save()
            f2 = open(
                "sandbox/submissions/{}/error.txt".format(tester.user.username), "r"
            )
            errors = f2.read()
            errors = san_saf_error(errors, language)
            f2.close()
            if(display_error==""):
                display_error="Wrong Anwer"
            if correct_tcs == tc_count:
                return render(
                    request,
                    "base.html",
                    {"result": "All Correct", "testcase": cases,'score':scr,'pk':pk,"time":newtime}
                )
            else:
                return render(
                    request,
                    "base.html",
                    {"result": display_error, "testcase": cases, "error": errors,'score':scr,'pk':pk,"time":newtime}
                )
        else:
            return redirect("clash-contest")
    else:
        return render(request, "question.html", {"ques": que})


def login_page(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                nw = Player(junior=True, user=user)
                nw.save()
            except:
                pass
            login(request, user)
            path = get_upload_path(username)
            try:
                os.mkdir(path)
            except:
                pass
            try:
                os.mkdir('sandbox/submissions/{0}'.format(username))
            except:
                pass
            
            obj = SetTime.objects.get(pk=1)
            a = obj.start_time.astimezone()  # to get current timezone time.
            # final time should be constant
            start_time = datetime(
                year=a.year,
                month=a.month,
                day=a.day,
                hour=a.hour,
                minute=a.minute,
                second=a.second,
            )  # final time
            # seconds from epoch.
            start_time_timestamp = int(start_time.timestamp())
            date_now = datetime.today()
            date_now_timestamp = int(date_now.timestamp())
            if date_now_timestamp >= start_time_timestamp:
                return redirect("clash-home")
            obj = SetTime.objects.get(pk=1)
            time = obj.start_time.astimezone() 
            # time = obj.start_time #start time format 2022-02-08 18:30:19+05
            newtime = str(time)
            return render(request, "waiting.html",{"time":newtime})

        return render(request, "login.html", {"error": "invalid username"})

    return render(request, "login.html")


# @login_required
# def logout_view(request):
#     tester = Player.objects.get(user=request.user)
#     data = []
#     count = 0
#     rank=0
#     for user in Player.objects.order_by("-total_score"):
#         count += 1
#         if count < 6:
#             data.append(user)
#         if(tester==user):
#             rank=count
#         if(rank>0 and count>5):
#             break
#     logout(request)
#     return render(request, "result.html", {"leaders": data,"rank":rank,"score":tester.total_score})

@login_required
def logout_view(request):
    tester = Player.objects.get(user=request.user)
    data = []
    count = 0
    rank=0
    for user in Player.objects.order_by("-total_score"):
        count += 1
        if count < 7:
            data.append(user)
        if(tester==user):
            rank=count
        if(rank>0 and count>5):
            break
    logout(request)
    first=data.pop(0)
    second=data.pop(0)
    third=data.pop(0)
    return render(request, "result.html", {"first":first,"second":second,"third":third,"leaders": data,"rank":rank,"tester":tester})
