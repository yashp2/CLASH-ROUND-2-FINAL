from django.contrib import admin
from django.db import models
from .models import *

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["junior", "user", "total_score"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "body",
        "correct_submissions",
        "total_submissions",
        "junior",
    ]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["p_id", "q_id", "score", "time", "code", "language", "status"]


@admin.register(testcase)
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ["q_id"]


@admin.register(SetTime)
class SetTimeAdmin(admin.ModelAdmin):
    list_display = ["start_time", "final_time"]
