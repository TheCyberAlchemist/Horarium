from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

#region //////////////////// view_functions //////////////////
from django.shortcuts import render,redirect
def view_func(request):
	return render(request,"try/asd.html")
#endregion

#region //////////////////// event_list //////////////////
class event_list(list):
	'event_list is class for event class list'
	def filt_faculty(self,Faculty):
		'returns filtered event_list of all the (event.Subject_event_id.Faculty_id = Faculty)'
		return event_list(filter(lambda x: x.Subject_event_id.Faculty_id == Faculty,self))
	def filt_sub_event(self,sub_event):
		'returns filtered event_list of all the (event.Subject_event_id = sub_events)'
		return event_list(filter(lambda x: x.Subject_event_id == sub_event,self))
	def filt_slot(self,slot):
		'returns filtered event_list of all the (event.Slot_id = slot)'
		return event_list(filter(lambda x: x.Slot_id == slot,self))
	def filt_slot_2(self,slot):
		'returns filtered event_list of all the (event.Slot_id_2 = slot)'
		return event_list(filter(lambda x: x.Slot_id_2 == slot,self))
	def filt_batch(self,batch = None):
		'''returns filtered event_list of all the (event.Batch_id = batch)'''
		return event_list(filter(lambda x: x.Batch_id == batch,self))
	def filt_prac(self):
		'returns filtered event_list of all the practical events (event.Slot_id_2 != None)'
		return event_list(filter(lambda x: x.Slot_id_2 != None,self))
	def filt_lect(self):
		'returns filtered event_list of all the lecture events (event.Slot_id_2 = None)'
		return event_list(filter(lambda x: x.Slot_id_2 == None,self))
	def filt_slot_day(self,day):
		'returns filtered event_list of all the (event.Slot_id.day = day)'
		return event_list(filter(lambda x: x.Slot_id.day == day,self))
	def get_json(self):
		json_list = []
		# self._current['id'] = obj._get_pk_val()
		include_list = ["Slot_id_id","Slot_id_2_id","Subject_event_id_id","Batch_id_id","Resource_id_id","link"]
		# print(self[0].values(include_list))
		for ob in self:
			# res = dict([(key, val) for key, val in ob.__dict__.items() if key in include_list]) 
			my_dict = {}
			for k,v in ob.__dict__.items():
				if k in include_list:
					if not v:
						v = ""
					if k.endswith("_id"):
						k = k[:-3]
					my_dict[k] = v
			json_list.append(my_dict)
		return json_list

#endregion

import json
from .forms import add_event
from institute_V1.models import *
from Table_V2.models import *
from faculty_V1.models import *
#region //////////////////// get_functions //////////////////

def get_division_subjects_and_events(my_division):
	'returns subjects and subject events of subjects for the division'
	context = {}
	my_batches = set(Batch.objects.filter(Division_id=my_division).order_by("name"))
	my_subjects = []
	all_subjects = Subject_details.objects.filter(Semester_id=my_division.Semester_id)
	for i in all_subjects:
		subject_batches = set(i.batch_set.all())
		if len(subject_batches) == 0:
			# if the subject has no batches
			# print(i," has no batches")
			if len(i.subject_event_set.all().filter(active=True)):
				my_subjects.append(i)
			continue
		if my_batches.intersection(subject_batches):
			# if the batches of the subject has the student's batch
			# print(i," is in batches ",my_batches.intersection(subject_batches))
			if len(i.subject_event_set.all().filter(active=True)):
				my_subjects.append(i)
			continue
	
	subject_events = Subject_event.objects.active().filter(Subject_id__in = my_subjects)

	return my_subjects,subject_events

def get_locked_events(locked_events_json,Division_id):
	'get the event_list of all the locked events'
	main_list = event_list()
	for i in locked_events_json:
		del i['locked']
		form = add_event(i)
		candidate = form.save(commit=False)
		candidate.Division_id_id = Division_id
		main_list.append(candidate)
	return main_list

def get_sorted_events(my_division,my_subj_events,locked_events,priority_list): 
	'returns the sorted and prioritized list of subject_events'
	sorted_subj_events = []
	my_dict = {}
	for subject_event in my_subj_events:
		t = len(Not_available.objects.filter(Faculty_id = subject_event.Faculty_id))
		t += len(Event.objects.active().filter(Subject_event_id__Faculty_id=subject_event.Faculty_id).exclude(Division_id=my_division))
		if locked_events:
			t += len(locked_events.filt_faculty(subject_event.Faculty_id))
		my_dict[subject_event] = t

	my_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)

	for i in my_dict:
		sorted_subj_events.append(i[0])
	final_list = [i for i in sorted_subj_events if i not in priority_list]

	# convert the sorted list to a priority list 
	for e in priority_list:
		for i in sorted_subj_events:
			if i == e:
				final_list = [i] + final_list
	
	return final_list

#endregion

class main(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request):
		# request.POST has locked_events and merging_subjects
		Division_id = 2

		my_division = Division.objects.get(pk = Division_id)
		_,my_sub_events = get_division_subjects_and_events(my_division)
		
		locked_events_json = json.loads(request.POST.get("locked_events"))
		all_events = get_locked_events(locked_events_json,Division_id)
		

		infinite = True
		priority_list = []
		# append the priority list by the sub_events causing -inf
		while infinite:
			sorted_sub_events = get_sorted_events(my_division,my_sub_events,all_events,priority_list)
			
			infinite = False
			print("one")
			# get_sorted_events(subject_events,locked_events,priority_list)
		data ={
			"my_events":all_events.get_json(),
		}

		return Response(data)


