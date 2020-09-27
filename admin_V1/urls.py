from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.admin_home,name = 'admin_home'),
	url(r'department/',views.show_department,name = 'show_department'),
	url(r'branch/(?P<Department_id>\d+)',views.show_branch,name = 'show_branch'),
	url(r'semester/(?P<Branch_id>\d+)',views.show_semester,name = 'show_semester'),
	url(r'division/(?P<Semester_id>\d+)',views.show_division,name = 'show_division'),
	url(r'batch/(?P<Division_id>\d+)',views.show_batch,name = 'show_batch'),
]