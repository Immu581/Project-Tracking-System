from typing import Tuple
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import random
import datetime


# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        #print(username,password)
        if username=="" and password=="":
            #open project coordinators related pages
            p=Project.objects.all()
            if(p.count()!=0):
                pid=[str(i.pid) for i in p]
                title=[str(i.title) for i in p]
                myzip=zip(pid,title)
                return render(request,"Projectdetails.html",{'myzip':myzip,'t':False});
            else:
                return render(request,"Projectdetails.html",{'myzip':[],'t':True});
        elif Project.objects.filter(username=username,password=password).exists():
            #open student related pages
            p=Project.objects.filter(username=username,password=password)
            l=[]
            tit=""
            for i in p:
                l.append(int(i.pid))
                tit+=str(i.title)
                break
            #print(l,tit,p)
            s=Assign.objects.filter(pid=l[0])
            rolls=[str(i.rollno) for i in s]
            st=Student.objects.all()
            names=[]
            emails=[]
            k=0
            for i in st:
                if(str(i.rollno)==rolls[k]):
                    names.append(str(i.name))
                    emails.append(str(i.emailid))
                    k+=1
            #print(s,st,rolls,names)
            myzip=zip(rolls,names,emails)
            return render(request,"student.html",{'title':tit,'myzip':myzip})
        else:
            messages.info(request,"username or password in wrong")
            return redirect("/")





        return render(request,"index.html")
    return render(request,"login.html")


def register(request):
    if request.method=="POST":
        title=request.POST['ptitle']
        size=int(request.POST.get('size',7))
        username=request.POST['username']
        password=request.POST['password']
        #store all the details in db;
        if Project.objects.filter(title=title).exists():
            messages.info(request,title+" already registered in another project")
            return render(request,"register1.html")
        elif Project.objects.filter(username=username).exists():
            messages.info(request,username+" already used in another project")
            return render(request,"register1.html")
        #print(size,username,password)
        return render(request,"register2.html",{'title':title,'size':range(size),'username':username,'password':password,'count':size})
    return render(request,"register1.html")

def complete_registration(request):
    name=request.GET.getlist('name')
    rollno=request.GET.getlist('rollno')
    emailid=request.GET.getlist('emailid')
    title=request.GET['ptitle']
    username=request.GET['username']
    password=request.GET['password']
    size=int(request.GET['size'])
    #branch=request.POST.getlist('branch')
    #print(name,rollno,emailid)
    for i in range(len(name)):
        if Student.objects.filter(rollno=rollno[i]).exists():
            messages.info(request,rollno[i]+" already registered in another project")
            return redirect("/register")
        if Student.objects.filter(emailid=emailid[i]).exists():
            messages.info(request,emailid[i]+" already registered in another project")
            return redirect("/register")
        else:
            Student(rollno=rollno[i],emailid=emailid[i],name=name[i]).save()
    Project(title=title,username=username,password=password).save()
    p=Project.objects.all();
    l=[int(i.pid) for i in p if str(i.title)==title]
    #print(l)
    for i in range(len(name)):
        Assign(rollno=rollno[i],pid=l[0]).save();
    return render(request,"index.html")


def forget(request):
    if request.method=="POST":
        username=request.POST['username']
        if not Project.objects.filter(username=username).exists():
            messages.info(request,username+" doesnot exists")
            return redirect("/forget")
        subject="OTP status"
        num=random.randint(100000,999999)
        #print(username,num)
        message="Your One Time Password (OTP)  is: "+str(num)
        # send mails to all mails corresponding to username 
        p=Project.objects.all();
        l=[int(i.pid) for i in p if str(i.username)==username]
        project_id=l[0];
        l=[]
        a=Assign.objects.all();
        l=[str(i.rollno) for i in a if int(i.pid)==project_id]
        s=Student.objects.all()
        emails=[]
        for i in s:
            for j in l:
                if str(i.rollno)==j:
                    emails.append(str(i.emailid))
                    break;
        print(emails)
        for i in emails:
            if not send_mail(subject,message,settings.EMAIL_HOST_USER,[i],fail_silently=False):
                messages.info(request,"email is not valid")
                return redirect('/forget')
        return render(request,"otp.html",{'otp':num,'username':username})
    return render(request,"Forget.html")

