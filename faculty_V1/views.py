from django.shortcuts import render
from django.core import serializers
import json
from datetime import datetime as date
from django.db.models import Q

from faculty_V1.models import Faculty_details, Chart
from Table_V2.models import Event
from institute_V1.models import Slots,Timings,Shift,Working_days
# Create your views here.

def get_events_json(qs):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		this = qs.get(pk = d['pk'])
		d["start_time"] = str(this.Slot_id.Timing_id.start_time)
		if this.Slot_id_2:
			d["end_time"] = str(this.Slot_id_2.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id) + " Practical"
		else:
			d["end_time"] = str(this.Slot_id.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id)
		d["link"] = this.link
		d["resource"] = str(this.Resource_id)
		del d['model'],d['fields']
	# print(qs)
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

def faculty_home(request):
	# for i in Slots.objects.filter(day=2):
	faculty = request.user.faculty_details
	my_shift = faculty.Shift_id
	my_events = Event.objects.filter(Subject_event_id__Faculty_id = faculty)
	# day = "Tuesday"
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
		# 'events_json' : get_events_json(my_events.filter(Slot_id__day__Days_id__name=day)),
		# 'break_json' : get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=day))
		'events_json' : get_events_json(my_events.filter(Slot_id__day__Days_id__name=date.today().strftime("%A"))),
		'break_json' : get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A")))
	}
	# print(get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A"))))
	# print(context["events"])
	return render(request,"Faculty/faculty_v1.html",context)

def faculty_feedback(request) :

	f_name = Chart.name
	f_money = Chart.money
	context = {
		'name' : f_name,
		'money' : f_money,
	}
	context["qs"] = Chart.objects.all()
	return render(request,"Faculty/feedback.html",context)