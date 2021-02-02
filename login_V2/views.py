from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from login_V2.models import CustomUser as User
from django.contrib.sessions.models import Session
from django.utils import timezone


################################################
from .forms import UserAdminCreationForm
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch
from .decorators import unauthenticated_user,get_home_page

################################################

def get_all_logged_in_users():
	# Query all non-expired sessions
	# use timezone.now() instead of datetime.now() in latest versions of Django
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []
	# Build a list of user ids from that query
	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.get('_auth_user_id', None))
	# Query all logged in users based on id list
	return User.objects.filter(id__in=uid_list)


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
				print("---------------------------------------")
				print(user," -- Logged in")
				print("---------------------------------------")
				print(get_all_logged_in_users())
				login(request, user)
				return redirect(page)
			else:
				message = "Something is wrong with your account.."
				context['message'] = message
		else:
			message = "Email or Password is Incorrect."
			context['message'] = message
	return render(request,'login_V2/login/login.html',context) 


def logout_user(request):
	print("---------------------------------------")
	print(request.user," -- Logged out")
	print("---------------------------------------")
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
