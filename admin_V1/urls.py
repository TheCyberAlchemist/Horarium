from django.contrib import admin
from django.urls import path,re_path
from . import views,user_dash,add_update_users,algo3,user_csv
import faculty_V1.views as faculty_view
urlpatterns = [
	re_path(r'^try/$',views.api_try,name = 'try'),

	path(r'home/',views.admin_home,name = 'admin_home'),

	re_path(r'^user_dash/(?P<Department_id>\d+)/$',add_update_users.user_dash,name = 'user_dash'),
	
	re_path(r'^user_dash/(?P<Department_id>\d+)/student_edit_called/$',add_update_users.student_edit_called,name = "student_edit"),
	re_path(r'^user_dash/(?P<Department_id>\d+)/faculty_edit_called/$',add_update_users.faculty_edit_called,name = "faculty_edit"),

	re_path(r'^user_dash/(?P<Department_id>\d+)/update_student/$',add_update_users.add_student,name = "student_edit"),

	re_path(r'^home/get_student_user_ajax/$',user_dash.student_user_table.as_view(),name = 'student_user_display'),
	re_path(r'^home/get_faculty_user_ajax/$',user_dash.faculty_user_table.as_view(),name = 'faculty_user_display'),

	re_path(r'^home/faculty_feedback/(?P<Faculty_id>\d+)$',faculty_view.faculty_feedback,name = 'faculty_feedback'),
    re_path(r'^all_feedbacks/$',views.all_feedbacks,name = 'all_feedbacks'),


    re_path(r'^home2/$',views.home,name = 'home2'),
	re_path(r'^home2/satisfaction$',views.student_satisfaction.as_view(),name = 'student_satisfaction'),


	re_path(r'^department/$',views.show_department,name = 'show_department'),
	re_path(r'^department/(?P<Department_id>\d+)/$',views.show_department,name = 'update_department'),

	re_path(r'^resource/$',views.show_resource,name = 'show_resource'),
	re_path(r'^resource/(?P<Resource_id>\d+)/$',views.show_resource,name = 'update_resource'),

	re_path(r'^branch/(?P<Department_id>\d+)/$',views.show_branch,name = 'show_branch'),
	re_path(r'^branch/(?P<Department_id>\d+)/(?P<Branch_id>\d+)/$',views.show_branch,name = 'update_branch'),
	
    re_path(r'^wef/(?P<Department_id>\d+)/$',views.show_wef,name = 'show_wef'),
	re_path(r'^wef/(?P<Department_id>\d+)/(?P<WEF_id>\d+)/$',views.show_wef,name = 'update_wef'),

	re_path(r'^semester/(?P<Branch_id>\d+)/$',views.show_semester,name = 'show_semester'),
	re_path(r'^semester/(?P<Branch_id>\d+)/(?P<Semester_id>\d+)/$',views.show_semester,name = 'update_semester'),
	
	re_path(r'^division/(?P<Semester_id>\d+)/$',views.show_division,name = 'show_division'),
	re_path(r'^division/(?P<Semester_id>\d+)/(?P<Division_id>\d+)/$',views.show_division,name = 'update_division'),
	
	re_path(r'^batch/(?P<Division_id>\d+)/$',views.show_batch,name = 'show_batch'),
	re_path(r'^batch/(?P<Division_id>\d+)/(?P<Batch_id>\d+)/$',views.show_batch,name = 'update_batch'),
	
	re_path(r'^table/(?P<Division_id>\d+)/$',views.show_table,name = 'show_table'),
	re_path(r'^not_avail/(?P<Faculty_id>\d+)/$',views.show_not_avail,name = 'show_not_avail'),

	re_path(r'^shift/(?P<Department_id>\d+)/$',views.show_shift,name = 'show_shift'),
	re_path(r'^shift/(?P<Department_id>\d+)/(?P<Shift_id>\d+)/$',views.show_shift,name = 'update_shift'),
	
	re_path(r'^slot/(?P<Shift_id>\d+)/$',views.show_slot,name = 'show_slot'),
	

	re_path(r'^faculty/(?P<Department_id>\d+)/$',views.add_faculty,name = 'add_faculty'),
	re_path(r'^faculty/(?P<Department_id>\d+)/(?P<Faculty_id>\d+)/$',views.add_faculty,name = 'update_faculty'),

	path('student/',views.add_student,name = 'add_student'),

	re_path(r'^sub/(?P<Branch_id>\d+)/$',views.show_sub_det,name = 'show_sub_det'),
	re_path(r'^sub/(?P<Branch_id>\d+)/(?P<Subject_id>\d+)/$',views.show_sub_det,name = 'update_sub_det'),

	re_path(r'^sub_event/(?P<Subject_id>\d+)/$',views.show_sub_event,name = 'show_sub_event'),
	re_path(r'^sub_event/(?P<Subject_id>\d+)/(?P<Faculty_id>\d+)/$',views.show_sub_event,name = 'update_sub_event'),

	re_path(r'^table/(?P<Division_id>\d+)/algo/$',views.algo_v1,name = 'algo'),

	re_path(r'^try/algo3/$',algo3.view_func,name = 'view_algo3'),
	re_path(r'^algo3/$',algo3.main.as_view(),name = 'algo3'),

	re_path(r'^csv_upload/$',user_csv.csv_view_func,name = 'csv_upload'),
	re_path(r'^csv/$',user_csv.csv_check_api.as_view(),name = 'csv'),
	
	# re_path("/algo",views.algo_v1,name = "algo"),
	# path('sub/',views.show_sub_det,name = 'show_sub_det'),
	# path('sube/',views.show_subject_events, name = 'show_subject_events')
	# path('500/',views.error_500_view,name = '500'),
]