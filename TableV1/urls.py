from django.urls import path

from .views import *

urlpatterns = [
    path('',view_table.as_view(),name = "table")
]
