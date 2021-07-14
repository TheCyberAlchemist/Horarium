from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from django.contrib.auth import authenticate,login,logout
from .forms import create_user_form
from .decorators import unauthenticated_user

@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username = username , password = password)
		if user is not None:
			print(user," -- Logged in")
			login(request, user)
			return redirect('/table')
		else:
			messages.info(request,"username or password not correct")
	context = {
	}
	return render(request,'login/login.html',context)


def logout_user(request):
	print(request.user," -- Logged out")
	logout(request)
	return redirect('login')


@unauthenticated_user
def register(request):
	form = create_user_form()
	if request.method == 'POST':
		form = create_user_form(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request,"Account made for " + user)
			return redirect('login')
	context = {'form': form}
	return render(request,'login/register.html',context)

def home(request):
	context = {
	}
	return render(request,'table',context)