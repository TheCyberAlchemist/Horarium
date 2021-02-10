from django.shortcuts import render
from django.core import serializers
import json
from datetime import datetime as date
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from student_V1.models import Student_details
from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from Table_V2.models import Event
from institute_V1.models import Slots,Timings,Shift,Working_days
from student_V1.forms import feedback_form

def get_events_json(qs):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		this = qs.get(pk = d['pk'])
		d["start_time"] = str(this.Slot_id.Timing_id.start_time)
		if this.Slot_id_2:  # if practical
			d["end_time"] = str(this.Slot_id_2.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id) + " Practical"
		else:			# if lecture
			d["end_time"] = str(this.Slot_id.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id)
		d["link"] = this.link
		d["resource"] = str(this.Resource_id)
		del d['model'],d['fields']
	return json.dumps(data)

def get_break_json(qs,):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		this = qs.get(pk = d['pk'])
		d["start_time"] = str(this.Timing_id.start_time)
		d["end_time"] = str(this.Timing_id.end_time)
		d["name"] = str(this.Timing_id.name)
		d["pk"] = this.Timing_id.id
		del d['model'],d['fields']
	return json.dumps(data)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Student'])
def student_home(request):	
		
	# for i in Slots.objects.filter(day=2):
	student = request.user.student_details
	my_shift = student.Division_id.Shift_id
	my_events = Event.objects.filter(Q(Batch_id=student.Batch_id) | Q(Batch_id=None),Division_id=student.Division_id)
	day = ""
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
	}
	if day:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=day))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=day))
	else:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=date.today().strftime("%A")))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A")))		
	# print(context["events_json"])
	return render(request,"Student/student_v1.html",context)