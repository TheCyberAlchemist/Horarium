from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
import json

from admin_V1.views import return_context
from institute_V1.models import *
from faculty_V1.models import *
from admin_V1.forms import update_user_name_email,student_details,add_user,faculty_details,faculty_load
from login_V2.models import CustomUser

def update_student(request):
	if request.method == 'POST':
		print(request.POST)		

def update_faculty(request):
	if request.method == 'POST':
		print(request.POST)

def faculty_edit_called(request,Department_id): 
	if request.method == 'POST':
		pk = request.POST.get('pk')
		faculty = CustomUser.objects.get(pk=pk)
		faculty_det = faculty.faculty_details
		faculty_load = faculty_det.faculty_load
		can_teach_subject_ids = list(faculty_det.can_teach_set.values_list("Subject_id",flat=True))
		if not faculty_det.Department_id_id == int(Department_id):
			# Check if the user is in the same institute
			return HttpResponse(status=500)
		update_data = {
			'pk':faculty.pk,
			'first_name':faculty.first_name,
			'last_name':faculty.last_name,
			'email':faculty.email,
			"short":faculty_det.short,
			"Designation_id":faculty_det.Designation_id_id,
			"Shift_id":faculty_det.Shift_id_id,
			"total_load":faculty_load.total_load,
			"can_teach":can_teach_subject_ids,
		}
		print(update_data)
	return JsonResponse(update_data)

def student_edit_called(request,Department_id):
	if request.method == 'POST':
		# print(request.POST,Department_id)
		pk = request.POST.get('pk')
		# print(pk)
		student = CustomUser.objects.all().filter(pk=pk).first()
		my_department = Department.objects.all().get(pk=Department_id)
		student_det = student.student_details
		print(student_det.Institute_id == my_department.Institute_id)
		if not  student_det.Institute_id == my_department.Institute_id:
			# Check if the user is in the same institute
			return HttpResponse(status=500)
		update_data = {
			'pk':student.pk,
			'first_name':student.first_name,
			'last_name':student.last_name,
			'email':student.email,
			"roll_no":student_det.roll_no,
			"Division_id": student_det.Division_id_id,
			"prac_batch": student_det.prac_batch_id,
			"lect_batch": student_det.lect_batch_id,
		}
		print(update_data)
	return JsonResponse(update_data)

def add_update_student(request,Department_id):
	if request.method == 'POST':
		user_obj = None
		if request.POST.get('pk'):
			user_obj = CustomUser.objects.all().filter(pk=request.POST.get('pk')).first()
		if user_obj:
			# if update is called (if the user-email doesn't exist)
			name_form = update_user_name_email(request.POST,instance=user_obj)
			details_form = student_details(request.POST,instance=user_obj.student_details)
			print("\nEdit is called 📥")
		else:
			# if add is called (if the user-email exist)
			name_form = add_user(request.POST)			
			details_form = student_details(request.POST)
			print("\nAdd is called ➕")
		if name_form.is_valid() and details_form.is_valid():
			print("Both Forms is valid ✅✅✅")
			details = details_form.save(commit=False)
			# region check if the batches selected are in the same divisions
			if details.prac_batch and not details.prac_batch.Division_id == details.Division_id:
				return JsonResponse({'error':'<ul class=\"errorlist\"><li>Practical Batch<ul class=\"errorlist\"><li>The practical batches selected are not in the same division.</li></ul></li></ul>'}, status=500)
			elif details.lect_batch and not details.lect_batch.Division_id == details.Division_id:
				return JsonResponse({'error':'<ul class=\"errorlist\"><li>Lecture Batch<ul class=\"errorlist\"><li>The lecture batches selected are not in the same division.</li></ul></li></ul>'}, status=500)
			# endregion
			if not user_obj: # if add is called
				group = Group.objects.get(name='Student')
				user = name_form.save(commit=False)

				details.User_id = user
				details.Institute_id = Department.objects.all().get(pk=Department_id).Institute_id

			print("save can be executed ✅✅")

			# name_form.save()
			# user.groups.add(group)
			# details.save()
			print("Save has been Successfull ✅✅")			
			return JsonResponse({'success':'Saved ✅✅'})
		else:
			if name_form.is_valid():
				print("name Form is valid ✅")
			else:
				print("name Form is not valid❌")
				print(name_form.errors)
			if details_form.is_valid():
				print("details form is valid ✅")
			else:
				print("details form is not valid❌")
				print(details_form.errors)
			return JsonResponse({'error':details_form.errors.as_ul() + name_form.errors.as_ul()},status=500)


