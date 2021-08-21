from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.faculty_home,name = 'faculty_home'),
	path('settings/',views.faculty_settings,name="faculty_settings"),
	path('feedback/',views.faculty_feedback,name = 'faculty_feedback'),
	path('attendance/',views.attendance,name = 'attendance'),
]