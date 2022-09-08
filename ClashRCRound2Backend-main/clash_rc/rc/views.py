from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from clash.decorators import timer
from sandbox import views
import re

signals = {
    1: "RE",
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


@login_required
@timer
def home(request):
    try:
        nw = RcPlayer(junior=True, user=request.user)
        nw.save()
    except:
        pass
    return render(request, "Rc-Home.html")


@login_required
@timer
def leaderboard(request):
    if request.user.is_authenticated:
        data = []
        for user in RcPlayer.objects.order_by("-total_score"):
            data.append(user)
        return render(request, "Rc-leaderboard.html", {"data": data})


@login_required
@timer
def contest(request):
    tester = RcPlayer.objects.get(user=request.user)
    ques = RcQuestion.objects.filter(Q(junior=tester.junior) | Q(junior=None))
    l_status = []
    for que in ques:
        status = RcSubmission.objects.filter(q_id=que, p_id=tester)
        if len(status) > 1:
            status = status.order_by("-score")
            status = status[0].status
            l_status.append(status)
        else:
            status = "Not Attempted"
            l_status.append(status)
    mylist = zip(ques, l_status)
    return render(request, "Rc-contest.html", {"mylist": mylist})


@login_required
@timer
def question(request, pk):
    ques = RcQuestion.objects.get(pk=pk)
    return render(request, "Rc-question.html", {"ques": ques})


@login_required
@timer
def mysubmission(request, pk):
    l1 = []
    for i in RcSubmission.objects.all().filter(
        p_id=RcPlayer.objects.get(user=request.user), q_id=pk
    ):
        l1.append(i)
    return render(request, "Rc-mysub.html", {"data": l1})


def get_upload_path(instance):
    return "User_Data/{0}".format(instance)


@login_required
@timer
def RC(request, pk):
    que = RcQuestion.objects.get(pk=pk)
    tester = RcPlayer.objects.get(user=request.user)
    if request.method == "POST":
        if que.junior == tester.junior or que.junior == None:
            intake = request.POST["Rc_input"]
            result = ""
            s = "User_Data/{0}/Rc_input.txt".format(tester.user.username)
            with open(s, "w+") as inp:
                inp.write(intake)
            with open(s, "r") as inp:
                views.get_code(que.code, request.user.username, que.language)
                views.execute(request.user.username, inp, que.language)
                f2 = open(
                    "sandbox/submissions/{}/result.txt".format(tester.user.username),
                    "r",
                )
                result = f2.read()
                f2.close()
            return render(
                request,
                "Rc-question.html",
                {"ques": que, "input": intake, "output": result},
            )
        else:
            return redirect("rc-contest")
    else:
        return render(request, "Rc-question.html", {"ques": que})


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
def rc_sub(request, pk):
    que = RcQuestion.objects.get(pk=pk)
    tester = RcPlayer.objects.get(user=request.user)
    tc_count = 0
    correct_tcs = 0
    code = ""
    language = request.POST.get("language")
    s = ""
    if request.method == "POST":
        if que.junior == tester.junior or que.junior == None:
            code = request.POST["input"]
            views.get_code(code, request.user.username, language)
            cases = []
            check = True
            display_error = ""
            for tc in Rctestcase.objects.filter(q_id=pk):
                tc_count += 1
                error_code = views.execute(request.user.username, tc.tc_input, language)
                print(error_code)
                if error_code == 0:
                    stat = views.compare(request.user.username, tc.tc_output)
                    if stat:
                        cases.append("Passed")
                        correct_tcs += 1
                    else:
                        cases.append("Failed")
                else:
                    cases.append(signals[error_code])
                    if check:
                        display_error = signals[error_code]
                        check = False
            scr = int((100 * correct_tcs) / tc_count)
            views.update_score(scr, pk, tester)
            if correct_tcs == tc_count:
                intake = RcSubmission(
                    q_id=que,
                    p_id=tester,
                    score=scr,
                    code=code,
                    status="AC",
                    language=language,
                )
                que.correct_submissions += 1
            elif error_code == 0:
                intake = RcSubmission(
                    q_id=que,
                    p_id=tester,
                    score=scr,
                    code=code,
                    status="WA",
                    language=language,
                )
            else:
                intake = RcSubmission(
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
            f2 = open("sandbox/submissions/{}/error.txt".format(tester.user.username), "r")
            errors = f2.read()
            errors = san_saf_error(errors, language)
            f2.close()

            if correct_tcs == tc_count:
                return render(
                    request,
                    "Rc-submission.html",
                    {"result": "All Correct", "testcase": cases},
                )
            return render(
                request,
                "Rc-submission.html",
                {"result": "Incorrect", "testcase": cases, "error": errors},
            )
        return redirect("rc-contest")

    return render(request, "Rc-question.html", {"ques": que})
