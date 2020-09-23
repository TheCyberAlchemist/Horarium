from django.urls import path
from .views import navtree,tried

urlpatterns = [
    path('admin/nav/',navtree,name = 'navtree'),
    path('tried/',tried,name = 'try'),
]
