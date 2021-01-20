from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from student.models import Admin, Lecturer, Class, Course, CourseTopic, CourseObjective

# Create your views here.
# 
# List of Modules:
# 1. Authentication
# 2. Course
# 3. Lecturer

####################################
# 1. AUTHENTICATION
####################################
def mainmenu(request):
    if request.user.is_authenticated:
        #if user is logged in, go to home page
        return redirect('home')
    else:
        #if user is not logged in, display the main page
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')

            request.session['role'] = role #role will be kept throughout the whole session
            request.session['loggedinuser'] = username

            if role == 'admin':
                if Admin.objects.filter(UserID=username).exists():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have permission to log in as Admin. Try log in as Lecturer')
            else:
                #if role == 'lecturer'
                if Lecturer.objects.filter(UserID=username).exists():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have permission to log in as Lecturer. Try log in as Admin')
    
    context = {}
    return render(request, 'mainmenu.html', context)

@login_required
def home(request):
    role = request.session['role']
    loggedinuser = request.session['loggedinuser']

    if role == 'admin':
        loggedin = Admin.objects.get(UserID=loggedinuser)
        name = loggedin.Admin_Name
        request.session['name'] = name
        lecturers = Lecturer.objects.all()
        courses = Course.objects.all()
        template = 'admin.html'
        context = {
            "name": name,
            "lecturers": lecturers,
            "courses": courses,
        }
    else:
        loggedin = Lecturer.objects.get(UserID=loggedinuser)
        name = loggedin.Lect_Name
        request.session['name'] = name
        classes = Class.objects.filter(Lecturer=loggedin.id)
        template = 'lecturer.html'
        context = {
            "name": name,
            "classes": classes,
        }
 
    return render(request, template, context)

def logout_view(request):
    logout(request)
    return redirect('mainmenu')

####################################
# 2. COURSE
####################################
def choosecourse(request):
    id = request.POST['courseID']
    course = Course.objects.get(id=id)
    course_real_id = course.CourseID #CSC 8483
    courseid = slugify(course_real_id)
    return redirect('viewcourse', id, courseid)

@login_required
def viewcourse(request, id, courseid):
    course = Course.objects.get(id=id)
    course_topics = CourseTopic.objects.filter(CourseID=id)
    course_objectives = CourseObjective.objects.filter(CourseID=id)
    class_available = Class.objects.filter(CourseID=id)
    lecturer = Lecturer.objects.all()    
    context = {
        "course": course,
        "course_topics": course_topics,
        "course_objectives": course_objectives,
        "class_available": class_available,
        "lecturer": lecturer,
    }
    return render(request, 'coursedetails.html', context)

def editcourse(request):
    id = request.POST['courseid']
    course = Course.objects.get(id=id)
    course_topics = CourseTopic.objects.filter(CourseID=id)
    course_objectives = CourseObjective.objects.filter(CourseID=id)
    course_real_id = course.CourseID #CSC 8483
    courseid = slugify(course_real_id)
    context = {
        "course": course,
        "course_topics": course_topics,
        "course_objectives": course_objectives,
        "courseid": courseid,
    }
    return render(request, 'coursedetails-edit.html', context)

