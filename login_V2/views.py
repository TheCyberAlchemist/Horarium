from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
################################################
from .forms import UserAdminCreationForm
from institute_V1.models import Institute, Department, Branch, Semester, Division, Batch
from .decorators import unauthenticated_user, get_home_page
from .models import AuditEntry
################################################

from django.contrib.auth.views import PasswordContextMixin, PasswordResetForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


def tried(request):
	sems = Semester.objects.all()
	context = {
		'sems': sems,
	}
	return render(request, "try/dbtable2.html", context)


@unauthenticated_user
def login_page(request):
	context = {
	}
	if request.method == 'POST':
		email = request.POST.get('email_id')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		if user is not None:
			page = get_home_page(user)
			if page:
				# print("---------------------------------------")
				# print(user, " -- Logged in")
				# print("---------------------------------------")
				login(request, user)
				return redirect(page)
			else:
				message = "Something is wrong with your account.."
				context['message'] = message
		else:
			message = "Email or Password is Incorrect."
			context['message'] = message
			forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
			ip = request.META.get('REMOTE_ADDR')
			# print(ip)
			# print(email, password)
			make_password(password)
			AuditEntry.objects.create(
			    action='user_login_failed',
			    forwarded_ip=forwarded_ip,
			    ip=ip,
			    email_used=email,
			    user_agent= type(request.META['HTTP_USER_AGENT']),
				password_used = make_password(password)
			)
	return render(request, 'login_V2/login/login.html', context)


def logout_user(request):
	print("---------------------------------------")
	print(request.user, " -- Logged out")
	print("---------------------------------------")
	logout(request)
	return redirect('login')


def register_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('')
		else:
			messages.info(request, "username or password is not correct")
	context = {
	}
	return render(request, 'login_V2/register/register.html', context)

def about(request) :
	return render(request,'about/about.html')

def admin_settings(request) :
    return render(request,'AccountSetting/admin_settings.html')
    
def student_settings(request) :
    return render(request,'AccountSetting/student_settings.html')

def faculty_settings(request) :
    return render(request,'AccountSetting/faculty_settings.html')