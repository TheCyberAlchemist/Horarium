from django.shortcuts import render,redirect
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch
from login_V2.decorators import allowed_users

def return_context(request):
	institute = request.user.admin_details.Institute_id #.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute.id)

	branches = {}
	for department in departments: # for all the departments in the institute
		temp = Branch.objects.filter(Department_id=department.id)	# filter all the branches in the same department
		if temp:	# if temp is not null
			branches[department.id] = temp 	# make a key having department id
											# and value having all the branches related to it

	sems = {}
	for key,values in branches.items():	# for all the key(department) and values(branches)
		for value in values:			# for all the coure in branches
			temp = Semester.objects.filter(Branch_id=value.id)	# find all the sems related to the branch
			if temp:	# if temp is not null
				sems[value.id] = temp		# make a key having branch id
											# and value having all the sems related to it

	divs = {}
	for key,values in sems.items():	# for all the key(branch) and values(sems)
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
		'branches':branches,
		'sems':sems,
		'divs':divs,
		'batches':batches,
	}
	return context

@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
	context = return_context(request)
	return render(request,'admin/homepage/home.html',context)


def show_department(request):
	if request.method == 'POST':
		pass
	context = return_context(request)
	if context['institute']:
		return render(request,"admin/details/department.html",context)
	else:
		raise redirect('/')


def show_branch(request,Department_id):
	if request.method == 'POST':
		pass
	context = return_context(request)
	my_department = Department.objects.get(id = Department_id)
	if context['institute'] == my_department.Institute_id:
		branches = Branch.objects.filter(Department_id=Department_id)
		context['my_branches'] = branches
		context['my_department']= my_department
		return render(request,"admin/details/branch.html",context)
	else:
		return redirect('/')


def show_semester(request,Branch_id):
	if request.method == 'POST':
		pass
	context = return_context(request)
	my_branch = Branch.objects.get(id = Branch_id)
	if context['institute'] == my_branch.Department_id.Institute_id:
		semesters = Semester.objects.filter(Branch_id=Branch_id)
		context['my_semesters'] = semesters
		context['my_branch'] = my_branch
		return render(request,"admin/details/semester.html",context)
	else:
		raise redirect('/')

def show_division(request,Semester_id):
	if request.method == 'POST':
		pass
	context = return_context(request)
	my_semester = Semester.objects.get(id = Semester_id)
	if context['institute'] == my_semester.Branch_id.Department_id.Institute_id:
		divisions = Division.objects.filter(Semester_id=Semester_id)
		context['my_divisions'] = divisions
		context['my_semester'] = my_semester
		return render(request,"admin/details/division.html",context)
	else:
		raise redirect('/')


def show_batch(request,Division_id):
	if request.method == 'POST':
		pass
	context = return_context(request)
	my_division = Division.objects.get(id = Division_id)
	if context['institute'] == my_division.Semester_id.Branch_id.Department_id.Institute_id:
		batches = Batch.objects.filter(Division_id=Division_id)
		context['my_batches'] = batches
		context['my_division'] = my_division
		return render(request,"admin/details/batch.html",context)
	else:
		raise redirect('/')
