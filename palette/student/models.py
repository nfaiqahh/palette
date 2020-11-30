from django.db import models

# Create your models here.

class Student(models.Model):
    StudentID = models.IntegerField(primary_key=True)
    StudentName = models.CharField(max_length=500)