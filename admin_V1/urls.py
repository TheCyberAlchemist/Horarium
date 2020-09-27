from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
	path('home/',views.admin_home,name = 'admin_home'),
	path('nav/',views.navtree,name = 'navtree'),
	url('branch/(?P<Department_id>\d+)',views.show_branch,name = 'show_branch'),
    # path('admin/home',),
]