def updatecoursedb(request):
    add_or_edit = request.POST['add_or_edit']

    if add_or_edit == 'edit':
        id = request.POST['courseid']
        Course_Description = request.POST['coursedesc']
        topic_count = CourseTopic.objects.filter(CourseID=id).count()
        topics = []
        for i in range(1, topic_count+1):
            topicno = str(i)
            topics.append(request.POST[topicno])
        
        course = Course.objects.get(id=id)
        course.Course_Description = Course_Description
        course_topic = CourseTopic.objects.filter(CourseID=id)
        x = 0
        for topic in course_topic:
            topic.Topic_Name = topics[x]
            topic.save()
            x = x+1
        
        course_objective = CourseObjective.objects.filter(CourseID=id)
        for obj in course_objective:
            objid = obj.ObjectiveID
            a = "objective"
            b = str(objid)
            c = a + b
            obj.Objective_Name = request.POST[c]
            obj.save()

        course.save()
        messages.add_message(request, messages.INFO, 'Course details successfully updated!')
        courseid = slugify(course.CourseID)
        return redirect('viewcourse', id, courseid)
    else:
        CourseID = request.POST['CourseID'].upper()
        Course_Name = request.POST['Course_Name']
        Course_Description = request.POST['Course_Description']
        if Course.objects.filter(CourseID = CourseID).exists():
            messages.add_message(request, messages.ERROR, 'You wanted to add a new course with the same ID, are you sure?')
            return redirect('mainmenu')
        else:
            id = Course.objects.count()+1
            insertcourse = Course(id=id, CourseID=CourseID, Course_Name=Course_Name, Course_Description=Course_Description)
            insertcourse.save()
            topic_count = request.POST['topic_count']
            obj_count = request.POST['obj_count']

            for a in range(int(topic_count)):
                b = a + 1
                c = "topic" + str(b)
                TopicID = CourseTopic.objects.count()+1
                Topic_Name = request.POST[c]
                inserttopics = CourseTopic(
                    TopicID = TopicID,
                    Topic_No = b,
                    Topic_Name = Topic_Name,
                    CourseID = insertcourse
                )
                inserttopics.save()

            for b in range(int(obj_count)):
                c = b + 1
                d = "objective" + str(c)
                ObjectiveID = CourseObjective.objects.count()+1
                if c < 10:
                    Objective_No = "CO0" + str(c)
                else:
                    Objective_No = "CO" + str(c)
                Objective_Name = request.POST[d]
                insertobj = CourseObjective(
                    ObjectiveID = ObjectiveID,
                    Objective_No = Objective_No,
                    Objective_Name = Objective_Name,
                    CourseID = insertcourse
                )            
                insertobj.save()
            messages.add_message(request, messages.INFO, 'Course succesfully created!')
            return redirect('mainmenu')


def addcourse(request):
    context = {}
    return render(request, 'coursedetails-add.html', context)

####################################
# 3. LECTURER
####################################
def chooselecturer(request):
    lecturerid = request.POST['lecturerid']
    return redirect('viewlecturer', lecturerid)

@login_required
def viewlecturer(request, lecturerid):
    lecturer = Lecturer.objects.get(UserID=lecturerid)
    class_incharge = Class.objects.filter(Lecturer=lecturer.id)
    context = {
        "lecturer": lecturer,
        "class_incharge": class_incharge,
    }
    return render(request, 'lectdetails.html', context)

def editlecturer(request):
    id = request.POST['lecturerid']
    lecturer = Lecturer.objects.get(UserID=id)
    context = {
        "lecturer": lecturer,
    }
    return render(request, 'lectdetails-edit.html', context)

def updatelecturerdb(request):
    add_or_edit = request.POST['add_or_edit']

    if add_or_edit == 'edit':
        Lect_Name = request.POST['Lect_Name']
        Lect_Email = request.POST['Lect_Email']
        lecturerid = request.POST['lecturerid']
        lecturer = Lecturer.objects.get(UserID=lecturerid)
        lecturer.Lect_Name = Lect_Name
        lecturer.Lect_Email = Lect_Email
        lecturer.save()
        messages.add_message(request, messages.INFO, 'Lecturer details succesfully updated!')
        return redirect('viewlecturer', lecturerid)

    else: #if action == 'add'        
        lecturerid = request.POST['LecturerID'] 
        Lect_Name = request.POST['Lect_Name']
        Lect_Email = request.POST['Lect_Email']
        if Lecturer.objects.filter(UserID=lecturerid).exists():
            messages.add_message(request, messages.ERROR, 'You wanted to add a new lecturer with the same ID, are you sure?')
            return redirect('viewlecturer', lecturerid)
        else:
            newlect = User.objects.create_user(lecturerid, Lect_Email, 'palette123')
            id = Lecturer.objects.count()+1
            insertlect = Lecturer(id=id, Lect_Name=Lect_Name, Lect_Email=Lect_Email, UserID=newlect)
            insertlect.save()
            messages.add_message(request, messages.INFO, 'Lecturer succesfully created!')
            return redirect('mainmenu')

def addlecturer(request):
    context = {}
    return render(request, 'lectdetails-add.html', context)

####################################
# 4. CLASS
####################################
def updateclassdb(request):
    ClassID = request.POST['ClassID']
    LecturerID = request.POST['LecturerID']
    id = request.POST['CourseID'] #single int
    course = Course.objects.get(id=id)
    lecturer = Lecturer.objects.get(id=LecturerID)
    classid = Class.objects.count()+1
    newclass = Class(
        id=classid,
        ClassID=ClassID,
        CourseID=course,
        Lecturer=lecturer
    )
    newclass.save()
    messages.add_message(request, messages.INFO, 'Class successfully added!')
    courseid = slugify(course.CourseID)
    return redirect('viewcourse', id, courseid)
