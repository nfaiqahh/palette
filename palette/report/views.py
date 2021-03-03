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
from django.conf import settings
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from django.views.generic import DetailView
from easy_pdf.rendering import render_to_pdf, render_to_pdf_response

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
    students = Student.objects.filter(RegisteredClass=Class_id).order_by('StudentID')
    classname = Class.objects.get(id=Class_id)
    assessments = Assessment.objects.filter(AssignedClass=Class_id)
    available = True

    if assessments.exists():
        #learning progress for each student
        learningprogress = [] # Array of learning progress for each student i.e: Student 1 = learningprogress[0] = 75
        qIDs = []
        for a in assessments:
            ques = Question.objects.filter(AssessmentID=a.AssessmentID)
            for q in ques:
                qIDs.append(q.QuestionID) # Get all IDs of questions in the assessments
        
        topic = CourseTopic.objects.filter(question__in=qIDs).distinct() # Get topics in questions
        for s in students:
            answers = Answer.objects.filter(StudentID=s.StudentID, Question__in=qIDs) # Get all answers from students
            if answers.exists():
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

                lp = round(totalPercentage / (int(len(topicPercentage))))
                learningprogress.append(lp)
            else:
                available = False
                break
            
        LPjs = dumps(learningprogress)

        #analyze performance for each student
        #Using Decision Tree Classifier concept, classify students into Good, Average, Bad performance based on:
        # 1. Marks
        # 2. Percentage of Learning Progress

        stumarks = []
        avgStumark = 0

        #Get total of marks from Result for each Student: stumarks = total student result (in percentage)
        #e.g. stumarks for Student 1110002727 = 70% + 80% = 150 
        for s in students:
            totalStumark = 0            
            for a in assessments:
                mark = Result.objects.filter(Assessment=a.AssessmentID, Student=s.StudentID)
                for rsult in mark:
                    totalStumark = totalStumark + int(rsult.Result)            
            avgStumark = avgStumark + totalStumark #Get the average stumark
            stumarks.append(totalStumark)

        avgStumark = round( avgStumark / (int(len(stumarks)))) #average 

        #Classification:
        # 1. Marks < (avgStumark - 2) AND learningprogress < 50 (LOW)
        # 2. Marks > (avgStumark + 2) AND learningprogress > 50 (HIGH)
        # 3. else, (AVERAGE)
        performance = []
        data_low = 0
        data_high = 0
        data_avg = 0
        if (avgStumark != 0):
            for m in stumarks:
                stuindex = stumarks.index(m)
                if ((m < (avgStumark-2)) and (learningprogress[stuindex] < 50)):
                    performance.append("LOW")
                    data_low = data_low + 1
                elif ((m > (avgStumark+2)) and (learningprogress[stuindex] > 50)):
                    performance.append("HIGH")
                    data_high = data_high + 1
                else:
                    performance.append("AVERAGE")
                    data_avg = data_avg + 1

        intotable = zip(students, performance)

        #Pie Chart
        labels = ["High", "Average", "Low"]
        data = [data_high, data_avg, data_low]

        context = {
            "students": students,
            "classname": classname,
            "assessments": assessments,
            "LPjs": LPjs,
            "available": available,
            "performance": performance,
            "intotable": intotable,
            "labels": labels,
            "data": data,
        }
    else:
        available = False
        context = {
            "students": students,
            "classname": classname,
            "available": available
        }

    return render(request, 'classreport.html', context)

def print_class(request, Class_id):
    students = Student.objects.filter(RegisteredClass=Class_id).order_by('StudentID')
    classname = Class.objects.get(id=Class_id)
    assessments = Assessment.objects.filter(AssignedClass=Class_id)
    available = True

    if assessments.exists():
        #learning progress for each student
        learningprogress = [] # Array of learning progress for each student i.e: Student 1 = learningprogress[0] = 75
        qIDs = []
        for a in assessments:
            ques = Question.objects.filter(AssessmentID=a.AssessmentID)
            for q in ques:
                qIDs.append(q.QuestionID) # Get all IDs of questions in the assessments
        
        topic = CourseTopic.objects.filter(question__in=qIDs).distinct() # Get topics in questions
        for s in students:
            answers = Answer.objects.filter(StudentID=s.StudentID, Question__in=qIDs) # Get all answers from students
            if answers.exists():
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

                lp = round(totalPercentage / (int(len(topicPercentage))))
                learningprogress.append(lp)
            else:
                available = False
                break
            
        LPjs = dumps(learningprogress)

        #analyze performance for each student
        #Using Decision Tree Classifier concept, classify students into Good, Average, Bad performance based on:
        # 1. Marks
        # 2. Percentage of Learning Progress

        stumarks = []
        avgStumark = 0

        #Get total of marks from Result for each Student: stumarks = total student result (in percentage)
        #e.g. stumarks for Student 1110002727 = 70% + 80% = 150 
        for s in students:
            totalStumark = 0            
            for a in assessments:
                mark = Result.objects.filter(Assessment=a.AssessmentID, Student=s.StudentID)
                for rsult in mark:
                    totalStumark = totalStumark + int(rsult.Result)            
            avgStumark = avgStumark + totalStumark #Get the average stumark
            stumarks.append(totalStumark)

        avgStumark = round( avgStumark / (int(len(stumarks)))) #average 

        #Classification:
        # 1. Marks < (avgStumark - 2) AND learningprogress < 50 (LOW)
        # 2. Marks > (avgStumark + 2) AND learningprogress > 50 (HIGH)
        # 3. else, (AVERAGE)
        performance = []
        data_low = 0
        data_high = 0
        data_avg = 0
        if (avgStumark != 0):
            for m in stumarks:
                stuindex = stumarks.index(m)
                if ((m < (avgStumark-2)) and (learningprogress[stuindex] < 50)):
                    performance.append("LOW")
                    data_low = data_low + 1
                elif ((m > (avgStumark+2)) and (learningprogress[stuindex] > 50)):
                    performance.append("HIGH")
                    data_high = data_high + 1
                else:
                    performance.append("AVERAGE")
                    data_avg = data_avg + 1

        intotable = zip(students, performance, learningprogress)

        #Pie Chart
        labels = ["High", "Average", "Low"]
        data = [data_high, data_avg, data_low]

        context = {
            "students": students,
            "classname": classname,
            "assessments": assessments,
            "LPjs": LPjs,
            "available": available,
            "performance": performance,
            "intotable": intotable,
            "labels": labels,
            "data": data,
        }
    else:
        available = False
        context = {
            "students": students,
            "classname": classname,
            "available": available
        }

    return render_to_pdf_response(request, 'pdf-classreport.html', context)

