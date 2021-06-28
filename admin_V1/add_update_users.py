from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
import json

from .views import return_context
from institute_V1.models import *
from .forms import update_user_name,student_details
import login_V2.models as login_V2

def update_student(request):
	if request.method == 'POST':
		print(request.POST)		

def update_faculty(request):
	if request.method == 'POST':
		print(request.POST)

def faculty_edit_called(request,Department_id): 
	if request.method == 'POST':
		pk = request.POST.get('pk')
		faculty = login_V2.CustomUser.objects.get(pk=pk)
		faculty_det = faculty.faculty_details
		faculty_load = faculty_det.faculty_load_set.first()
		can_teach_subject_ids = list(faculty_det.can_teach_set.values_list("Subject_id",flat=True))
		if not faculty_det.Department_id_id == int(Department_id):
			# Check if the user is in the same institute
			return HttpResponse(status=500)
		update_data = {
			'first_name':faculty.first_name,
			'last_name':faculty.last_name,
			'email':faculty.email,
			"short":faculty_det.short,
			"Designation_id":faculty_det.Designation_id_id,
			"Shift_id":faculty_det.Shift_id_id,
			"Department_id":faculty_det.Department_id_id,
			"Faculty_load":faculty_load.total_load,
			"can_teach":can_teach_subject_ids,
		}
		print(update_data)
	return JsonResponse(update_data)

def student_edit_called(request,Department_id):
	if request.method == 'POST':
		# print(request.POST,Department_id)
		pk = request.POST.get('pk')
		# print(pk)
		student = login_V2.CustomUser.objects.all().filter(pk=pk).first()
		my_department = Department.objects.all().get(pk=Department_id)
		student_det = student.student_details
		print(student_det.Institute_id == my_department.Institute_id)
		if not  student_det.Institute_id == my_department.Institute_id:
			# Check if the user is in the same institute
			return HttpResponse(status=500)
		update_data = {
			'first_name':student.first_name,
			'last_name':student.last_name,
			'email':student.email,
			"roll_no":student_det.roll_no,
			"Institute_id": student_det.Institute_id_id,
			"Division_id": student_det.Division_id_id,
			"prac_batch": student_det.prac_batch_id,
			"lect_batch": student_det.lect_batch_id,
		}
		print(update_data)
	return JsonResponse(update_data)

def add_student(request,Department_id):
	if request.method == 'POST':
		print(request.POST.get("email"))
		name_form = update_user_name(request.POST)
		details_form = student_details(request.POST)
		if name_form.is_valid() and details_form.is_valid():
			print("Both Forms is valid ✅✅✅")
			details = details_form.save(commit=False)
			# region check if the batches selected are in the same divisions
			if details.prac_batch and not details.prac_batch.Division_id == details.Division_id:
				return JsonResponse({'error':'The batches selected are not in the same division'})
			elif details.lect_batch and not details.lect_batch.Division_id == details.Division_id:
				return JsonResponse({'error':'The batches selected are not in the same division'})
			# endregion
			print("save can be executed ✅✅")
			# name_form.save()
			# details.save()
			return JsonResponse({'success':'Saved'})
		else:
			if name_form.is_valid():
				print("name Form is valid ✅")
			else:
				print("name Form is not valid❌")
			if details_form.is_valid():
				print("details form is valid ✅")
			else:
				print("details form is not valid❌")
		# print(request.POST)

from pprint import pprint
@login_required(login_url="login")
@allowed_users(allowed_roles=['Admin'])
def user_dash(request,Department_id):
	context = return_context(request)
	# region Student form context
	my_divisions = Division.objects.active().filter(Semester_id__Branch_id__Department_id = Department_id).order_by("Semester_id__Branch_id")
	my_prac_batches = Batch.objects.all().filter(batch_for="prac",Division_id__in = my_divisions).order_by("Division_id__Semester_id__Branch_id")
	my_lect_batches = Batch.objects.all().filter(batch_for="lect",Division_id__in = my_divisions).order_by("Division_id__Semester_id__Branch_id")
	pprint(list(my_prac_batches))
	context['my_divisions'] = my_divisions
	context['my_prac_batches'] = my_prac_batches
	context['my_lect_batches'] = my_lect_batches

	# endregion

	# region Faculty form context
	# endregion

	return render(request,'admin/user_dash/user_dash.html',context)