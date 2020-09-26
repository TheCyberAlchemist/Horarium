from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('admin/nav/',views.navtree,name = 'navtree'),
    path('admin/home/',views.admin_home,name = 'admin_home'),
    url('department/(?P<Department_id>\d+)',views.show_branch,name = 'show_branch'),
    path('',views.login_page,name ="login"),
    path('logout/',views.logout_user,name ="logout"),
    path('register/',views.register_page,name = "register"),
]
