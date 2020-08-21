from django.urls import path

from .views import *

urlpatterns = [
    path('table',view_table,name = "table")
]
