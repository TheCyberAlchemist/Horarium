from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
 
from Table_V2.models import *
from institute_V1.models import *
from faculty_V1.models import *
from admin_V1.views import return_context

#region //////////////////// other_functions //////////////////
def lcm(x, y):
	# choose the greater number
	x = 1 if not x else x
	y = 1 if not y else y
	greater = max(x,y)
	while(True):
		if greater % x == 0 and greater % y == 0:
			ans = greater
			break
		greater += 1
	return ans

#endregion
#region //////////////////// Division Print //////////////////

def select_batch_for_division(request,Division_id):
	context = return_context(request)
	batch_list = Batch.objects.all().filter(Division_id_id=Division_id)
	context['my_division'] = Division.objects.get(pk=Division_id)
	context['my_prac_batches'] = batch_list.filter(batch_for="prac")
	context['my_lect_batches'] = batch_list.filter(batch_for="lect")
	post_result = {
		'lect_batch': ['53', '55'],
		'prac_batch': ['59', '60']
	}
	
	# if request.method == 'POST':
	# 	print(request.POST)

	return render(request,"admin/create_table/select_batch.html",context)


def division_print(request,Division_id):
	template = "admin/print_table/division_print.html"
	Division_id = Division.objects.get(pk=Division_id)
	my_shift = Division_id.Shift_id

	# lect_batch_list = ["58","59","60"]
	# prac_batch_list = ['53', '55',"57"]

	lect_batch_list=request.GET.getlist("lect_batch")
	prac_batch_list=request.GET.getlist("prac_batch")

	prac_batches = Batch.objects.all().filter(pk__in=prac_batch_list)
	lect_batches = Batch.objects.all().filter(pk__in=lect_batch_list)

	all_division_events = Event.objects.all().filter(Division_id=Division_id)
	my_events = all_division_events.filter(Q(Batch_id=None) | Q(Batch_id__in = prac_batch_list) | Q(Batch_id__in =lect_batch_list))

	lect_batch_count,prac_batch_count = len(lect_batch_list),len(prac_batch_list)
	unit_col = lcm(lect_batch_count,prac_batch_count)
	lect_batch_col = unit_col/lect_batch_count if lect_batch_count else unit_col
	prac_batch_col = unit_col/prac_batch_count if prac_batch_count else unit_col
	prac_str = ','.join([str(batch.name) for batch in prac_batches])
	lect_str = ','.join([str(batch.name) for batch in lect_batches])
	context = {
		'my_division' : Division_id,
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
		"prac_batches": prac_batches,
		"lect_batches": lect_batches,
		'unit_col': unit_col,
		"lect_batch_col": lect_batch_col,
		"prac_batch_col": prac_batch_col,
		'file_name' : f"{Division_id.name} ({prac_str}) ({lect_str})",
	}
	if request.method == "POST":	# if print is called
		context['print'] = True
		return export_pdf(template,f"{Division_id.name} ({prac_str}) ({lect_str})",context)
	return render(request,template,context)
#endregion

#region //////////////////// Resource Print //////////////////
def select_shift_for_resource(request,Resource_id):
	context = return_context(request)
	# batch_list = Batch.objects.all().filter(Division_id_id=Division_id)
	context['my_resource'] = Resource.objects.get(pk=Resource_id)
	context['my_shifts'] = Shift.objects.filter(Department_id__Institute_id=context['institute'])
	print(context['my_shifts'])
	# if request.method == 'POST':
	# 	print(request.POST)

	return render(request,"admin/create_table/select_shift.html",context)

def resource_print(request,Resource_id):
	template = "admin/print_table/resource_print.html"
	Resource_id = Resource.objects.get(pk=Resource_id)

	Shift_id=request.GET.get("shift")
	Shift_id = Shift.objects.get(pk=Shift_id)
	all_resource_events = Event.objects.active().filter(Resource_id=Resource_id,Division_id__Shift_id=Shift_id)
	context = {
		'Resource_id' : Resource_id,
		'days' : Working_days.objects.filter(Shift_id=Shift_id),
		'events' : all_resource_events,
		'timings' : Timings.objects.filter(Shift_id = Shift_id),
		'file_name' : f"{Resource_id.name} ({Shift_id})",
	}
	return render(request,template,context)

#endregion

#region //////////////////// Resource Print //////////////////
def faculty_print(request,Faculty_id):
	template = "admin/print_table/faculty_print.html"
	Faculty_id = Faculty_details.objects.get(pk=Faculty_id)

	Shift_id=Faculty_id.Shift_id
	
	all_resource_events = Event.objects.filter_faculty(Faculty_id)

	context = {
		'Faculty_id' : Faculty_id,
		'days' : Working_days.objects.filter(Shift_id=Shift_id),
		'events' : all_resource_events,
		'timings' : Timings.objects.filter(Shift_id = Shift_id),
		'file_name' : f"{Faculty_id.Designation_id} {Faculty_id.User_id}",
	}
	return render(request,template,context)

#endregion
