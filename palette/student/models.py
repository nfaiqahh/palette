from django.db import models

# Create your models here.

################################
# User - Authentication purposes
################################

################################
# Lecturer - Lecturer information (refer User)
################################
class Lecturer(models.Model):
    Lect_Name = models.CharField(max_length=500)
    Lect_Email = models.EmailField(max_length=254)
    #UserID (foreign key User)

################################
# Admin - Admin information (refer User)
################################
class Admin(models.Model):
    Admin_Name = models.CharField(max_length=500)
    Admin_Email = models.EmailField(max_length=254)
    #UserID (foreign key User)

################################
# Request - Edit course details request
################################
class Request(models.Model):
    RequestID = models.CharField(max_length=10) #eg: RQ + id = RQ1, RQ2...
    #CourseID (foreign key Course)
    #UserID (foreign key User)
    Status = models.BooleanField() #True: Approved, False: Denied

################################
# Class - Class information
################################
class Class(models.Model):
    ClassID = models.CharField(max_length=10) #eg: TC01
    #CourseID (foreign key Course)

################################
# Course - Course information
################################
class Course(models.Model):
    CourseID = models.CharField(max_length=10) #eg: ABC1234
    Course_Name = models.CharField(max_length=500)
    #Course_Description = models.

################################
# CourseTopic - Topics for each course information
################################
class CourseTopic(models.Model):
    TopicID = models.AutoField(primary_key=True)
    #CourseID (foreign key Course)
    Topic_No = models.IntegerField()
    Topic_Name = models.CharField(max_length=500)

################################
# CourseObjective - Objectives for course
################################
class CourseObjective(models.Model):
    ObjectiveID = models.AutoField(primary_key=True)
    #CourseID (foreign key Course)
    Objective_No = models.CharField(max_length=4) #CO01
    Objective_Name = models.CharField(max_length=700)

################################
# CourseObjective - Objectives for course
################################
class Assessment(models.Model):
    AssessmentID = models.AutoField(primary_key=True)
    Assessment_Name = models.CharField(max_length=500)
    Assessment_Desc = models.TextField()
    #CourseID (foreign key Course)

################################
# Student - Student information
################################
class Student(models.Model):
    StudentID = models.IntegerField(primary_key=True)
    StudentName = models.CharField(max_length=500)

################################
# Question - Assessment questions
################################
class Question(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    #AssessmentID (foreign key Assessment)
    Question = models.TextField()
    Answer_1 = models.CharField(max_length=500)
    Answer_2 = models.CharField(max_length=500)
    Answer_3 = models.CharField(max_length=500)
    Answer_4 = models.CharField(max_length=500)
    ANSWER_CHOICES = [
        ('A', 'AnswerA'),
        ('B', 'AnswerB'),
        ('C', 'AnswerC'),
        ('D', 'AnswerD'),
    ]
    Correct_Answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default='A')
    Answer_Explanation = models.TextField()
    #Topics (array of topics according to CourseID in Assessment info)
    #Objectives (array of objectives according to CourseID in assessment)
