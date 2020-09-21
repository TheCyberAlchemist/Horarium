from django.urls import path
from .views import navtree

urlpatterns = [
    path('admin/nav/',navtree,name = 'navtree'),
]
