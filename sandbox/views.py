import subprocess
from clash.models import *
import resource
import os
import re


def set_limit_resource(language):
    time_limit = 1
    memory_limit = 104000000

    def setlimits():
        resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit))
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

    return setlimits


def comment_remover(code):
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "  # note: a space and not an empty string
        return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    code = re.sub(pattern, replacer, code)
    return code


def add_header(code):
    path = os.getcwd() + "/sandbox/filter/"
    try:
        if code.find(" main(")+1:
            lst = code.split(" main(")
            part1 = lst[0] + " main("
        else:
            lst = code.split(" main ")
            part1 = lst[0] + " main"
        part2 = lst[1]
        pt = part2.find("{") + 1
        code = (
            f'#include "{path}filter.h"\n'
            + part1
            + part2[0:pt]
            + "\nput_filter();\n"
            + part2[pt:]
        )

        return code
    except:
        pass


def get_code(code, name, language):
    try:
        if language == "py":
            s = "User_Data/{0}/codePy.py".format(name)
            f1 = open("sandbox/filter/filter.py", "r")
            f2 = f1.read() + code

        elif language == "cpp":
            s = "User_Data/{0}/codeCPP.cpp".format(name)
            code = comment_remover(code)
            f2 = add_header(code)

        elif language == "c":
            s = "User_Data/{0}/codeC.c".format(name)
            code = comment_remover(code)
            f2 = add_header(code)

        with open(s, "w+") as f:
            f.write(f2)
    except:
        pass


def execute(name, test_input, language):
    f1 = open("sandbox/submissions/{}/result.txt".format(name), "w+")
    f2 = open("sandbox/submissions/{}/error.txt".format(name), "w+")

    if language == "py":
        s = "User_Data/{0}/codePy.py".format(name)
        s = "python3 " + s + " -lseccomp"
        a = subprocess.run(
            s,
            shell=True,
            preexec_fn=set_limit_resource(language),
            stdin=test_input,
            stdout=f1,
            stderr=f2,
            text=True,
        )

        return a.returncode

    elif language == "cpp":
        s = "User_Data/{0}/codeCPP.cpp".format(name)
        fp = r"User_Data/{0}/".format(name)
        s = r"g++ " + s + (" -o {0}a".format(fp)) + " -lseccomp"
        a = subprocess.Popen(s, shell=True, stderr=f2)
        a.wait()

        if a.returncode == 0:
            fp = r"User_Data/{0}/".format(name)
            exe = r"./{0}a".format(fp)
            a = subprocess.Popen(
                exe,
                shell=True,
                preexec_fn=set_limit_resource(language),
                stdin=test_input,
                stdout=f1,
                stderr=f2,
                text=True,
            )
            a.wait()

        else:
            f1.write("")

        return a.returncode

    elif language == "c":
        s = "User_Data/{0}/codeC.c".format(name)
        fp = r"User_Data/{0}/".format(name)
        s = r"gcc " + s + (" -o {0}c").format(fp) + " -lseccomp"
        a = subprocess.Popen(s, shell=True, stderr=f2)
        a.wait()

        if a.returncode == 0:
            fp = r"User_Data/{0}/".format(name)
            exe = r"./{0}c".format(fp)
            a = subprocess.Popen(
                exe, shell=True, stdin=test_input, stdout=f1, stderr=f2, text=True
            )
            a.wait()

        else:
            f1.write("")
        return a.returncode
    f1.close()
    f2.close()


def compare(name, test_output):
    with open("sandbox/submissions/{}/result.txt".format(name)) as file_1:
        file_1_text = file_1.readlines()
    with open(str(test_output)) as file_2:
        file_2_text = file_2.readlines()
    index = 0
    result = True
    if len(file_2_text) > len(file_1_text):
        result = False
    else:
        for line in file_2_text:
            line1 = file_1_text.pop(0)
            line = line.rstrip()
            line1 = line1.rstrip()
            if len(line) != len(line1):
                result = False
            else:
                for index in range(len(line)):
                    if line[index] != line1[index]:
                        result = False
        for line in file_1_text:
            line = line.split()
            if len(line) > 0:
                result = False
    return result


def update_score(scr, pk, tester):
    if pk == 1 and scr > tester.ques1:
        tester.total_score -= tester.ques1
        tester.ques1 = scr
        tester.total_score += scr
    elif pk == 2 and scr > tester.ques2:
        tester.total_score -= tester.ques2
        tester.ques2 = scr
        tester.total_score += scr
    elif pk == 3 and scr > tester.ques3:
        tester.total_score -= tester.ques3
        tester.ques3 = scr
        tester.total_score += scr
    elif pk == 4 and scr > tester.ques4:
        tester.total_score -= tester.ques4
        tester.ques4 = scr
        tester.total_score += scr
    elif pk == 5 and scr > tester.ques5:
        tester.total_score -= tester.ques5
        tester.ques5 = scr
        tester.total_score += scr
    elif pk == 6 and scr > tester.ques6:
        tester.total_score -= tester.ques6
        tester.ques6 = scr
        tester.total_score += scr
    tester.save()
