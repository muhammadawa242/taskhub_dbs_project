from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('signup_page', views.signup_page, name='signup_page'),
    path('addtask', views.addtask, name='addtask'),
    path('taskdetails/<int:taskid>', views.taskdetails, name='taskdetails'),
    path('leaderboard', views.leaderboard, name='leaderboard')
]