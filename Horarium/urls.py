"""Horarium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.views.generic import RedirectView
import admin_V1.views as v
from django.conf.urls import handler404, handler500
urlpatterns = [
    path('script/', v.run_script,name = 'run_script'),
    path('admin/', admin.site.urls),
    path('Admin/',include('admin_V1.urls')),
    path('student/',include('student_V1.urls')),
    path('faculty/',include('faculty_V1.urls')),
    path('',include('login_V2.urls')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/site_logo.ico')),
    url(r'^a/(?P<Division_id>\d+)/$',v.algo_v1,name = 'a')
]
handler404 = v.error_404_view
handler500 = v.error_500_view
