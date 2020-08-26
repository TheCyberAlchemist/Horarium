from django.urls import path

from .views import *

urlpatterns = [
    path('login/',login_page,name = "login"),
    path('logout',logout_user,name = "logout"),
    path('register/',register,name = "register"),
]
