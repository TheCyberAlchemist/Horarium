from django.urls import path
from .views import *

urlpatterns = [
    path('select_days',view_table.selectday,name = 'day_form'),
    path('',view_table.as_view(),name = "table"),
    path('add_event',view_table.add_event,name = 'add_event'),
    # path('cde',view_nav),
]
