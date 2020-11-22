from django.shortcuts import render,redirect
from django.http import HttpResponse
from login_V2.decorators import allowed_users
from django.contrib import messages
import json
from django.db import IntegrityError
from django.core import serializers


from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch,Shift,Working_days,Timings,Slots
from .forms import create_branch,create_department,create_semester,create_division,create_division,create_batch
from .forms import add_user,faculty_details,faculty_load,student_details
from .forms import slot,shift
from faculty_V1.models import Faculty_designation

def return_context(request):
	institute = request.user.admin_details.Institute_id #.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute.id).order_by('name')

	shifts = {}
	branches = {}
	for department in departments: # for all the departments in the institute
		temp = Branch.objects.filter(Department_id=department.id).order_by('name')	# filter all the branches in the same department
		if temp:	# if temp is not null
			print(temp)
			branches[department.id] = temp 	# make a key having department id
											# and value having all the branches related to it
		temp_shift = Shift.objects.filter(Department_id=department.id).order_by('name')	# filter all the branches in the same department
		if temp_shift:
			print(temp_shift)
			shifts[department.id] = temp_shift	# make a key having department id
												# and value having all the shifts related to it
				

	sems = {}
	for key,values in branches.items():	# for all the key(department) and values(branches)
		for value in values:			# for all the coure in branches
			temp = Semester.objects.filter(Branch_id=value.id).order_by('short')	# find all the sems related to the branch
			if temp:	# if temp is not null
				sems[value.id] = temp		# make a key having branch id
											# and value having all the sems related to it

	divs = {}
	for key,values in sems.items():	# for all the key(branch) and values(sems)
		for value in values:			# for all the sem in sems
			temp = Division.objects.filter(Semester_id=value.id).order_by('name')	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				divs[value.id] = temp		# make a key having sem id
											# and value having all the divs related to it

	batches = {}
	for key,values in divs.items():	# for all the key(sem) and values(divs)
		for value in values:			# for all the div in divss
			temp = Batch.objects.filter(Division_id=value.id).order_by('name')	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				batches[value.id] = temp		# make a key having div id
												# and value having all the batches related to it

	context = {
		'institute':institute,
		'departments':departments,
		'branches':branches,
		'shifts':shifts,
		'sems':sems,
		'divs':divs,
		'batches':batches,
	}
	return context


def delete_entries(qs,data):
	for d in data:
		print("p1")
		qs.get(id = int(d)).delete()
		# pass


@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
	context = return_context(request)
	return render(request,'admin/homepage/home.html',context)


