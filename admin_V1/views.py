from django.shortcuts import render,redirect
from django.http import HttpResponse
from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.db import IntegrityError
from django.core import serializers


from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch,Shift,Working_days,Timings,Slots,Resource
from subject_V1.models import Subject_details,Subject_event
from .forms import create_branch,create_department,create_semester,create_division,create_division,create_batch
from .forms import add_user,faculty_load,faculty_details,student_details
from .forms import timing,shift,add_resource,add_subject_details,add_sub_event,update_sub_event
from .forms import add_event
from faculty_V1.models import Faculty_designation,Can_teach,Faculty_details,Faculty_load,Not_available
from Table_V2.models import Event


############# For running any scripts ###############
def run_script(request):
	var = []
	# for i in Event.objects.all():
	# 	if i.Slot_id_2:
	# 		i.link = i.Batch_id.link
	# 		i.save()
	# 		print(i.link,"- is prac")
	# 	else:
	# 		i.link = i.Division_id.link
	# 		i.save()
	# 		print(i.link,"- is lect")
	# 	if i.Subject_event_id.Subject_id.name == "Web Application Development":
	# 		i.link = "https://bkvlearningsystemsprivatelimited.my.webex.com/webappng/sites/bkvlearningsystemsprivatelimited.my/meeting/download/0e59b41ffacf437ab0f338df7ce7d06d?siteurl=bkvlearningsystemsprivatelimited.my&MTID=mfdda13a691e94f89c950540d20160085"
	# 		i.save()
	# 	pass

	# for i in Batch.objects.all():		
	# 	for j in Subject_details.objects.filter(Semester_id = i.Division_id.Semester_id):
	# 		i.subjects_for_batch.add(j)
	# 	# # i.subjects_for_batch.remove(Subject_details.objects.filter())
	# 	i.save()
		# break
	for j in Subject_details.objects.all():
		print(j.get_prac_lect())
		break
	return HttpResponse(Subject_details.objects.first())

############# Returns data for navigation tree #############
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

############# deletes the objects in the data list from qs #############
def delete_entries(qs,data):
	for d in data:
		qs.get(pk = d).delete()