def add_update_faculty(request,Department_id):
	if request.method == 'POST':
		user_obj = None
		if request.POST.get('pk'):
			user_obj = CustomUser.objects.all().filter(pk=request.POST.get('pk')).first()
		# user_obj = CustomUser.objects.all().filter(email=request.POST.get("email")).first()
		if user_obj:
			# if edit is called (if the user-email doesn't exist)
			name_form = update_user_name_email(request.POST,instance=user_obj)
			details_form = faculty_details(request.POST,instance=user_obj.faculty_details)
			load_form = faculty_load(request.POST,instance=user_obj.faculty_details.faculty_load)
			print("Edit is called 📥")
		else:
			# if add is called (if the user-email exist)
			name_form = add_user(request.POST)
			details_form = faculty_details(request.POST)
			load_form = faculty_load(request.POST)
			print("Add is called ➕")
		if name_form.is_valid() and details_form.is_valid() and load_form.is_valid():
			print("All forms is valid ..... ✅✅✅")
			user = name_form.save(commit=False)
			details = details_form.save(commit=False)
			load = load_form.save(commit=False)
			if not user_obj: # if add is called
				group = Group.objects.get(name='Faculty')

				details.User_id = user
				details.Department_id_id = Department_id

				load.Faculty_id = details

			if user_obj: # if update
				# region # check if the new load is >= load carried 
				old_load_obj = Faculty_load.objects.get(Faculty_id=details)
				load_carried = old_load_obj.load_carried()
				if load.total_load < load_carried:
					'<ul class=\"errorlist\"><li>password2<ul class=\"errorlist\"><li>The password is too similar to the first name.</li><li>This password is too short. It must contain at least 8 characters.</li><li>This password is too common.</li></ul></li></ul>'
					return JsonResponse({'error':'<ul class=\"errorlist\"><li>Total Load<ul class=\"errorlist\"><li>The total load cannot be less than the load carried (Current Load :: {load_carried})</li></ul></li></ul>'},status=500)
				# endregion
				print("Save can be executed ..... ✅✅")

				# user.save()
				# user.groups.add(group)
				# details_form.save()
				# load_form.save()
				old_can_teach = set(Can_teach.objects.filter(Faculty_id=details).values_list("Subject_id",flat = True))
				new_can_teach = set(list(map(int,request.POST.getlist('can_teach'))))
				to_be_deleted = old_can_teach.difference(new_can_teach)
				to_be_added = new_can_teach.difference(old_can_teach)

				for i in to_be_deleted:
					print("deleted - ",Can_teach.objects.filter(Faculty_id=details,Subject_id= i))
					# Can_teach.objects.filter(Subject_id_id= i).delete()
				for i in to_be_added:
					a = Can_teach(Faculty_id = details,Subject_id_id=i)
					print("added - ",a)
					# a.save()
				print("Save has been Successfull ..... ✅✅")
			else:
				print("Save can be executed ..... ✅✅")
				# user.save()
				# details_form.save()
				# load_form.save()
				can_teach_obj_list = []
				error_in_can_teach = False
				for i in request.POST.getlist('can_teach[]'):
					try:
						can_teach_obj_list.append(Can_teach(Faculty_id = details,Subject_id_id = i))
					except Exception as e:
						print(e)
						error_in_can_teach = True
						break
				if error_in_can_teach:
					# user.delete()
					print("Save was not Successfull ❌")
					return JsonResponse({'error':'We have some problems back here please refresh the page.'})
				else:
					# for can_teach_obj in can_teach_obj_list:
					# 	can_teach_obj.save()
					print("Save has been Successfull ✅✅")
			return JsonResponse({'success':'Saved ✅✅'})
		else:
			if name_form.is_valid():
				print("User form is valid ✅")
			else:
				print("User form is not valid❌")
				print(name_form.errors)
				
			
			if details_form.is_valid():
				print("Details form is valid ✅")
			else:
				print("Details form is not valid❌")
				print(name_form.errors)
				
			
			if load_form.is_valid():
				print("Load form is valid ✅")
			else:
				print("Load form is not valid❌")
				print(load_form.errors)
			return JsonResponse({'error':details_form.errors.as_ul() + name_form.errors.as_ul() + load_form.errors.as_ul()},status=500)


from pprint import pprint
@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def user_dash(request,Department_id):
	context = return_context(request)
	# region Student form context
	my_divisions = Division.objects.active().filter(Semester_id__Branch_id__Department_id = Department_id).order_by("Semester_id__Branch_id")
	my_prac_batches = Batch.objects.all().filter(batch_for="prac",Division_id__in = my_divisions).order_by("Division_id__Semester_id__Branch_id")
	my_lect_batches = Batch.objects.all().filter(batch_for="lect",Division_id__in = my_divisions).order_by("Division_id__Semester_id__Branch_id")
	# pprint(list(my_prac_batches))
	context['my_divisions'] = my_divisions
	context['my_prac_batches'] = my_prac_batches
	context['my_lect_batches'] = my_lect_batches

	# endregion

	# region Faculty form context
	department = Department.objects.get(pk = Department_id)
	context['my_department'] = department
	context['my_branches'] = Branch.objects.filter(Department_id=department)
	context['my_sems'] = Semester.objects.filter(Branch_id__Department_id=department).order_by("short")
	context['my_subjects'] = Subject_details.objects.filter(Semester_id__in=context['my_sems'])
	context['my_shifts'] = Shift.objects.filter(Department_id=Department_id)
	context['designations'] = Faculty_designation.objects.filter(Institute_id=department.Institute_id) | Faculty_designation.objects.filter(Institute_id=None)
	# endregion
	def delete_entries(qs,data):
		' Delete from qs if exists. Data must have array of ids of items to be deleted '
		for d in data:
			i = qs.filter(pk = d).first()
			print(i)
			if i:
				i.delete()

	if request.method == 'POST':
		if request.is_ajax():	# if delete is called
			data = json.loads(request.body)
			delete_entries(
				CustomUser.objects.all().filter(
					Q(student_details__pk__isnull=False,
						student_details__Division_id__Semester_id__Branch_id__Department_id = department
					) 
					|Q(faculty_details__pk__isnull=False,
						faculty_details__Department_id_id = department
					)
				)
				,data)


	return render(request,'admin/user_dash/user_dash.html',context)