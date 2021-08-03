from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.student_home,name = 'student_home'),
	path('settings/',views.student_settings,name="student_settings"),
	path('gg/',views.sendMail,name = 'gg'),
	re_path('home/get_mandatory_subjects/',views.get_all_subjects_of_feedback_type,name="mandatory_subjects"),
	re_path('home/fill_mandatory_feedback',views.fill_mandatory_feedback,name="fill_mandatory_feedback"),

	re_path('home/get_put_sticky_notes/',views.get_put_sticky_notes,name="get_put_sticky_notes"),
	re_path('home/delete_sticky_notes/',views.delete_sticky_notes,name="delete_sticky_notes"),
]