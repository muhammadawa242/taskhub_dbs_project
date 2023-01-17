from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
import django.contrib.auth as dd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

USER_ID = None

# Create your views here.
@login_required(login_url='login_page')
def index(req):
    with connection.cursor() as cursor:
        cursor.execute('select * from pendingtasks')
        res = cursor.fetchall()
    
    return render(req, 'app/index.html', {
        'res' : res
    })

def logout_page(request):
    global USER_ID
    dd.logout(request)
    USER_ID = None
    return HttpResponseRedirect('/')

def login_page(request):
    if request.method == 'POST':
        # Get the username and password from the request
        username = request.POST.get('floatingInput')
        password = request.POST.get('floatingPassword')

        user = dd.authenticate(request, username=username, password=password)
        if user is not None:
            # if the credentials are valid, log the user in
            dd.login(request, user)
            
        # Query the database to check if the user's credentials are valid
            with connection.cursor() as cursor:
                cursor.execute('select * from student where password = %s and dp_name = %s', [password, username])
                res = cursor.fetchall()
                global USER_ID
                USER_ID = res[0][0]

                return HttpResponseRedirect('/app')
                    
        else:
            # If the user's credentials are invalid
            return HttpResponse("Invalid login credentials")
                    
        
    else:
        # If the request method is not POST
        # Render the login template
        return render(request, 'app/login_page.html')

def signup_page(request):
    if request.method == 'POST':
        # Save data and make username, password variables
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dp_name = request.POST.get('dp_name')
        pic = request.POST.get('pic')
        uniname = request.POST.get('uniname')
        campus = request.POST.get('campus')
        area = request.POST.get('area')
        city = request.POST.get('city')
        refsid = int(request.POST.get('refsid'))
        password = request.POST.get('password')

        # Insert into Student Table
        with connection.cursor() as cursor:
            try:
                cursor.execute('select addressid from address where city = %s and area = %s', [city, area])
                addressid = cursor.fetchall()[0][0]
                print(addressid)
                
                cursor.execute('insert into student (Name, Age, Gender, Email, Phone, DP_Name, Pic, UniName, Campus, AddressId, refSid, password) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [name, age, gender, email, phone, dp_name, pic, uniname, campus, addressid, refsid, password])
            except(Exception):
                print([name, age, gender, email, phone, dp_name, pic, uniname, campus, addressid, refsid, password])
                return HttpResponse([name, age, gender, email, phone, dp_name, pic, uniname, campus, addressid, refsid, password])
            
        # Insert into admin_users Table for django
        user = User.objects.create_user(username=dp_name, email=email, password=password)
        user.save()
        
        # Log the user in
        user = dd.authenticate(request, username=dp_name, password=password)
        if user is not None:
            # if the credentials are valid, log the user in
            dd.login(request, user)
            
            # Query the database to check if the user's credentials are valid
            with connection.cursor() as cursor:
                cursor.execute('select * from student where password = %s and dp_name = %s', [password, dp_name])
                res = cursor.fetchall()
                global USER_ID
                USER_ID = res[0][0]

                return HttpResponseRedirect('/app')
        else:
            # If the user's credentials are invalid
            return HttpResponse("Some Error occured while signing you up")
        
        
    else:
        with connection.cursor() as cursor:
            cursor.execute('select distinct area from address')
            areas = cursor.fetchall()
            
            cursor.execute('select distinct city from address')
            cities = cursor.fetchall()
            
            cursor.execute('select * from student')
            users = cursor.fetchall()
            

        return render(request, 'app/signup_page.html', {
            'areas': areas,
            'cities': cities,
            'users':users,
        })

@login_required(login_url='login_page')
def addtask(req):
    return render(req, 'app/addtask.html')

@login_required(login_url='login_page')
def taskdetails(req, taskid):
    with connection.cursor() as cursor:
        cursor.execute('select * from pendingtasks where taskid = %s', [taskid])
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