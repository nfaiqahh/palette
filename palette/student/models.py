from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

# Create your models here.

################################
# User - Authentication purposes
################################
# User model is the built-in Django model. Provides:
# username *required
# email *required
# password *required
# first_name
# last_name

################################
# Lecturer - Lecturer information (refer User)
################################
class Lecturer(models.Model):
    Lect_Name = models.CharField(max_length=500)
    Lect_Email = models.EmailField(max_length=254)
    UserID = models.OneToOneField(User, on_delete=models.PROTECT, to_field='username', default='ID Number')

################################
# Admin - Admin information (refer User)
################################
class Admin(models.Model):
    Admin_Name = models.CharField(max_length=500)
    Admin_Email = models.EmailField(max_length=254)
    UserID = models.OneToOneField(User, on_delete=models.PROTECT, to_field='username', default='ID Number')

################################
# Course - Course information
################################
class Course(models.Model):
    CourseID = models.CharField(max_length=10, unique=True) #eg: ABC1234
    Course_Name = models.CharField(max_length=500)
    Course_Description = models.TextField(default='Description')

################################
# Class - Class information
################################
class Class(models.Model):
    ClassID = models.CharField(max_length=10) #eg: TC01
    CourseID = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default='1'
    )
    Lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        default='1'
    )

################################
# CourseTopic - Topics for each course information
################################
class CourseTopic(models.Model):
    TopicID = models.AutoField(primary_key=True)
    CourseID = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default='1'
    )
    Topic_No = models.IntegerField()
    Topic_Name = models.CharField(max_length=500)

################################
# CourseObjective - Objectives for course
################################
class CourseObjective(models.Model):
    ObjectiveID = models.AutoField(primary_key=True)
    CourseID = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default='1'
    )
    Objective_No = models.CharField(max_length=4) #CO01
    Objective_Name = models.CharField(max_length=700)

################################
# Assessment - Student's Assessment
################################
class Assessment(models.Model):
    AssessmentID = models.AutoField(primary_key=True, unique=True) #1,2,3,4,etc..
    Assessment_Name = models.CharField(max_length=500)
    Assessment_Desc = models.TextField()
    CourseID = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default='1'
    )
    AssignedClass = models.ManyToManyField(Class)
    Lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        default='11'
    )

################################
# Student - Student information
################################
class Student(models.Model):
    StudentID = models.IntegerField(primary_key=True)
    StudentName = models.CharField(max_length=500)
    RegisteredClass = models.ManyToManyField(Class)

################################
# Question - Assessment questions
################################
class Question(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    AssessmentID = models.ForeignKey(
        Assessment,
        on_delete=models.PROTECT,
        default='1'
    )
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
    Topics = models.ManyToManyField(CourseTopic)

################################
# Answer - Student's answer records
################################
class Answer(models.Model):
    StudentID = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    Question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    ANSWER_CHOICES = [
        ('A', 'AnswerA'),
        ('B', 'AnswerB'),
        ('C', 'AnswerC'),
        ('D', 'AnswerD'),
    ]
    Answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default='A')

################################
# Result - Students result in percentage
################################
class Result(models.Model):
    Student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    Assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE
    )
    Result = models.IntegerField()