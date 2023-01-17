from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
import django.contrib.auth as dd
from .models import Student

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Query the database to check if the user is authenticated
        if request.user.is_authenticated:
            print(".sda.asd.asd.asd.asd.asd./123\n\n\nasdasdasdasd......")
            return view_func(request, *args, **kwargs)
        else:
            print('asdasdasd')
            return render(request, 'app/login_page.html')
    return wrapper

# Create your views here.
@login_required
def index(req):
    with connection.cursor() as cursor:
        cursor.execute('select * from pendingtasks')
        res = cursor.fetchall()
    
    return render(req, 'app/index.html', {
        'res' : res
    })

def login_page(request):
    if request.method == 'POST':
        # Get the email and password from the request
        email = request.POST.get('floatingInput')
        password = request.POST.get('floatingPassword')

        user = dd.authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            # if the credentials are valid, log the user in
            dd.login(request, user)
            return render(request, 'app/index.html')

        # Query the database to check if the user's credentials are valid
        # with connection.cursor() as cursor:
        #     cursor.execute('select * from student where password = %s and email = %s', [password, email])
        #     user = cursor.fetchall()

        #     if user and len(user) == 1:
        #         # If the user's credentials are valid
        #         # Log the user in
        #         request.session['user_id'] : user[0][0]
        #         dd.login(request, user[0][0])
        #         return render(request, 'app/index.html')
                    
        else:
            # If the user's credentials are invalid
            return HttpResponse("Invalid login credentials")
                    
        
    else:
        # If the request method is not POST
        # Render the login template
        return render(request, 'app/login.html')

def signup_page(req):
    return render(req, 'app/signup_page.html')

@login_required
def addtask(req):
    return render(req, 'app/addtask.html')

@login_required
def taskdetails(req, taskid):
    with connection.cursor() as cursor:
        cursor.execute(f'select * from pendingtasks where taskid = {taskid}')
        res = cursor.fetchall()

    return render(req, 'app/taskdetails.html', {
        'res': res
    })

def leaderboard(req):
    with connection.cursor() as cursor:
        cursor.execute('select * from pendingtasks')
        res = cursor.fetchall()
        
    return render(req, 'app/leaderboard.html', {
        'res': res
    })