from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard', views.leaderboard, name = 'rc-leaderboard'),
    path('question/', views.contest, name = 'rc-contest'),
    path('question/<int:pk>',views.question,name='rc-question'),
    path('home', views.home, name = 'rc-home'),
    path('mysubs/<int:pk>',views.mysubmission,name='rc-mysub'),
    path('submit/<int:pk>',views.rc_sub,name='rc-sub'),
    path('RC/<int:pk>',views.RC,name='rc-RC')
]