####################################
# 2. ASSESSMENT REPORT
####################################
def viewassessment(request, Assessment_id):
    assessment = Assessment.objects.get(AssessmentID=Assessment_id)
    questions = Question.objects.filter(AssessmentID=Assessment_id)
    available = True

    qIDs = []
    accuracy = []
    for q in questions:
        qIDs.append(q.QuestionID)

    if Answer.objects.filter(Question__in=qIDs).exists():
        for q in questions:
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
            "available": available,
        }
    else:
        topic = CourseTopic.objects.filter(question__in=qIDs).distinct()
        available = False
        context = {
            "assessment":assessment,
            "questions":questions,
            "topic": topic,
            "available": available,
        }
    return render(request, 'assessmentreport.html', context)

def print_assessment(request, Assessment_id):
    assessment = Assessment.objects.get(AssessmentID=Assessment_id)
    questions = Question.objects.filter(AssessmentID=Assessment_id)
    available = True

    qIDs = []
    accuracy = []
    for q in questions:
        qIDs.append(q.QuestionID)

    if Answer.objects.filter(Question__in=qIDs).exists():
        for q in questions:
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
            "available": available,
        }
    else:
        topic = CourseTopic.objects.filter(question__in=qIDs).distinct()
        available = False
        context = {
            "assessment":assessment,
            "questions":questions,
            "topic": topic,
            "available": available,
        }
    return render_to_pdf_response(request,'pdf-assessmentreport.html', context)

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
    criticaltopics = [] # List critical topics - (less than 35% accuracy) for sidebox
    for t in topicPercentage:
        if (t <= 50):
            index = topicPercentage.index(t)
            criticaltopics.append(topic[index])
        totalPercentage = totalPercentage + int(t)

    LearningProgress = round(totalPercentage / (int(len(topicPercentage))))
    LPjs = dumps(LearningProgress)

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
        "criticaltopics": criticaltopics,
    }
    return render(request, 'studentreport.html', context)

def print_student(request, Class_id, StudentID, AssessmentID):
    std_class = Class.objects.get(id=Class_id) # Get details of Class
    student = Student.objects.get(StudentID=StudentID) # Get details of Student
    assessment = Assessment.objects.filter(AssignedClass=Class_id) # Get assessments assigned to the student's class
    
    questions = Question.objects.filter(AssessmentID=AssessmentID) # Get list of questions in the assessment
    std_answer = Answer.objects.filter(StudentID=StudentID, Question__in=questions) # Get list of student's answers according to the questions
    assessment_name = Assessment.objects.get(AssessmentID=AssessmentID) # Get details of selected assessment
    result = Result.objects.filter(Assessment=AssessmentID).get(Student=StudentID) # Get student's result

    # Calculate class average score for sidebox
    classmates = Student.objects.filter(RegisteredClass=Class_id)
    ScoreSum = 0
    totalStdnts = classmates.count()
    for c in classmates:
        score = Result.objects.filter(Assessment=AssessmentID).get(Student=c.StudentID)
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
    criticaltopics = [] # List critical topics - (less than 35% accuracy) for sidebox
    for t in topicPercentage:
        if (t <= 50):
            index = topicPercentage.index(t)
            criticaltopics.append(topic[index])
        totalPercentage = totalPercentage + int(t)

    LearningProgress = round(totalPercentage / (int(len(topicPercentage))))
    LPjs = dumps(LearningProgress)

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
        "criticaltopics": criticaltopics,
    }
    return render_to_pdf_response(request, 'pdf-studentreport.html', context)