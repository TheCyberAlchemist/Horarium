from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
################################################
from .forms import UserAdminCreationForm
from institute_V1.models import Institute, Department, Branch, Semester, Division, Batch
from .decorators import unauthenticated_user, get_home_page
from .models import AuditEntry,CustomUser
################################################

from django.contrib.auth.views import PasswordContextMixin, PasswordResetForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def tried(request):
	sems = Semester.objects.all()
	context = {
		'sems': sems,
	}
	return render(request, "try/dbtable2.html", context)


def check_password(password,user):
	'returns array of errors if password not suitable else returns True'
	a = 1
	try:
		a = validate_password(password,user)
	except ValidationError as e:
		return e
	except e:
		return ["Some error occured."]
	if a == None:
		return True
	return ["Some error occured."]

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
			print("Page to redirect :: ",page)
			if page:
				print("---------------------------------------")
				print(user, " -- Logged in")
				print("---------------------------------------")
				login(request, user)
				return redirect(page)
			else:
				message = "Something is wrong with your account.."
				context['message'] = message
	return render(request, 'login_V2/login/login.html', context)

def reset_user_password(request):
	if request.method == 'POST':
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		current_password = request.POST.get('current_password')
		print(request.POST.get('password1'),request.POST.get('password2'))
		if password1 and current_password and password2:
			if password1 == password2 and check_password(current_password,request.user.password):
				print("The passwords are correct")
				pass
				# password changed



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

from django.core.mail import send_mail
def landing(request) :
	if request.method == "POST" and request.is_ajax():
		try:
			name_of_client = request.POST['name']

			subject = f"Contact from {name_of_client} saying '{request.POST['subject']}' "
			
			from_email = request.POST['email']
			message = f"This email address of the client is :: {from_email} \n '{request.POST['message']}'"
			# from_email = "yogeshrathod19@gnu.ac.in"
			# message = request.POST['message']

			send_mail(
				subject, #subject
				message, #message
				from_email, # from email 
				['horarium@tecrave.in'] # to email
			)
			return JsonResponse({"success":"We have heard you. Thank You 😊."})
		except Exception as e:
			return JsonResponse({},status=500)
		
	return render(request,'landingpage/Techie/index.html')

# for i in Institute.objects.using("horarium").all():
#     i.save(using="default")

# for i in  Resource.objects.using("horarium").all():
#     # print(i)
#     i.save(using="default")

# for i in Department.objects.using("horarium").all():
#     print(i)
#     # i.save(using="default")
#     # print(f"Saved :: {i}")
# for i in WEF.objects.using("horarium").all():
#     print(i)
#     # i.save(using="default")
#     # print(f"Saved :: {i}")

# from django.contrib.contenttypes.models import ContentType
# auth_app = [ct.model_class() for ct in ContentType.objects.filter(app_label="auth")]
# g = auth_app[0]
# for i in g.objects.using("horarium").all():
# 	print(i)
# 	i.save(using="default")

# ContentType.objects.filter(app_label="auth")
# login_app = [ct.model_class() for ct in ContentType.objects.filter(app_label="login_V2")]
# for i in login_app:
# 	for j in i.objects.using("horarium").all():
# 		j.save(using='default')