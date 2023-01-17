from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "app"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page'),
    path('signup_page', views.signup_page, name='signup_page'),
    path('addtask', views.addtask, name='addtask'),
    path('taskdetails/<int:taskid>', views.taskdetails, name='taskdetails'),
    path('leaderboard', views.leaderboard, name='leaderboard')
]