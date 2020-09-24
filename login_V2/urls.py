from django.urls import path
from .views import navtree,show_branch,tried
from django.conf.urls import url
urlpatterns = [
    path('admin/nav/',navtree,name = 'navtree'),
    url('department/(?P<Department_id>\d+)',show_branch,name = 'show_branch'),
    # url(r'^User/(?P<userid>\d+)/$', 'search.views.user_detail', name='user_details'), 
    path('tried/',tried,name = 'try'),
]
