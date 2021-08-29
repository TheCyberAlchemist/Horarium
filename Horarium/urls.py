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
from django.urls import path,include,re_path
# from django.conf.urls import re_path
from django.views.generic import RedirectView

from django.conf.urls.static import static
from django.conf import settings

import admin_V1.views as v
import institute_V1.views as iv
import student_V1.views as sv
import faculty_V1.views as fv
import login_V2.views as lv
from django.conf.urls import handler404, handler500

from django.contrib.auth import views as auth_views

urlpatterns = [
    ##### try #####
    path('script/', v.run_script,name = 'run_script'),
    path('try/',sv.add_student,name='try'),
    path('tryopen/',iv.open_try,name='open_try'),
    ##### defaults #####
    path('',include('login_V2.urls')),
    path('Admin/',include('admin_V1.urls')),
    path('student/',include('student_V1.urls')),
    path('faculty/',include('faculty_V1.urls')),
	path('reset_user_password/',lv.reset_user_password,name='reset_user_password'),
	
	path('reset_password',auth_views.PasswordResetView.as_view(template_name="2.html"), name="reset_password_setting"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="login_V2/ForgotPassword/forgot_email_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="login_V2/ForgotPassword/forgot_password.html"), name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="login_V2/ForgotPassword/password_reset_complete.html"), name="password_reset_complete"),
    ##### feedback apis #####
    re_path(r'api/\Z', fv.feedback.as_view()),
    re_path(r'mandatory/\Z', fv.mandatory_feedbacks.as_view()),
    re_path(r'ave_all/\Z', fv.average_all_questions.as_view()),

	re_path(r'get_put_sticky_notes/\Z',sv.get_put_sticky_notes,name="get_put_sticky_notes"),
	re_path(r'delete_sticky_notes/\Z',sv.delete_sticky_notes,name="delete_sticky_notes"),

    ##### system #####
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$',RedirectView.as_view(url='/static/site_logo.ico')),
    path('media/<path:relative_path>', iv.DocumentDownload, name='document-download'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = v.error_404_view
handler500 = v.error_500_view
