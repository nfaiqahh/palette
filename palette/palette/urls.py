"""palette URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from student import views as mainviews
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', mainviews.mainmenu, name='mainmenu'),
    path('home', mainviews.home, name='home'),
    path('logout', mainviews.logout_view, name='logout'),
    # COURSE
    path('course', mainviews.choosecourse, name='choosecourse'),
    path('course/<int:id>/<slug:courseid>', mainviews.viewcourse, name='viewcourse'),
    path('edit-course-details', mainviews.editcourse, name='editcourse'),
    path('add-course', mainviews.addcourse, name='addcourse'),
    path('updatecourse', mainviews.updatecoursedb, name='updatecourse'),
    # LECTURER
    path('lecturer', mainviews.chooselecturer, name='chooselecturer'), #redirect to 'viewlecturer'
    path('lecturer/<str:lecturerid>', mainviews.viewlecturer, name='viewlecturer'),
    path('edit-lecturer-details', mainviews.editlecturer, name='editlecturer'),
    path('add-lecturer', mainviews.addlecturer, name='addlecturer'),
    path('updatelect', mainviews.updatelecturerdb, name='updatelect'), #redirect to 'viewlecturer'
    # ADMIN
    path('admin', admin.site.urls),    
]
