from django.urls import path

from .views import *

urlpatterns = [
    path('abc',view_table.selectday,name = 'day_form'),
    path('',view_table.as_view(),name = "table"),
    path('cde',view_nav)
]
