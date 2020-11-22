from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.admin_home,name = 'admin_home'),
	
	url(r'^department/$',views.show_department,name = 'show_department'),
	url(r'^department/(?P<Department_id>\d+)/$',views.show_department,name = 'update_department'),

	url(r'^branch/(?P<Department_id>\d+)/$',views.show_branch,name = 'show_branch'),
	url(r'^branch/(?P<Department_id>\d+)/(?P<Branch_id>\d+)/$',views.show_branch,name = 'update_branch'),
	
	url(r'^semester/(?P<Branch_id>\d+)/$',views.show_semester,name = 'show_semester'),
	url(r'^semester/(?P<Branch_id>\d+)/(?P<Semester_id>\d+)/$',views.show_semester,name = 'update_semester'),
	
	url(r'^division/(?P<Semester_id>\d+)/$',views.show_division,name = 'show_division'),
	url(r'^division/(?P<Semester_id>\d+)/(?P<Division_id>\d+)/$',views.show_division,name = 'update_division'),
	
	url(r'^batch/(?P<Division_id>\d+)/$',views.show_batch,name = 'show_batch'),
	url(r'^batch/(?P<Division_id>\d+)/(?P<Batch_id>\d+)/$',views.show_batch,name = 'update_batch'),
	
	url(r'^shift/(?P<Department_id>\d+)/$',views.show_shift,name = 'show_shift'),
	url(r'^shift/(?P<Department_id>\d+)/(?P<Shift_id>\d+)/$',views.show_shift,name = 'update_shift'),
	
	url(r'^slot/(?P<Shift_id>\d+)/$',views.show_slot,name = 'show_slot'),
	
	url(r'^faculty/(?P<Department_id>\d+)/$',views.add_faculty,name = 'add_faculty'),
	path('student/',views.add_student,name = 'add_student'),
]