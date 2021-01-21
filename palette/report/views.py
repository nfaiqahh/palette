from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from student.models import Admin, Lecturer, Class, Course, CourseTopic, CourseObjective, Student

# Create your views here.
def viewclass(request):
    id = request.POST['Class_id']
    students = Student.objects.filter(RegisteredClass=id)
    classname = Class.objects.get(id=id)
    context = {
        "students": students,
        "classname": classname,
    }
    return render(request, 'classreport.html', context)
