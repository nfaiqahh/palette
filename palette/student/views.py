from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from student.models import Admin, Lecturer, Class, Course

# Create your views here.

def mainmenu(request):
    if request.user.is_authenticated:
        #if user is logged in, go to home page
        return redirect('home')
    else:
        #if user is not logged in, display the main page
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')

            request.session['role'] = role #role will be kept throughout the whole session
            request.session['loggedinuser'] = username

            if role == 'admin':
                if Admin.objects.filter(UserID=username).exists():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have permission to log in as Admin. Try log in as Lecturer')
            else:
                #if role == 'lecturer'
                if Lecturer.objects.filter(UserID=username).exists():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have permission to log in as Lecturer. Try log in as Admin')
    
    context = {}
    return render(request, 'mainmenu.html', context)

@login_required
def home(request):
    role = request.session['role']
    loggedinuser = request.session['loggedinuser']

    if role == 'admin':
        loggedin = Admin.objects.get(UserID=loggedinuser)
        name = loggedin.Admin_Name
        lecturers = Lecturer.objects.all()
        courses = Course.objects.all()
        template = 'admin.html'
        context = {
            "name": name,
            "lecturers": lecturers,
            "courses": courses,
        }
    else:
        loggedin = Lecturer.objects.get(UserID=loggedinuser)
        name = loggedin.Lect_Name
        classes = Class.objects.filter(Lecturer=loggedin.id)
        template = 'lecturer.html'
        context = {
            "name": name,
            "classes": classes,
        }
 
    return render(request, template, context)

def logout_view(request):
    logout(request)
    return redirect('mainmenu')