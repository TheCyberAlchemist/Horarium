from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.student_home,name = 'student_home'),
]