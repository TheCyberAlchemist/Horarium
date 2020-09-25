from django.shortcuts import render,redirect
################################################
from django.http import HttpResponse
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch
################################################


def navtree(request):
	institute_pk = 1
	institute = Institute.objects.filter(pk=institute_pk)#.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute_pk)

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
	print(batches)

	context = {
		'institute':institute[0],
		'departments':departments,
		'courses':courses,
		'sems':sems,
		'divs':divs,
		'batches':batches,
	}
	return render(request,"login_V2/admin/home.html",context)


def show_branch(request,Department_id):
	courses = Branch.objects.filter(Department_id=Department_id)
	print(courses)
	context = {
		'courses':courses,
	}
	return render(request,"login_V2/admin/show_branch.html",context)


def tried(request):
	sems = Semester.objects.all()
	context = {
		'sems':sems,
	}
	return render(request,"try/dbtable2.html",context)

def login_page(request):
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
	return render(request,'login_V2/login/login.html',context)

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