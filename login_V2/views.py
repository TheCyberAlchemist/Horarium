from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
################################################
from .forms import UserAdminCreationForm
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch,Admin_details
from .decorators import unauthenticated_user,get_home_page
################################################


def admin_home(request):
	return render(request,'admin/homepage/home.html')


def navtree(request):
	institute = request.user.admin_details.Institute_id #.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute.id)

	courses = {}
	for department in departments: # for all the departments in the institute
		temp = Branch.objects.filter(Department_id=department.id)	# filter all the courses in the same department
		if temp:	# if temp is not null
			courses[department.id] = temp 	# make a key having department id
											# and value having all the courses related to it

	sems = {}
	for key,values in courses.items():	# for all the key(department) and values(courses)
		for value in values:			# for all the coure in courses
			temp = Semester.objects.filter(Branch_id=value.id)	# find all the sems related to the course
			if temp:	# if temp is not null
				sems[value.id] = temp		# make a key having course id
											# and value having all the sems related to it

	divs = {}
	for key,values in sems.items():	# for all the key(course) and values(sems)
		for value in values:			# for all the sem in sems
			temp = Division.objects.filter(Semester_id=value.id)	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				divs[value.id] = temp		# make a key having sem id
											# and value having all the divs related to it

	batches = {}
	for key,values in divs.items():	# for all the key(sem) and values(divs)
		for value in values:			# for all the div in divss
			temp = Batch.objects.filter(Division_id=value.id)	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				batches[value.id] = temp		# make a key having div id
												# and value having all the batches related to it

	context = {
		'institute':institute,
		'departments':departments,
		'courses':courses,
		'sems':sems,
		'divs':divs,
		'batches':batches,
	}
	return render(request,"admin/navtree.html",context)


def show_branch(request,Department_id):
	institute = request.user.admin_details.Institute_id
	if institute.id == Department.objects.get(id = Department_id):
		print("hii")
	courses = Branch.objects.filter(Department_id=Department_id)
	context = {
		'courses':courses,
	}
	return render(request,"admin/details/show_branch.html",context)


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