def forget_user(request):
    if request.GET['otp1']==request.GET['otp']:
        #print(request.GET['username1'])
        return render(request,"password.html",{'username':request.GET['username1']})
    messages.info(request,"otp is not matching")
    return render(request,"Forget.html")   #need send otp messages to same html page

def change_password(request):
    #if request.method=="POST":
        username=request.GET['username']
        pass1=request.GET['pass1']
        pass2=request.GET['pass2']
        if pass1==pass2:
            #print(username,pass1,pass2)
            p=Project.objects.all()
            l=[int(i.pid) for i in p if str(i.username)==username]
            k=Project(pid=l[0],password=pass1)
            k.save(update_fields=['password'])
            #print(p)
            return render(request,"index.html") # need to show the success page
        else:
            messages.info(request,"passwords are not matching")
            return render(request,'password.html') 


def project(request):
    pid=int(request.GET.get('params'))
    #print(pid)
    t=Project.objects.filter(pid=pid)
    title=[str(i.title) for i in t]
    a=Assign.objects.filter(pid=pid)
    rollno=[str(i.rollno) for i in a]
    names=[]
    for i in rollno:
        s=Student.objects.filter(rollno=i)
        for j in s:
            names.append(j.name)
            break
    #print(names,rollno,title[0])
    myzip=zip(rollno,names)
    m=Mentor.objects.all()
    ment=[str(i.mname) for i in m]
    mids=[str(i.mid) for i in m]
    mentors=zip(mids,ment)

    
    # adding mentors is pending



    return render(request,"project.html",{'myzip':myzip,'title':title[0],'mentors':mentors})


def addmentors(request):
    if request.method=="POST":
        name=request.POST['name']
        emailid=request.POST['emailid']
        password=request.POST['password']
        #print(name,emailid)
        try:
            if(Mentor.objects.filter(memailid=emailid).exists()):
                messages.info(request,name+" already exists")
            else:
                Mentor(mname=name,memailid=emailid,mpassword=password).save()# getting error
                messages.info(request,name+" details are added successfully")
        except:
            messages.info(request,"something went wrong")
        return redirect('/addmentors')
    return render(request,"Addmentors.html")

def reviewdates(request):
    r=Review.objects.all()
    l=[]
    for i in r:
        print(i)
        if(i.r1!=0):
            l.append(i.r1)
        else:
            l.append("")
        if(i.r2!=0):
            l.append(i.r2)
        else:
            l.append("")
        if(i.r3!=0):
            l.append(i.r3)
        else:
            l.append("")
    #print(l)
    if request.method=="POST":
        dates=request.POST['dates']
        reviewno=request.POST['reviewno']
        if(dates!=""):
            if(reviewno=="1"):
                Review(id=1,r1=dates).save(update_fields=['r1'])
            if(reviewno=="2"):
                Review(id=1,r2=dates).save(update_fields=['r2'])
            if(reviewno=="3"):
                Review(id=1,r3=dates).save(update_fields=['r3'])
            r=Review.objects.all()
            l=[]
            for i in r:
                print(i)
                if(i.r1!='0'):
                    l.append(i.r1)
                else:
                    l.append("")
                if(i.r2!="0"):
                    l.append(i.r2)
                else:
                    l.append("")
                if(i.r3!="0"):
                    l.append(i.r3)
                else:
                    l.append("")
            #print(l)
    return render(request,"Reviewdates.html",{'a':l[0],'b':l[1],'c':l[2]})

def projectdetails(request):
    p=Project.objects.all()
    if(p.count()!=0):
        pid=[str(i.pid) for i in p]
        title=[str(i.title) for i in p]
        myzip=zip(pid,title)
        return render(request,"Projectdetails.html",{'myzip':myzip,'t':False});
    else:
        return render(request,"Projectdetails.html",{'myzip':[],'t':True});