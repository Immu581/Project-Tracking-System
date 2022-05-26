from django.db import models

# Create your models here.
class Mentor(models.Model):
    mid=models.BigAutoField(primary_key=True,default=None,blank=True)
    mname=models.CharField(max_length=20)
    memailid=models.CharField(max_length=20)
    mpassword=models.CharField(max_length=10)
class Project(models.Model):
    pid=models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=30)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)
class Student(models.Model):
    rollno=models.CharField(max_length=10,primary_key=True)
    emailid=models.CharField(max_length=50)
    name=models.CharField(max_length=20)
class Evaluation(models.Model):
    rollno=models.CharField(max_length=10,primary_key=True)
    m1=models.FloatField(blank=True,null=True)
    m2=models.FloatField(blank=True,null=True)
    m3=models.FloatField(blank=True,null=True)
    avg=models.FloatField()

class Review(models.Model):
    r1=models.CharField(max_length=10,blank=True,null=True)
    r2=models.CharField(max_length=10,blank=True,null=True)
    r3=models.CharField(max_length=10,blank=True,null=True)

class Assign(models.Model):
    rollno=models.CharField(max_length=10)
    pid=models.IntegerField()
    mid=models.IntegerField(blank=True,null=True)