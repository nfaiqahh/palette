from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from student.models import Admin, Lecturer, Class, Course, CourseTopic, CourseObjective, Student, Assessment, Question

# Create your views here.
# 
# List of Modules:
# 1. Class Performance Report
# 2. Assessment Report
# 3. Student Personal Performance Report

####################################
# 1. CLASS PERFORMANCE REPORT
####################################
def viewclass(request):
    id = request.POST['Class_id']
    students = Student.objects.filter(RegisteredClass=id)
    classname = Class.objects.get(id=id)
    assessments = Assessment.objects.filter(AssignedClass=id)
    context = {
        "students": students,
        "classname": classname,
        "assessments": assessments,
    }
    return render(request, 'classreport.html', context)

####################################
# 2. ASSESSMENT REPORT
####################################
#scores: highest, average, lowest
#list of topics related to this assessment
#accuracy
def viewassessment(request):
    AssessmentID = request.POST['AssessmentID']
    assessment = Assessment.objects.get(AssessmentID=AssessmentID)
    questions = Question.objects.filter(AssessmentID=AssessmentID)
    qno = questions.count()
    context = {
        "assessment": assessment,
        "questions": questions,
        "range": range(1,qno+1),
    }
    return render(request, 'assessmentreport.html', context)

####################################
# 3. STUDENT PERSONAL PERFORMANCE REPORT
####################################
