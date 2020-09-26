from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
################################################
from .forms import UserAdminCreationForm
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch
from .decorators import unauthenticated_user,get_home_page
################################################

def tried(request):
	sems = Semester.objects.all()
	context = {
		'sems':sems,
	}
	return render(request,"try/dbtable2.html",context)


@unauthenticated_user
def login_page(request):
	context = {
	}
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request,email = email , password = password)
		if user is not None:
			page = get_home_page(user)
			if page:
				login(request, user)
				return redirect(page)
			else:
				message = "Something is wrong with your account.."
				context['message'] = message
		else:
			print("hii")
			message = "Email or Password is Incorrect."
			context['message'] = message
	return render(request,'login_V2/login/login.html',context)


def logout_user(request):
	logout(request)
	return redirect('login')


def register_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username = username , password = password)
		if user is not None:
			login(request, user)
			return redirect('')
		else:
			messages.info(request,"username or password not correct")
	context = {
	}
	return render(request,'login_V2/register/register.html',context)
