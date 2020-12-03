from django.shortcuts import render,redirect
from django.http import HttpResponse
from login_V2.decorators import allowed_users
from django.contrib import messages
import json
from django.db import IntegrityError
from django.core import serializers


from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch,Shift,Working_days,Timings,Slots
from subject_V1.models import Subject_details,Subject_event
from .forms import create_branch,create_department,create_semester,create_division,create_division,create_batch
from .forms import add_user,faculty_load,faculty_details,student_details
from .forms import slot,shift
from faculty_V1.models import Faculty_designation,Can_teach,Faculty_details,Faculty_load,Not_available
from Table_V2.models import Event


def return_context(request):
	institute = request.user.admin_details.Institute_id #.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute.id).order_by('name')

	shifts = {}
	branches = {}
	for department in departments: # for all the departments in the institute
		temp = Branch.objects.filter(Department_id=department.id).order_by('name')	# filter all the branches in the same department
		if temp:	# if temp is not null
			branches[department.id] = temp 	# make a key having department id
											# and value having all the branches related to it
		temp_shift = Shift.objects.filter(Department_id=department.id).order_by('name')	# filter all the branches in the same department
		if temp_shift:
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
		qs.get(id = int(d)).delete()


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
						context['integrityErrors'] = "*Short Name and Name must be unique for Institute*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors.as_text()
					print(context['errors'])
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
						context['integrityErrors'] = "*Short must be unique for Branch*"   #errors to integrityErrors
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
						context['integrityErrors'] = "*Division Name is Unique for Semester*"   #errors to integrityErrors
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
						context['integrityErrors'] = "*Name must be unique for Division*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/batch.html",context)
	else:
		raise redirect('/')


def add_faculty(request,Department_id,Faculty_id=None):
	context = return_context(request)
	if context['institute']:
		department = Department.objects.get(pk = Department_id)
		context['my_department'] = department
		context['my_branches'] = Branch.objects.filter(Department_id=department)
		context['my_sems'] = Semester.objects.filter(Branch_id=1)
		context['my_subjects'] = Subject_details.objects.filter(Semester_id__in=context['my_sems'])
		context['my_shifts'] = Shift.objects.filter(Department_id=Department_id)
		context['designations'] = Faculty_designation.objects.filter(Institute_id=department.Institute_id) | Faculty_designation.objects.filter(Institute_id=None)
		context['refresh'] = False
		context['faculty'] = Faculty_details.objects.filter(Department_id=Department_id)

		if Faculty_id:	# if edit is called
			edit = context['faculty'].get(pk = Faculty_id)
			user_form = add_user(instance = edit.User_id)
			faculty_detail_form = faculty_details(instance = edit)
			faculty_load_form = faculty_load(instance=Faculty_load.objects.get(Faculty_id=edit))
			abc = Can_teach.objects.filter(Faculty_id=edit)
			context['update'] = [user_form.instance,
								faculty_detail_form.instance,
								faculty_load_form.instance,
								list(i.Subject_id.pk for i in abc)
							]
			if request.method == 'POST':
				request.POST = request.POST.copy()
				request.POST['email'] = edit.User_id.email
				user_form = add_user(request.POST,instance = edit.User_id)
				faculty_detail_form = faculty_details(request.POST,instance = edit)
				faculty_load_form = faculty_load(request.POST,instance=Faculty_load.objects.get(Faculty_id=edit))
				# print(faculty_detail_form.is_valid(),faculty_load_form.is_valid(),user_form.is_valid())
				subjects = request.POST.getlist('subject')
				can_teach = []
				for subject in subjects:
					try :
						can_teach.append(Can_teach.objects.create(Faculty_id = edit,Subject_id=context['my_subjects'].get(pk = subject)))
					except:
						context['integrityErrors'] = "We have encountered some problem refresh the page"   #errors to integrityErrors
						context['refresh'] = True
						break
				if not context['refresh']:
					for i in can_teach:
						i.save()
					user_form.save()
					faculty_detail_form.save()
					faculty_load_form.save()
				else :
					pass
				return redirect('/')

		if request.method == 'POST':
			user_form = add_user(request.POST)
			faculty_detail_form = faculty_details(request.POST)
			faculty_load_form = faculty_load(request.POST)
			# print(user_form.is_valid(),faculty_detail_form.is_valid(),faculty_load_form.is_valid())
			# print(user_form.errors)
			if user_form.is_valid() and faculty_detail_form.is_valid() and faculty_load_form.is_valid():
				from django.contrib.auth.models import Group
				group = Group.objects.get(name='Faculty')
				user = user_form.save(commit = False)
				user.save()
				user.groups.add(group)
				###########
				A = faculty_detail_form.save(commit = False)
				A.Department_id = Department.objects.get(id = Department_id)
				A.User_id = user
				A.save()
				#############
				B = faculty_load_form.save(commit = False)
				B.Faculty_id = A
				subjects = request.POST.getlist('subject')
				can_teach = []
				B.save()

				for subject in subjects:
					try :
						can_teach.append(Can_teach.objects.create(Faculty_id = A,Subject_id=context['my_subjects'].get(pk = subject)))
					except:
						context['integrityErrors'] = "We have encountered some problem refresh the page"   #errors to integrityErrors
						context['refresh'] = True
						break
				if not context['refresh']:
					for i in can_teach:
						i.save()
				else:
					user.delete()
			else:
				context['errors'] = [user_form.errors,faculty_detail_form.errors,faculty_load_form.errors]
	else:
		return redirect('/')
		
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


