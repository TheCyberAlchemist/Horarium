from django.contrib import admin
from django.urls import path
from . import views,user_dash,add_update_users
from django.conf.urls import url
import faculty_V1.views as faculty_view
urlpatterns = [
	
	path(r'home/',views.admin_home,name = 'admin_home'),

	url(r'^home/get_student_user_ajax/$',user_dash.student_user_table.as_view(),name = 'student_user_display'),
	url(r'^home/get_faculty_user_ajax/$',user_dash.faculty_user_table.as_view(),name = 'faculty_user_display'),
	url(r'^home/faculty_feedback/api/$',faculty_view.ChartData.as_view(),name = 'admin_faculty_feedback_api'),

	path('home/faculty_edit_called/',add_update_users.faculty_edit_called,name = "faculty_edit"),

	path('home/student_edit_called/',add_update_users.student_edit_called,name = "student_edit"),
	
	path('home/update_student/',add_update_users.student_edit_called,name = "student_edit"),

	url(r'^home/faculty_feedback/(?P<Faculty_id>\d+)$',faculty_view.faculty_feedback,name = 'faculty_feedback'),

	url(r'^form/$',views.show_form,name = 'show_form'),

	url(r'^department/$',views.show_department,name = 'show_department'),
	url(r'^department/(?P<Department_id>\d+)/$',views.show_department,name = 'update_department'),

	url(r'^resource/$',views.show_resource,name = 'show_resource'),
	url(r'^resource/(?P<Resource_id>\d+)/$',views.show_resource,name = 'update_resource'),

	url(r'^branch/(?P<Department_id>\d+)/$',views.show_branch,name = 'show_branch'),
	url(r'^branch/(?P<Department_id>\d+)/(?P<Branch_id>\d+)/$',views.show_branch,name = 'update_branch'),
	
	url(r'^semester/(?P<Branch_id>\d+)/$',views.show_semester,name = 'show_semester'),
	url(r'^semester/(?P<Branch_id>\d+)/(?P<Semester_id>\d+)/$',views.show_semester,name = 'update_semester'),
	
	url(r'^division/(?P<Semester_id>\d+)/$',views.show_division,name = 'show_division'),
	url(r'^division/(?P<Semester_id>\d+)/(?P<Division_id>\d+)/$',views.show_division,name = 'update_division'),
	
	url(r'^batch/(?P<Division_id>\d+)/$',views.show_batch,name = 'show_batch'),
	url(r'^batch/(?P<Division_id>\d+)/(?P<Batch_id>\d+)/$',views.show_batch,name = 'update_batch'),
	
	url(r'^table/(?P<Division_id>\d+)/$',views.show_table,name = 'show_table'),
	url(r'^not_avail/(?P<Faculty_id>\d+)/$',views.show_not_avail,name = 'show_not_avail'),

	url(r'^shift/(?P<Department_id>\d+)/$',views.show_shift,name = 'show_shift'),
	url(r'^shift/(?P<Department_id>\d+)/(?P<Shift_id>\d+)/$',views.show_shift,name = 'update_shift'),
	
	url(r'^slot/(?P<Shift_id>\d+)/$',views.show_slot,name = 'show_slot'),
	

	url(r'^faculty/(?P<Department_id>\d+)/$',views.add_faculty,name = 'add_faculty'),
	url(r'^faculty/(?P<Department_id>\d+)/(?P<Faculty_id>\d+)/$',views.add_faculty,name = 'update_faculty'),

	path('student/',views.add_student,name = 'add_student'),

	url(r'^sub/(?P<Branch_id>\d+)/$',views.show_sub_det,name = 'show_sub_det'),
	url(r'^sub/(?P<Branch_id>\d+)/(?P<Subject_id>\d+)/$',views.show_sub_det,name = 'update_sub_det'),

	url(r'^sub_event/(?P<Subject_id>\d+)/$',views.show_sub_event,name = 'show_sub_event'),
	url(r'^sub_event/(?P<Subject_id>\d+)/(?P<Faculty_id>\d+)/$',views.show_sub_event,name = 'update_sub_event'),

	url(r'^table/(?P<Division_id>\d+)/algo/$',views.algo_v1,name = 'algo'),
	# url("/algo",views.algo_v1,name = "algo"),
	# path('sub/',views.show_sub_det,name = 'show_sub_det'),
	# path('sube/',views.show_subject_events, name = 'show_subject_events')
	
	# path('500/',views.error_500_view,name = '500'),
]