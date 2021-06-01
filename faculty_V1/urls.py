from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.faculty_home,name = 'faculty_home'),
	path('feedback/',views.faculty_feedback,name = 'faculty_feedback'),
]