def get_json(qs,keep_pk=True):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		if not keep_pk:
			del d['pk']
		del d['model']
	return json.dumps(data)


def show_slot(request,Shift_id=None):
	context = return_context(request)
	my_shift = Shift.objects.get(pk = Shift_id)
	context["my_shift"] = my_shift
	context['old_data'] = get_json(Timings.objects.filter(Shift_id = Shift_id))
	context['working_days'] = Working_days.objects.filter(Shift_id=my_shift).order_by("Days_id")
	if request.method == 'POST':
		# print(request.body,"hii")
		data = json.loads(request.body)	# data is the json object returned after savings
		check_all = True
		timing = data['slots'];
		days = data['days']
		old_days = set(context['working_days'].values_list("id",flat=True))
		new_days = set(i for i in range(int(days[0]),int(days[1])+1))
		to_be_deleted = old_days.difference(new_days)
		to_be_saved = new_days.difference(old_days)
		for i in to_be_deleted:
			print(Working_days.objects.get(Days_id=i)," - deleted")
		for i in to_be_saved:
			print(Working_days.objects.create(Shift_id=my_shift,Days_id_id=i)," - added")

		print(new_days,old_days)
		for dictonary in timing:
			if dictonary["id"] :	# if already present
				edit = Timings.objects.get(pk=int(dictonary["id"]))
				form = slot(dictonary,instance = edit)
				if form.is_valid():
					form.save()
				else:
					check_all = False
					break
			else:
				form = slot(dictonary)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Shift_id = my_shift
					candidate.save()
					for day in Working_days.objects.filter(Shift_id=Shift_id):
						Slots.objects.create(day=day.Days_id,Timing_id=candidate)
				else:
					check_all = False
					break
		# if check_all:	# is all the data is clean
		# 		for time in Timings.objects.all():
		return redirect('show_slot',Shift_id)		
	
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
						context['integrityErrors'] = "*Name and Short must be unique for Department*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/branch.html",context)
	else:
		return redirect('/')


def show_shift(request,Department_id,Shift_id = None):
	context = return_context(request)
	my_department = Department.objects.get(id = Department_id)
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
						context['integrityErrors'] = "*Shift Name must be unique for Department*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
			return render(request,"admin/details/shift.html",context)
	else:
		return redirect('/')

	return render(request,"admin/details/shift.html",context)


def show_table(request,Division_id):
	if request.method == "POST":
		print(json.loads(request.body))
		if request.is_ajax():
			pass
		redirect('show_table',Division_id)
	# context = return_context(request)
	my_division = Division.objects.get(pk = Division_id)
	Shift_id = my_division.Shift_id
	subjects = Subject_details.objects.filter(Semester_id=my_division.Semester_id)
	timings = Timings.objects.filter(Shift_id = Shift_id)
	context = {
		'working_days' : Working_days.objects.filter(Shift_id = Shift_id),
		'timings' : timings,
		'slots_json' : get_json(Slots.objects.filter( Timing_id__in = timings)),
		'subject_events' : Subject_event.objects.filter(Subject_id__in=subjects),
	}
	return render(request,"try/table.html",context)


def show_not_avail(request,Faculty_id):
	def get_slots(qs):
		return Slots.objects.filter(pk__in = qs.values("Slot_id"))
	faculty = Faculty_details.objects.get(pk = Faculty_id)
	context["my_department"] = faculty.Department_id
	events = Event.objects.filter(Subject_event_id__in = Subject_event.objects.filter(Faculty_id = Faculty_id))
	not_available = Not_available.objects.filter(Faculty_id=Faculty_id)
	Shift_id = faculty.Shift_id
	context = {}
	context['working_days'] = Working_days.objects.filter(Shift_id = Shift_id)
	context['timings'] = Timings.objects.filter(Shift_id = Shift_id)
	context['slots_json'] = get_json(Slots.objects.filter( Timing_id__in = context['timings']))
	context['events'] = get_json(get_slots(events),False)
	context['not_available'] = get_json(get_slots(not_available),False)

	if request.method == "POST":
		# print(json.loads(request.body))
		if request.is_ajax():
			slot_ids = json.loads(request.body)
			old_data = set(get_slots(not_available).values_list("id",flat = True))
			new_data = set(slot_ids)
			to_be_deleted = old_data.difference(new_data)
			to_be_added = new_data.difference(old_data)
			print(to_be_added,to_be_deleted)
			for i in to_be_deleted:
				print("deleted - ",Not_available.objects.get(Slot_id_id = i))
				Not_available.objects.get(Slot_id_id=i).delete()
			for i in to_be_added:
				Not_available.objects.create(Faculty_id_id=Faculty_id,Slot_id_id=i).save()
				# print("added - ",Slots.objects.get(pk = i))
		redirect('show_not_avail',Faculty_id = Faculty_id)


	return render(request,"admin/details/not_available.html",context)


def show_sub_det(request): 
	return render(request,"admin/details/subject_details.html")