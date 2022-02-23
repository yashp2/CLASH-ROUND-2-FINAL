from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard', views.leaderboard, name = 'clash-leaderboard'),
    path('question/', views.contest, name = 'clash-contest'),
    path('question/<int:pk>',views.question,name='clash-question'),
    path('home', views.home, name = 'clash-home'),
    path('mysubs/<int:pk>',views.mysubmission,name='clash-mysub'),
    path('submit/<int:pk>',views.clash_sub,name='clash-sub'),
    path('logout',views.logout_view,name='logout'),
    path('buffer/<int:pk>',views.buffer,name='buffer'),
    # path('leaderboard1',views.leaderboardf,name='lb'),

]