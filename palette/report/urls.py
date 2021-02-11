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

from django.urls import path, include
from report import views as report

urlpatterns = [
    # CLASS PERFORMANCE REPORT
    path('class/<int:Class_id>', report.viewclass, name='classreport'),
    # ASSESSMENT REPORT
    path('assessment/<int:Assessment_id>', report.viewassessment, name='assessmentreport'),
    path('printreport', report.printreport, name='print'),
    # STUDENT PERSONAL PERFORMANCE REPORT
    path('class/<int:Class_id>/<int:StudentID>', report.viewstudent, name='viewstudent'),
]
