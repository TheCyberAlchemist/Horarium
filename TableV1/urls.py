from django.urls import path

from .views import *

urlpatterns = [
    path('table',view_table.as_view(),name = "table")
]