def show_department(request,Department_id = None):
	context = return_context(request)
	if context['institute']:	# Check if the user is in the same institute as the urls
		context['form'] = create_department()
		if Department_id:	# if edit is called
			edit = context['departments'].get(pk = Department_id)
			form = create_department(instance = edit)
			context['u_name'] = form.instance.name
			context['u_short'] = form.instance.short
		if request.method == 'POST':
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(context['departments'],data)
			else:
				if Department_id:
					form = create_department(request.POST,instance=edit)
				else:
					form = create_department(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Institute_id = context['institute']
					try:	# unique contraint added
						candidate.save()
						context['form'] = create_department()     			#Form Renewed
						return redirect('show_department')                  #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Short and Name must be unique for Institute"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/department.html",context)
	else:
		return redirect('/')


def show_semester(request,Branch_id,Semester_id = None):
	context = return_context(request)
	my_branch = Branch.objects.get(id = Branch_id)
	if context['institute'] == my_branch.Department_id.Institute_id:	# Check if the user is in the same institute as the urls
		semesters = Semester.objects.filter(Branch_id=Branch_id).order_by('short')
		context['form'] = create_semester()
		if Semester_id:	# if edit is called
			edit = semesters.get(pk=Semester_id)
			form = create_semester(instance = edit)
			context['u_short'] = form.instance.short

		context['my_semesters'] = semesters
		context['my_branch'] = my_branch
		if request.method == 'POST':	# if create is submitted
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(semesters,data)
			else:
				if Semester_id:	# if edit 
					form = create_semester(request.POST, instance=edit) 
				else:
					form = create_semester(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Branch_id = my_branch
					try:	# unique contraint added
						candidate.save()
						context['form'] = create_semester()     				#Form Renewed
						return redirect('show_semester',Branch_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Short must be unique for Branch"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/semester.html",context)
	else:
		raise redirect('/')


def show_division(request,Semester_id,Division_id = None):
	context = return_context(request)
	my_semester = Semester.objects.get(id = Semester_id)
	if context['institute'] == my_semester.Branch_id.Department_id.Institute_id:	# Check if the user is in the same institute as the urls
		divisions = Division.objects.filter(Semester_id=Semester_id).order_by('name')
		context['form'] = create_division()
		if Division_id:	# if edit is called
			edit = divisions.get(pk=Division_id)
			form = create_division(instance = edit)
			context['u_name'] = form.instance.name
		context['my_divisions'] = divisions
		context['my_semester'] = my_semester
		if request.method == 'POST':
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(divisions,data)
			else:
				if Division_id:	# if edit 
					form = create_division(request.POST, instance=edit) 
				else:
					form = create_division(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Semester_id = my_semester
					# candidate.Shift_id = 
					try:	# unique contraint added
						candidate.save()
						context['form'] = create_division()     				#Form Renewed
						return redirect('show_division',Semester_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Division Name is Unique for Semester"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/division.html",context)
	else:
		raise redirect('/')


def show_batch(request,Division_id,Batch_id = None):
	context = return_context(request)
	my_division = Division.objects.get(id = Division_id)
	if context['institute'] == my_division.Semester_id.Branch_id.Department_id.Institute_id:
																		# Check if the user is in the same institute as the urls
		batches = Batch.objects.filter(Division_id=Division_id).order_by('name')
		context['form'] = create_division()
		if Batch_id:	# if edit is called
			edit = divisions.get(pk=Batch_id)
			form = create_batch(instance = edit)
			context['u_name'] = form.instance.name
		context['my_batches'] = batches
		context['my_division'] = my_division
		if request.method == 'POST':
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(batches,data)
			else:
				if Batch_id:	# if edit 
					form = create_batch(request.POST, instance=edit) 
				else:
					form = create_batch(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Division_id = my_division
					try:	# unique contraint added
						candidate.save()
						context['form'] = create_batch()     				#Form Renewed
						return redirect('show_batch',Division_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Name must be unique for Division"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/batch.html",context)
	else:
		raise redirect('/')


def add_faculty(request,Department_id=None):
	context = return_context(request)
	context['user_form'] = add_user()
	context['faculty_detail_form'] = faculty_details()
	context['faculty_load_form'] = faculty_load()
	context['shifts'] = Shift.objects.filter(Department_id=Department_id)
	department = Department.objects.get(pk = Department_id)
	context['designations'] = Faculty_designation.objects.filter(Institute_id=department.Institute_id) | Faculty_designation.objects.filter(Institute_id=None)
	# context['designations'] = Faculty_designation.objects.filter(Department_id__in=[None])
	if request.method == 'POST':
		user_form = add_user(request.POST)
		faculty_detail_form = faculty_details(request.POST)
		faculty_load_form = faculty_load(request.POST)
		print(request.POST)
		if user_form.is_valid() and faculty_detail_form.is_valid() and faculty_load_form.is_valid():
			# print("all done")
			user = user_form.save()
			###########
			A = faculty_detail_form.save(commit = False)
			A.Institute_id = context['institute']
			A.User_id = user
			F = A.save()
			#############
			B = faculty_load_form.save(commit = False)
			B.Faculty_id = F
			B.save()

		else:
			context['errors'] = [user_form.errors,faculty_detail_form.errors,faculty_load_form.errors]
			
		
	return render(request,"admin/faculty/faculty_details.html",context)


def add_student(request):
	context = return_context(request)
	context['user_form'] = add_user()
	context['student_detail_form'] = student_details()
	if request.method == "POST":
		user_form = add_user(request.POST)
		student_detail_form = student_details(request.POST)
		if user_form.is_valid() and student_detail_form.is_valid():
			user = user_form.save()
			#########################
			A = student_detail_form.save(commit=False)
			A.User_id = user
			A.Institute_id = context['institute']
			A.save()

			
	return render(request,"admin/student/add_student.html",context)


def show_slot(request,Shift_id=None):
	context = return_context(request)
	my_shift = Shift.objects.get(pk = Shift_id)
	context["my_shift"] = my_shift

	if request.method == 'POST':
		data = json.loads(request.body)	# data is the json object returned after savings
		# print(data)
		Timings.objects.all().delete()
		check_all = True
		for dictonary in data:
			# print(dictonary)
			form = slot(dictonary)
			if form.is_valid():
				print(form.is_valid())
				candidate = form.save(commit=False)
				candidate.Shift_id = my_shift
				candidate.save()
			else:
				check_all = False
				break
		if check_all:	# is all the data is clean
			for day in Working_days.objects.all():
				for time in Timings.objects.all():
					Slots.objects.create(day=day.Days_id,Timing_id=time)
		redirect('show_slot',Shift_id)

	context['form'] = slot()
	SomeModel_json = serializers.serialize("json", Timings.objects.all())
	data = json.loads(SomeModel_json)
	for d in data:
		del d['pk']
		del d['model']
	data = json.dumps(data)
	print(data)
	context['old_data'] = data
	return render(request,"admin/details/slot.html",context)


def show_branch(request,Department_id,Branch_id=None):
	context = return_context(request)
	my_department = Department.objects.get(id = Department_id)
	if context['institute'] == my_department.Institute_id:	# Check if the user is in the same institute as the urls
		context['form'] = create_branch()
		branches = Branch.objects.filter(Department_id=Department_id).order_by('name')
		context['my_branches'] = branches
		context['my_department']= my_department

		if Branch_id:	# if edit is called
			edit = branches.get(pk=Branch_id)
			form = create_branch(instance = edit)

			context['u_name'] = form.instance.name
			context['u_short'] = form.instance.short

		if request.method == 'POST':	# if create is submitted
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(branches,data)
			else:
				if Branch_id:
					form = create_branch(request.POST,instance=edit)
				else:
					form = create_branch(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Department_id = my_department
					candidate.save()
					try:	# unique contraint added
						candidate.save()
						context['form'] = create_branch()     				#Form Renewed
						return redirect('show_branch',Department_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Name and Short must be unique for Department"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/branch.html",context)
	else:
		return redirect('/')


def show_shift(request,Department_id,Shift_id = None):
	context = return_context(request)
	my_department = Department.objects.get(id = Department_id)
	print(context['shifts'])
	if context['institute'] == my_department.Institute_id:	# Check if the user is in the same institute as the urls
		context['form'] = shift()
		context['my_department']= my_department
		context['my_shifts'] = Shift.objects.filter(Department_id=context['my_department'].id)
		if Shift_id:	# if edit is called
			edit = Shift.objects.get(id=Shift_id)
			form = shift(instance = edit)

			context['u_name'] = form.instance.name
			context['u_start_time'] = form.instance.start_time
			context['u_end_time'] = form.instance.end_time
			
		if request.method == 'POST':	# if create is submitted
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(context['shifts'],data)
			else:
				if Shift_id:
					form = shift(request.POST,instance=edit)
				else:
					form = shift(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Department_id = my_department
					candidate.save()
					try:	# unique contraint added
						candidate.save()
						context['form'] = shift()     				#Form Renewed
						return redirect('show_shift',Department_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Shift Name must be unique for Department"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
			return render(request,"admin/details/shift.html",context)
	else:
		return redirect('/')

	return render(request,"admin/details/shift.html",context)