def get_json(qs,keep_pk=True,event = False,time_table = False,my_division=0,time_table_event = False):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		if event:
			d['fields']['day'] = qs.filter(day = d['fields']['day'])[0].day.Days_id_id
		elif time_table_event:
			d['fields']['day'] = qs.filter(day = d['fields']['day'])[0].day.Days_id_id
			# print(Event.objects.filter(Slot_id_id=d['pk']).values_list("id",flat=True))
			d['fields']['resources_filled'] = list(Event.objects.filter(Slot_id_id=d['pk']).values_list("Resource_id",flat=True).exclude(Division_id=my_division))
		elif time_table:
			d['fields']['Subject_color'] = qs.filter(Subject_id=d['fields']['Subject_id'])[0].Subject_id.color
			d['fields']['Faculty_name'] = str(qs.filter(pk = d['pk'])[0].Faculty_id)
			d['fields']['Subject_id'] = str(qs.filter(Subject_id=d['fields']['Subject_id'])[0].Subject_id)
			d['fields']['not_available'] = list(Not_available.objects.filter(Faculty_id=d['fields']['Faculty_id']).values_list("Slot_id",flat=True))
			d['fields']['other_events'] = get_json(Event.objects.filter(Subject_event_id__Faculty_id = d['fields']['Faculty_id']).exclude(Division_id=my_division),my_division=my_division,keep_pk=False)
		if not keep_pk:
			del d['pk']
		del d['model']
	if not time_table and my_division and not time_table_event:		# if it is called by recursion 
		for d in data:
			d['fields']['Division_id'] = str(Division.objects.get(pk = d['fields']['Division_id']))
		return data
	return json.dumps(data)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
	context = return_context(request)
	return render(request,'admin/homepage/home.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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
		return redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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
		raise redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_division(request,Semester_id,Division_id = None):
	context = return_context(request)
	my_semester = Semester.objects.get(id = Semester_id)
	if context['institute'] == my_semester.Branch_id.Department_id.Institute_id:	# Check if the user is in the same institute as the urls
		context['my_shifts'] = Shift.objects.filter(Department_id=my_semester.Branch_id.Department_id)
		divisions = Division.objects.filter(Semester_id=Semester_id).order_by('name')
		context['form'] = create_division()
		if Division_id:	# if edit is called
			edit = divisions.get(pk=Division_id)
			form = create_division(instance = edit)
			context['update'] = form.instance
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
		raise redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_batch(request,Division_id,Batch_id = None):
	context = return_context(request)
	my_division = Division.objects.get(id = Division_id)
	if context['institute'] == my_division.Semester_id.Branch_id.Department_id.Institute_id:
																		# Check if the user is in the same institute as the urls
		batches = Batch.objects.filter(Division_id=Division_id).order_by('name')
		context['form'] = create_division()
		if Batch_id:	# if edit is called
			edit = Batch.objects.get(pk=Batch_id)
			form = create_batch(instance = edit)
			context['update'] = form.instance
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
						# print(candidate.batch_for)
						candidate.save()
						context['form'] = create_batch()     				#Form Renewed
						return redirect('show_batch',Division_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "*Name must be unique for Division*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/batch.html",context)
	else:
		raise redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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
		refresh = False
		my_faculty = Faculty_details.objects.filter(Department_id=Department_id)
		context['my_faculty_load'] = Faculty_load.objects.filter(Faculty_id__in=my_faculty)
		if Faculty_id:	# if edit is called
			context['my_subject_events'] = get_json(Subject_event.objects.filter(Faculty_id=Faculty_id),False)
			edit = my_faculty.get(pk = Faculty_id)
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
				old_load = Faculty_load.objects.get(Faculty_id=edit).total_load
				faculty_detail_form = faculty_details(request.POST,instance = edit)
				faculty_load_form = faculty_load(request.POST,instance=Faculty_load.objects.get(Faculty_id=edit))
				# print(faculty_detail_form.is_valid(),faculty_load_form.is_valid(),user_form.is_valid())
				old_can_teach = set(abc.values_list("Subject_id",flat = True))
				new_can_teach = set(request.POST.getlist('subject'))
				to_be_deleted = old_can_teach.difference(new_can_teach)
				to_be_added = new_can_teach.difference(old_can_teach)
				if not refresh:
					for i in to_be_deleted:
						print("deleted - ",Can_teach.objects.filter(Subject_id= i))
						Can_teach.objects.filter(Subject_id_id= i).delete()
					for i in to_be_added:
						Can_teach.objects.create(Faculty_id = edit,Subject_id_id=i).save()
					faculty_detail_form.save()
					if int(request.POST['total_load']) < old_load:	
						# if the new load is less then the old load delete all the subject events 
						# see pagination.js for js
						for i in context['my_subject_events']:
							i.delete()
					faculty_load_form.save()
				else :
					pass
				return redirect('add_faculty',Department_id = Department_id)

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
						refresh = True
						break
				if not refresh:
					for i in can_teach:
						i.save()
				else:
					user.delete()
			else:
				context['errors'] = [user_form.errors,faculty_detail_form.errors,faculty_load_form.errors]
	else:
		return redirect(get_home_page(request.user))
		
	return render(request,"admin/faculty/faculty_details.html",context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_slot(request,Shift_id=None):
	context = return_context(request)
	my_shift = Shift.objects.get(pk = Shift_id)
	context["my_shift"] = my_shift
	context['old_data'] = get_json(Timings.objects.filter(Shift_id = Shift_id))
	context['working_days'] = Working_days.objects.filter(Shift_id=my_shift).order_by("Days_id")
	if request.method == 'POST':
		data = json.loads(request.body)	# data is the json object returned after savings
		check_all = True
		timings = data['slots'];
		days = data['days']
		############# for working-day models #############
		old_days = set(context['working_days'].values_list("Days_id",flat=True))
		new_days = set(i for i in range(int(days[0]),int(days[1])+1))
		to_be_deleted = old_days.difference(new_days)
		to_be_saved = new_days.difference(old_days)
		for i in to_be_deleted:
			Working_days.objects.get(Days_id=i).delete()
		for i in to_be_saved:
			day = Working_days(Shift_id=my_shift,Days_id_id=i).save()
			day = Working_days.objects.get(Shift_id=my_shift,Days_id_id=i)
			for time in Timings.objects.filter(Shift_id=my_shift):
				Slots(day=day,Timing_id=time).save()
		############# for timing models #############
		working_days = Working_days.objects.filter(Shift_id=Shift_id)
		for dictonary in timings:
			if dictonary["id"] :	# if already present
				edit = Timings.objects.get(pk=int(dictonary["id"]))
				form = timing(dictonary,instance = edit)
				if form.is_valid():
					form.save()
			else:					# if new entry
				form = timing(dictonary)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Shift_id = my_shift
					candidate.save()
					for day in working_days:
						Slots(day=day,Timing_id=candidate).save()
		return redirect('show_slot',Shift_id)		
	
	return render(request,"admin/details/slot.html",context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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
		return redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
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
				delete_entries(context['my_shifts'],data)
			else:
				if Shift_id:
					form = shift(request.POST,instance=edit)
				else:
					form = shift(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Department_id = my_department
					try:	# unique contraint added
						candidate.save()
						context['form'] = shift()     				#Form Renewed
						return redirect('show_shift',Department_id)                      #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "*Shift Name must be unique for Department*"   #errors to integrityErrors
					except BaseException:
						context['integrityErrors'] = "*End time must be Greater than Start time*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
			return render(request,"admin/details/shift.html",context)
	else:
		return redirect(get_home_page(request.user))

	return render(request,"admin/details/shift.html",context)
from django.core.serializers.python import Serializer

class MySerialiser(Serializer):
	def end_object( self, obj ):
		self._current['id'] = obj._get_pk_val()
		include_list = ["Slot_id","Slot_id_2","Subject_event_id","Batch_id","Resource_id"]
		res = dict([(key, val) for key, val in self._current.items() if key in include_list]) 
		for i in res:
			if not res[i]:
				res[i] = ""
		self.objects.append( res )
		

@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_not_avail(request,Faculty_id):
	context = return_context(request)
	############# Returns slot objects for a Qs#############
	def get_slots(qs):
		return Slots.objects.filter(pk__in = qs.values("Slot_id"))
	faculty = Faculty_details.objects.get(pk = Faculty_id)
	events = Event.objects.filter(Subject_event_id__Faculty_id = Faculty_id)
	not_available = Not_available.objects.filter(Faculty_id=Faculty_id)
	Shift_id = faculty.Shift_id
	context["my_faculty"] = faculty
	context["my_department"] = faculty.Department_id
	context['working_days'] = Working_days.objects.filter(Shift_id = Shift_id)
	context['timings'] = Timings.objects.filter(Shift_id = Shift_id)
	context['slots_json'] = get_json(Slots.objects.filter( Timing_id__in = context['timings']),event = True)
	context['events'] = get_json(get_slots(events),False,event = True)
	context['not_available'] = get_json(get_slots(not_available),False,event = True)
	if request.method == "POST":
		if request.is_ajax():
			############# Old data and New data Processing #############
			slot_ids = json.loads(request.body)
			old_data = set(get_slots(not_available).values_list("id",flat = True))
			# print(old_data)
			new_data = set(slot_ids)
			to_be_deleted = old_data.difference(new_data)
			to_be_added = new_data.difference(old_data)
			############# Add - Delete#############
			print(to_be_deleted)
			for i in to_be_deleted:
				# print("deleted - ",Not_available.objects.get(Slot_id_id = i))
				Not_available.objects.get(Faculty_id=Faculty_id,Slot_id_id=i).delete()
			for i in to_be_added:
				Not_available.objects.create(Faculty_id_id=Faculty_id,Slot_id_id=i).save()
				# print("added - ",Slots.objects.get(pk = i))
		redirect('show_not_avail',Faculty_id = Faculty_id)
	return render(request,"admin/details/not_available.html",context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_sub_det(request,Branch_id,Subject_id = None):
	context = return_context(request)
	my_branch = Branch.objects.get(id = Branch_id)
	context['my_semesters'] = Semester.objects.filter(Branch_id = Branch_id)
	# print("world")
	my_subjects = Subject_details.objects.filter(Semester_id__in=context['my_semesters'])
	# print(my_subjects)
	context['my_subjects'] = my_subjects
	context['my_branch'] = my_branch
	if context['institute'] == my_branch.Department_id.Institute_id:	# Check if the user is in the same institute as the urls
		context['form'] = add_subject_details()
		if Subject_id:	# if edit is called
			edit = my_subjects.get(pk=Subject_id)
			form = add_subject_details(instance = edit)
			context['update'] = form.instance

		if request.method == 'POST':	# if create is submitted
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(my_subjects,data)
			else:
				if Subject_id:	# if edit 
					form = add_subject_details(request.POST, instance=edit) 
				else:
					form = add_subject_details(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					try:	# unique contraint added
						candidate.save()
						context['form'] = add_subject_details()		     				#Form Renewed
						return redirect('show_sub_det',Branch_id)                    #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "Name and Short must be unique for Semester"   #errors to integrityErrors
				else:
					context['errors'] = form.errors
		return render(request,"admin/details/subject_details.html",context)
	else:
		raise redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_sub_event(request,Subject_id,Faculty_id=None):
	def return_json(teachers):
		data = serializers.serialize("json", teachers)
		data = json.loads(data)
		for d in data:
			faculty = Faculty_details.objects.get(pk = d['pk'])
			d['fields']['id'] = d['pk']
			d['fields']['name'] = faculty.User_id.__str__()
			d['fields']['remaining_load'] = Faculty_load.objects.get(Faculty_id=faculty).remaining_load()
			del d['pk'],d['model'],d['fields']['User_id'],d['fields']['Designation_id'],d['fields']['Department_id'],d['fields']['Shift_id']
		return json.dumps(data)
	context = return_context(request)
	teachers = Faculty_details.objects.filter(pk__in = Can_teach.objects.filter(Subject_id=Subject_id).values("Faculty_id"))
	context["Subject_event"] = Subject_event.objects.filter(Subject_id = Subject_id)
	context["my_faculty"] = teachers.exclude(pk__in = context["Subject_event"].values("Faculty_id"))
	# print(teachers)
	my_subject = Subject_details.objects.get(pk = Subject_id)
	context["remaining_lect"],context["remaining_prac"] = my_subject.remaining_lect_prac()
	context["my_subject"] = my_subject
	context['my_branch'] = my_subject.Semester_id.Branch_id
	context['fac'] = return_json(teachers)
	context['form'] = add_sub_event()
	if Faculty_id:	# if edit is called
		edit = Subject_event.objects.get(Faculty_id=Faculty_id, Subject_id = Subject_id)
		form = add_sub_event(instance = edit)
		form.instance.Faculty_id = edit.Faculty_id
		context['update'] = form.instance
	if request.method == 'POST':
		if request.is_ajax():	# if delete is called
			data = json.loads(request.body)
			delete_entries(context["Subject_event"],data)
		else:
			if Faculty_id:	# if edit 
				form = update_sub_event(request.POST, instance=edit)
				# form.instance.Faculty_id = Faculty_details.objects.get(pk = Faculty_id)
			else:
				form = add_sub_event(request.POST)
			if form.is_valid():
				candidate = form.save(commit=False)
				candidate.Subject_id = my_subject
				print("it is true :: ",candidate)
				try:	# unique contraint added
					candidate.save()
					context['form'] = add_sub_event()     				#Form Renewed
					return redirect('show_sub_event',Subject_id)                      #Page Renewed
				except IntegrityError:
					context['integrityErrors'] = "*Subject can have only one Unique Faculty.*"   #errors to integrityErrors
			else:
				context['errors'] = form.errors
	return render(request,"admin/details/subject_events.html",context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_resource(request,Resource_id = None):
	context = return_context(request)
	context['my_resources'] = Resource.objects.filter(Institute_id=context['institute'])
	if context['institute']:	# Check if the user is in the same institute as the urls
		context['form'] = add_resource()
		if Resource_id:	# if edit is called
			edit = context['my_resources'].get(pk = Resource_id)
			form = add_resource(instance = edit)
			context["update"] = form.instance
		if request.method == 'POST':
			if request.is_ajax():	# if delete is called
				data = json.loads(request.body)
				delete_entries(context['my_resources'],data)
			else:
				if Resource_id:
					form = add_resource(request.POST,instance=edit)
				else:
					form = add_resource(request.POST)
				if form.is_valid():
					candidate = form.save(commit=False)
					candidate.Institute_id = context['institute']
					try:	# unique contraint added
						candidate.save()
						context['form'] = add_resource()     			#Form Renewed
						return redirect('show_resource')                  #Page Renewed
					except IntegrityError:
						context['integrityErrors'] = "*Name must be unique for Institute*"   #errors to integrityErrors
				else:
					context['errors'] = form.errors.as_text()
					print(context['errors'])
		print(context['my_resources'])
		return render(request,"admin/details/resources.html",context)
	else:
		return redirect(get_home_page(request.user))


@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def show_table(request,Division_id):
	# the remaining lect and prac for all the subjects should return 0,0
	#  to start the timetable
	context = return_context(request)
	if request.method == "POST":
		old_events_qs = list(Event.objects.filter(Division_id=Division_id).values_list('Slot_id', 'Subject_event_id', 'Batch_id', 'Resource_id', 'Slot_id_2'))
		json_events = json.loads(request.body)
		new_events = set()
		old_events = set()
		for l in json_events:
			new_events.add(tuple(map(str, l.values())))
		for i in old_events_qs:
			old_events.add(tuple(map(str, i)))
		to_be_added = new_events.difference(old_events)
		to_be_deleted = old_events.difference(new_events)
		# print(to_be_added,to_be_deleted)
		def foo(x,i):
			if tuple(map(str, x.values())) == i:
				return True
			return False
		for i in to_be_deleted:
			def get_str(a):
				return str(a) if a else None
			TBD = Event.objects.filter(Division_id=Division_id,Slot_id= get_str(i[0]))
			# print(TBD)
			if len(TBD):
				TBD.delete()
		for i in to_be_added:
			TBA = [x for x in json_events if foo(x,i)]
			print(TBA)
			form = add_event(TBA[0])
			candidate = form.save(commit=False)
			candidate.Division_id_id = Division_id
			form.save()
		redirect('show_table',Division_id)
	
	my_division = Division.objects.get(pk = Division_id)
	Shift_id = my_division.Shift_id
	subjects = Subject_details.objects.filter(Semester_id=my_division.Semester_id)
	serializer = MySerialiser()
	my_semester = my_division.Semester_id
	my_batches = Batch.objects.filter(Division_id=Division_id).order_by("name")
	timings = Timings.objects.filter(Shift_id = Shift_id)
	subject = {}
	for i in Subject_details.objects.filter(Semester_id = my_semester):
		subject[i] = Subject_event.objects.filter(Subject_id=i)
	context['working_days'] = Working_days.objects.filter(Shift_id = Shift_id)
	context['timings'] = timings
	context['slots_json'] = get_json(Slots.objects.filter( Timing_id__in = timings),time_table_event=True,my_division=Division_id)
	context['subject_events_json'] = get_json(Subject_event.objects.filter(Subject_id__in=subjects),time_table=True,my_division=Division_id)
	context['events_json'] = serializer.serialize(Event.objects.filter(Division_id=Division_id))
	context['subject_events'] = Subject_event.objects.filter(Subject_id__in=subjects).order_by("Subject_id")
	context['my_subjects'] = subject
	context['resources'] = Resource.objects.filter(Institute_id=my_division.Shift_id.Department_id.Institute_id)
	context['my_batches'] = my_batches
	context['batches_json'] = get_json(my_batches)
	print(Event.objects.filter(Division_id=Division_id))
	print(Slots.objects.filter( Timing_id__in = timings)[0])
	return render(request,"try/table.html",context)





from admin_V1.algo import get_points,get_sorted_events,put_event

from tabulate import tabulate

import admin_V1.algo2 as algo

def algo_context(request,Division_id):
	context = {}
	my_division = Division.objects.get(pk = Division_id)
	Shift_id = my_division.Shift_id
	subjects = Subject_details.objects.filter(Semester_id=my_division.Semester_id)
	serializer = MySerialiser()
	my_semester = my_division.Semester_id
	my_batches = Batch.objects.filter(Division_id=Division_id).order_by("name")
	timings = Timings.objects.filter(Shift_id = Shift_id)
	subject = {}
	for i in Subject_details.objects.filter(Semester_id = my_semester):
		subject[i] = Subject_event.objects.filter(Subject_id=i)
	context["my_events"] = Event.objects.filter(Division_id=Division_id)
	context['working_days'] = Working_days.objects.filter(Shift_id = Shift_id)
	context['timings'] = timings
	context['slots_json'] = get_json(Slots.objects.filter( Timing_id__in = timings),time_table_event=True,my_division=Division_id)
	context['subject_events_json'] = get_json(Subject_event.objects.filter(Subject_id__in=subjects),time_table=True,my_division=Division_id)
	context['events_json'] = serializer.serialize(Event.objects.filter(Division_id=Division_id))
	context['subject_events'] = Subject_event.objects.filter(Subject_id__in=subjects).order_by("Subject_id")
	context['my_subjects'] = subject
	context['resources'] = Resource.objects.filter(Institute_id=my_division.Shift_id.Department_id.Institute_id)
	context['my_batches'] = my_batches
	context['batches_json'] = get_json(my_batches)	
	context['slots_json'] = get_json(Slots.objects.filter( Timing_id__in = timings),time_table_event=True,my_division=Division_id)
	algo.put_vars(my_division)
	return context

def algo_v1(request,Division_id):
	# delete all the prior events after taking the locked events
	# save all the locked events
	context = algo_context(request,Division_id)
	locked_events = Event.objects.filter(Division_id=Division_id)
	subject_events = algo.get_sorted_events(context["subject_events"],locked_events)
	for subject_event in subject_events:
		prac_carried = subject_event.prac_carried
		lect_carried = subject_event.lect_carried
		if prac_carried:	# if the faculty has practicals here
			batches = subject_event.Subject_id.batch_set.filter(batch_for = "prac")
			locked_subject_event = locked_events.filter(Subject_event_id=subject_event).exclude(Slot_id_2=None)
			prac_per_week = subject_event.Subject_id.prac_per_week
			if batches:
				for batch in batches:
					locked_prac_count = locked_subject_event.filter(Batch_id = batch).count()

					remaining_count = prac_per_week-locked_prac_count	# get the practicals remaining after locking
					prac_remaining = subject_event.prac_carried - locked_subject_event.count()
					# get the capability of the faculty to take this event

					remaining_count = remaining_count if remaining_count<prac_remaining else prac_remaining
					# if the faculty has no capicity then have the highest capability be remaining count
					
					for i in range(remaining_count):
						# print(batch,"-",subject_event)
						algo.get_subject_events(Division_id,subject_event,True,locked_events,batch)
			else:
				locked_prac_count = locked_subject_event.count()
				
				remaining_count = prac_per_week-locked_prac_count	# get the practicals remaining after locking
				prac_remaining = subject_event.prac_carried - locked_subject_event.count()
				# get the capability of the faculty to take this event

				remaining_count = remaining_count if remaining_count<prac_remaining else prac_remaining
				# if the faculty has no capicity then have the highest capability be remaining count
				
				for i in range(remaining_count):
					# print(subject_event,"- Class")
					algo.get_subject_events(Division_id,subject_event,True,locked_events)

		if lect_carried:
			batches = subject_event.Subject_id.batch_set.filter(batch_for = "lect")
			locked_subject_event = locked_events.filter(Subject_event_id=subject_event,Slot_id_2=None)
			lect_per_week = subject_event.Subject_id.lect_per_week
			if batches:		# if the subject has a batch
				for batch in batches:
					locked_lect_count = locked_subject_event.filter(Batch_id = batch).count()

					remaining_count = lect_per_week-locked_lect_count	# get the practicals remaining after locking
					lect_remaining = subject_event.lect_carried - locked_subject_event.count()
					# get the capability of the faculty to take this event

					remaining_count = remaining_count if remaining_count < lect_remaining else lect_remaining
					# if the faculty has no capicity then have the highest capability be remaining count
					
					for i in range(remaining_count):
						# print(batch,"-",subject_event)
						algo.get_subject_events(Division_id,subject_event,False,locked_events,batch)

			else:
				locked_lect_count = locked_subject_event.count()
				
				remaining_count = lect_per_week-locked_lect_count	# get the practicals remaining after locking
				lect_remaining = subject_event.lect_carried - locked_subject_event.count()
				# get the capability of the faculty to take this event

				remaining_count = remaining_count if remaining_count<lect_remaining else lect_remaining
				# if the faculty has no capicity then have the highest capability be remaining count
				
				for i in range(remaining_count):
					# print(subject_event,"- Class")
					algo.get_subject_events(Division_id,subject_event,False,locked_events)
					
				# print(subject_event," - Class")



		# if locked_events :
		# 	subject_event_locked = locked_events.filter(Subject_event_id=subject_event)
		# 	prac_carried = subject_event.prac_carried
		# 	lect_carried = subject_event.lect_carried
		# 	lect_batch = Batch.objects.filter(Division_id = Division_id,batch_for="lect")
		# 	if len(lect_batch):
		# 		for batch in lect_batch:
		# 			print(batch)
		# 	else:
		# 		print(subject_event)
		# 	print(subject_event ," - ",prac_carried,lect_carried)
			# locked_events.filter()
			
	print(tabulate(algo.l,headers=["event","batch","type"],tablefmt="grid"))
	# 	# print(subject_event.Subject_id.lect_per_week)

	# print(list(locked_events.values_list("Subject_event_id",flat=True)))
	return render(request,"try/algo_v1.html",context)