from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from student.models import Admin, Lecturer, Class, Course, CourseTopic, CourseObjective, Student, Assessment, Question, Answer

# Create your views here.
# 
# List of Modules:
# 1. Class Performance Report
# 2. Assessment Report
# 3. Student Personal Performance Report

####################################
# 1. CLASS PERFORMANCE REPORT
####################################
def viewclass(request, Class_id):
    students = Student.objects.filter(RegisteredClass=Class_id)
    classname = Class.objects.get(id=Class_id)
    assessments = Assessment.objects.filter(AssignedClass=Class_id)
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
def viewstudent(request, Class_id, StudentID):
    std_class = Class.objects.get(id=Class_id)
    student = Student.objects.get(StudentID=StudentID)
    assessment = Assessment.objects.filter(AssignedClass=Class_id)

    if request.method == 'GET' and 'assessment' in request.GET:
        selected_assessment = request.GET['assessment']
    else:
        selected_assessment = assessment[0].AssessmentID
        
    questions = Question.objects.filter(AssessmentID=selected_assessment)
    std_answer = Answer.objects.filter(StudentID=StudentID, Question__in=questions)
    assessment_name = Assessment.objects.get(AssessmentID=selected_assessment)

    context = {
        "std_class": std_class,
        "student": student,
        "assessment": assessment,
        "assessment_name": assessment_name,
        "std_answer": std_answer,
    }
    return render(request, 'studentreport.html', context)