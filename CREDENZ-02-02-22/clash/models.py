from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    junior = models.BooleanField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(null=True, default=0)
    ques1 = models.IntegerField(null=True, default=0)
    ques2 = models.IntegerField(null=True, default=0)
    ques3 = models.IntegerField(null=True, default=0)
    ques4 = models.IntegerField(null=True, default=0)
    ques5 = models.IntegerField(null=True, default=0)
    ques6 = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.user.username)


class Question(models.Model):
    title = models.CharField(max_length=1003, null=True)
    body = models.TextField(null=True)  # text field.
    input_format=models.TextField(null=True)
    output_format=models.TextField(null=True)
    constraints=models.TextField(null=True)
    sample_input=models.TextField(null=True)
    sample_output=models.TextField(null=True)
    explaination=models.TextField(null=True)
    correct_submissions = models.IntegerField(null=True)
    total_submissions = models.IntegerField(null=True)
    accuracy = models.FloatField(null=True)
    junior = models.BooleanField(null=True)
    # questions score for junior senior.
    def __str__(self):
        return self.title


class Submission(models.Model):
    q_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    p_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    code = models.TextField(null=True)  # text field
    status = models.CharField(
        max_length=10,
        null=True,
        choices=(
            ("WA", "Wrong Answer"),
            ("AC", "Accepted"),
            ("TLE", "Time Limit Exceeded"),
            ("CTE", "Compile Time Error"),
            ("RE", "Runtime Error"),
            ("MLE", "Memory Limit Exceeded"),
        ),
    )  # four type of submission status(WA, PASS, TLE, CTE)
    language = models.CharField(
        max_length=10, null=True, choices=(("c", "C"), ("cpp", "C++"), ("py", "Python"))
    )


def get_question_path(state):
    return "Question_Data/{0}".format(state)


class testcase(models.Model):
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    tc_input = models.FileField(null=True, upload_to=get_question_path("Input"))
    tc_output = models.FileField(null=True, upload_to=get_question_path("Output"))


class SetTime(models.Model):
    start_time = models.DateTimeField(auto_now_add=False)
    final_time = models.DateTimeField(auto_now_add=False)
