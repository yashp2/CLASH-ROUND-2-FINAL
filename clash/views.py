import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from clash.decorators import timer
from sandbox import views
from django.db.models import Q
from datetime import datetime
import re


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
    if request.user.is_authenticated:
        data = []
        for user in Player.objects.order_by("-total_score"):
            data.append(user)
        return render(request, "leaderboard.html", {"data": data})


@login_required
@timer
def contest(request):
    tester = Player.objects.get(user=request.user)
    ques = Question.objects.filter(Q(junior=tester.junior) | Q(junior=None))
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
    print("hello")
    return render(request, "trial1.html", {"mylist": mylist})


@login_required
@timer
def question(request, pk):
    ques = Question.objects.get(pk=pk)
    return render(request, "question.html", {"ques": ques})


@login_required
@timer
def mysubmission(request, pk):
    l1 = []
    for i in Submission.objects.all().filter(
        p_id=Player.objects.get(user=request.user), q_id=pk
    ):
        l1.append(i)
    return render(request, "mysub.html", {"data": l1})


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
    if request.method == "POST":
        custom=False
        for key in request.POST:
            if(key=="cust"):
                custom=True
        if(custom):
            code = request.POST["input"]
            intake = request.POST["custom_input"]
            s = "User_Data/{0}/cust_input.txt".format(tester.user.username)
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
                "sandbox/submissions/{}/error.txt".format(tester.user.username), "r"
            )
            errors = f2.read()
            errors = san_saf_error(errors, language)
            f2.close()
            return render(
                request,
                "question.html",
                {
                    "ques": que,
                    "code": code,
                    "input": intake,
                    "output": result,
                    "error": errors,
                },
            )
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
            if correct_tcs == tc_count:
                return render(
                    request,
                    "submission.html",
                    {"result": "All Correct", "testcase": cases},
                )
            else:
                return render(
                    request,
                    "submission.html",
                    {"result": "Incorrect", "testcase": cases, "error": errors},
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
            
            return render(request, "waiting.html")

        return render(request, "login.html", {"error": "invalid username"})

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    data = []
    count = 0
    for user in Player.objects.order_by("-total_score"):
        if count < 3:
            data.append(user)
            count += 1
        else:
            break
    return render(request, "result.html", {"leaders": data})
