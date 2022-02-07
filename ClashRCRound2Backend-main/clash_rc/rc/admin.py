from django.contrib import admin
from django.db import models
from .models import *

# Register your models here.
@admin.register(RcPlayer)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["junior", "user", "total_score"]


@admin.register(RcQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "body",
        "correct_submissions",
        "total_submissions",
        "junior",
    ]


@admin.register(RcSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["p_id", "q_id", "score", "time", "code", "language", "status"]


@admin.register(Rctestcase)
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ["q_id"]
