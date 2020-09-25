from django.urls import path
from .views import navtree,show_branch,tried,login_page,register_page
from django.conf.urls import url
urlpatterns = [
    path('admin/nav/',navtree,name = 'navtree'),
    url('department/(?P<Department_id>\d+)',show_branch,name = 'show_branch'),
    # url(r'^User/(?P<userid>\d+)/$', 'search.views.user_detail', name='user_details'),
    path('tried/',tried,name = 'try'),
    path('',login_page,name ="login"),
    path('register/',register_page,name = "register")
]
