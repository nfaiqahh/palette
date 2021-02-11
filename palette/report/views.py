import io
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from student.models import Admin, Lecturer, Class, Course, CourseTopic, CourseObjective, Student, Assessment, Question, Answer, Result
from reportlab.pdfgen import canvas
from json import dumps

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
    
    #analyze performance

    #learning progress

    context = {
        "students": students,
        "classname": classname,
        "assessments": assessments,
    }
    return render(request, 'classreport.html', context)

####################################
# 2. ASSESSMENT REPORT
####################################
def viewassessment(request, Assessment_id):
    assessment = Assessment.objects.get(AssessmentID=Assessment_id)
    questions = Question.objects.filter(AssessmentID=Assessment_id)
    
    qIDs = []
    accuracy = []
    for q in questions:
        qIDs.append(q.QuestionID)
        correct = 0
        wrong = 0
        answers = Answer.objects.filter(Question=q.QuestionID)
        for a in answers:
            if ( a.Answer == a.Question.Correct_Answer ):
                correct = correct + 1
            else:
                wrong = wrong + 1
        
        acc = (correct / answers.count()) * 100
        roundAcc = round(acc)
        accuracy.append(roundAcc)

    intotable = zip(questions, accuracy)

    result = Result.objects.filter(Assessment=Assessment_id)
    highest = result[0].Result
    lowest = result[0].Result
    total = 0

    for r in result:
        x = int(r.Result)
        if (x > highest):
            highest = x
        elif (x < lowest):
            lowest = x
        total = total + x
    
    average = round(total / result.count())


    topic = CourseTopic.objects.filter(question__in=qIDs).distinct()

    context = {
        "assessment": assessment,
        "intotable": intotable,
        "questions": questions,
        "highest": highest,
        "lowest": lowest,
        "average": average,
        "topic": topic,
    }
    return render(request, 'assessmentreport.html', context)

def printreport(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='AssessmentReport.pdf')

####################################
# 3. STUDENT PERSONAL PERFORMANCE REPORT
####################################
def viewstudent(request, Class_id, StudentID):
    std_class = Class.objects.get(id=Class_id) # Get details of Class
    student = Student.objects.get(StudentID=StudentID) # Get details of Student
    assessment = Assessment.objects.filter(AssignedClass=Class_id) # Get assessments assigned to the student's class

    # For when user choose which assessment to view
    if request.method == 'GET' and 'assessment' in request.GET:
        selected_assessment = request.GET['assessment']
    else: # If user does not choose yet, automatically go to the first assessment listed
        selected_assessment = assessment[0].AssessmentID
    
    questions = Question.objects.filter(AssessmentID=selected_assessment) # Get list of questions in the assessment
    std_answer = Answer.objects.filter(StudentID=StudentID, Question__in=questions) # Get list of student's answers according to the questions
    assessment_name = Assessment.objects.get(AssessmentID=selected_assessment) # Get details of selected assessment
    result = Result.objects.filter(Assessment=selected_assessment).get(Student=StudentID) # Get student's result

    # Calculate class average score for sidebox
    classmates = Student.objects.filter(RegisteredClass=Class_id)
    ScoreSum = 0
    totalStdnts = classmates.count()
    for c in classmates:
        score = Result.objects.filter(Assessment=selected_assessment).get(Student=c.StudentID)
        ScoreSum = ScoreSum + int(score.Result)
    avg = round(ScoreSum / totalStdnts)

    # Calculate learning progress for sidebox
    qIDs = []
    for a in assessment:
        ques = Question.objects.filter(AssessmentID=a.AssessmentID)
        for q in ques:
            qIDs.append(q.QuestionID) # Get all IDs of questions answered by the student
    
    topic = CourseTopic.objects.filter(question__in=qIDs).distinct() # Get topics in questions
    answers = Answer.objects.filter(StudentID=StudentID, Question__in=qIDs) # Get all answers from students
    topicPercentage = []
    for t in topic:
        x = 0
        y = 0
        q = Question.objects.filter(Topics=t) # Get Questions under the topic
        for ans in answers: # For every answers from student
            if ans.Question in q: # Check if the answers is for the questions under the topic
                if (ans.Answer == ans.Question.Correct_Answer): # Check if answer is correct, add 1 to x
                    x = x + 1
                y = y + 1 # Total of questions in the topic
        z = round((x / y)*100) # Calculate score for each topics
        topicPercentage.append(z)

    totalPercentage = 0
    for t in topicPercentage:
        totalPercentage = totalPercentage + int(t)

    LearningProgress = round(totalPercentage / (int(len(topicPercentage))))
    LPjs = dumps(LearningProgress)   
    
    # List critical topics - (less than 35% accuracy) for sidebox
    
    context = {
        "std_class": std_class,
        "student": student,
        "assessment": assessment,
        "assessment_name": assessment_name,
        "std_answer": std_answer,
        "result": result,
        "avg": avg,
        "LearningProgress": LearningProgress,
        "LPjs": LPjs,
    }
    return render(request, 'studentreport.html', context)
