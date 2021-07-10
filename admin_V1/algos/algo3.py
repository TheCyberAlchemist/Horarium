from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import json
import math
from tabulate import tabulate
from pprint import pprint

from admin_V1.forms import add_event
from institute_V1.models import *
from Table_V2.models import *
from faculty_V1.models import *

REPETATION_WEIGHT = -8
OTHER_EVENT_FACULTY = -math.inf
LOAD_IS_MORE = -3
NOT_AVAILABLE = -math.inf
SLOT_BELOW = -math.inf
OTHER_EVENT_SLOT = -math.inf
PRAC_ON_PRAC = 2

my_division = None
WORKING_DAYS = 0
usable_slots = []


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
	def filt_sub(self,sub):
		'returns filtered event_list of all the (event.Subject_event_id.Subject_id = sub)'
		return event_list(filter(lambda x: x.Subject_event_id.Subject_id == sub,self))
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
		'returns filtered event_list of all the practical events (bool(event.Slot_id_2) == True)'
		return event_list(filter(lambda x: bool(x.Slot_id_2_id),self))
	def filt_lect(self):
		'returns filtered event_list of all the lecture events (bool(event.Slot_id_2) == False)'
		# print(self)
		return event_list(filter(lambda x: bool(x.Slot_id_2_id) == False,self))
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
	def count(self):
		return len(self)
#endregion


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
	if locked_events_json:
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

def get_slot_below(slot,day_slots):	
	'returns the slot below and takes slot obj and slot qs having day_slots '
	next_slot = day_slots.filter(Timing_id__start_time = slot.Timing_id.end_time).first()
	if next_slot:
		return next_slot
	return False

#endregion

#region //////////////////// other functions //////////////////
def append_event_list(all_events,event,events_template):
	'''Adds event to event_list and removes the same event from events_template
	returns [all_events,events_template]'''
	a = events_template.filt_sub_event(event.Subject_event_id).filt_batch(event.Batch_id)
	if len(a):
		events_template.remove(a[0])
		all_events.append(event)
	return all_events,events_template

def fill_global_vars(Division_id):
	'gets the division_id and adds the related info to the file to use'
	global WORKING_DAYS,usable_slots,l,my_division
	division = Division.objects.all().filter(pk = Division_id).first()
	# print(Division_id,Division.objects.all())
	my_division = division
	WORKING_DAYS = Working_days.objects.filter(Shift_id=division.Shift_id).count()
	all_slots = Slots.objects.filter(Timing_id__Shift_id = division.Shift_id).order_by("day")
	usable_slots = all_slots.exclude(Timing_id__is_break = True)
	l = []
#endregion

#region //////////////////// check_functions //////////////////


def check_repetation(day_events,subject_event,is_prac = False,batch = None):
	'''
	REPETATION_WEIGHT(-8) * number_of_repetations or 0
	'''
	if is_prac: 	# for all day events if there is same practical for same batch
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filt_sub_event(subject_event).filt_batch(batch).filt_prac().count()
		else:		# if no batch
			repetation = day_events.filt_sub_event(subject_event).filt_prac().count()
	else:
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filt_sub_event(subject_event).filt_batch(batch).filt_lect().count()
		else:		# if no batch
			repetation = day_events.filt_sub_event(subject_event).filt_lect().count()
	if repetation:
		return REPETATION_WEIGHT * repetation
	return 0


def check_availability(slot,subject_event):
	'returns -inf if the faculty is not available at that spot'
	if Not_available.objects.filter(Faculty_id=subject_event.Faculty_id,Slot_id=slot).first():
		return NOT_AVAILABLE
	else:
		return 0


def check_load_distribution(day_events,subject_event,is_prac = False):
	'''
	LOAD_IS_MORE(-3) * delta(today's load - ave_load) or 0
	'''
	faculty_details = subject_event.Faculty_id
	same_events = day_events.filt_faculty(faculty_details)
	todays_load = 0
	for event in same_events:
		if event.Slot_id_2:
			todays_load += 2
		else:
			todays_load += 1
	ave_load = math.ceil(faculty_details.faculty_load.load_carried()/WORKING_DAYS)
	delta = todays_load - ave_load + (2 if is_prac else 1)
	if delta > 0:
		return LOAD_IS_MORE*delta
	return 0

def check_other_events_for_faculty(slot,all_events,subject_event,is_prac=False):
	'sees if there is another event of the same faculty for the slot in other divisions and in all_slots'
	# print(slot)	
	# for other divisions
	e = Event.objects.filter(Slot_id = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id).exclude(Division_id=my_division).first()
	e = Event.objects.filter(Slot_id_2 = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id).exclude(Division_id=my_division).first() if not e else e
	if e:
		return OTHER_EVENT_FACULTY
	###############
	# for same division
	same_division_events = all_events.filt_slot(slot).filt_faculty(subject_event.Faculty_id)
	same_division_events += all_events.filt_slot_2(slot).filt_faculty(subject_event.Faculty_id)
	if same_division_events:
		return OTHER_EVENT_FACULTY
	###############
	return 0


def check_other_events_for_slot(all_events,slot,subject_event,batch=None,slot_below=None):
	# checks the slot to see if there is another event already or not
	if slot_below: # if practical
		e = all_events.filt_slot(slot)
		e += all_events.filt_slot_2(slot_below)
		if e :	# if there is any event
			if not batch:	# if class_prac
				return OTHER_EVENT_SLOT
			if not e[0].Slot_id_2:		# if the event is a lecture
				return OTHER_EVENT_SLOT
			if e[0].Slot_id_2 and (not e[0].Batch_id or e.filt_batch(batch)) :	
				# if the event is a practical and the batch is empty  or
				# if the event does not have a batch i.e. not div_prac
				# print("{}--{}".format(e,e.filter(Batch_id=batch)))
				return OTHER_EVENT_SLOT
	else:	# if lecture
		e = all_events.filt_slot(slot)
		e += all_events.filt_slot_2(slot)
		if e:
			if e[0].Slot_id_2:		# if there is a prac event
				return OTHER_EVENT_SLOT
			if batch:	# if there is a batch_lect
				if e.filt_batch(batch):
					return OTHER_EVENT_SLOT
			else:	# if there is a class_lect
				return OTHER_EVENT_SLOT
	return 0

def check_prac_on_prac(events_on_slot,batch_list):
	if events_on_slot and events_on_slot[0].Batch_id:
		# if there is a events_on_slot
		# and others having a batch
		for event in events_on_slot:
			if event.Batch_id in batch_list:
				# if event batch having same batch as batch_list
				return 0
		return PRAC_ON_PRAC
	return 0

def is_better_slot(points,best_pair,this_slot):
	'returns if this_slot is better or not'
	if points > best_pair[0]:	# if slot is better
		return True
	if points == best_pair[0] and points != -math.inf:	# if slot has same points as best one
		if best_pair[1].Timing_id.start_time > this_slot.Timing_id.start_time:
			# if the given slot is earlier
			return True
	return False

#endregion

#region //////////////////// Get-point functions //////////////////

def get_point_for_prac_batch(subject_event,all_events,batch_list):
	# print(subject_event,all_events,batch_list)
	day = None
	best_pair = [-math.inf,"",""]
	tab = []
	for slot in usable_slots:
		next_slot_point = points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filt_slot_day(day)
		slot_below = get_slot_below(slot,day_slots)
		if slot_below:	
			prac_event_on_slot = day_events.filt_slot(slot).filt_slot_2(slot_below)

			points = check_availability(slot,subject_event)
			if points == 0:		# if it is available
				points += check_load_distribution(day_events,subject_event,True)
				points += check_other_events_for_faculty(slot,all_events,subject_event,True)
				temp_points = math.inf
				for batch in batch_list:
					t_points = 0
					t_points += check_repetation(day_events,subject_event,True,batch)
					t_points += check_other_events_for_slot(all_events,slot,subject_event,batch,slot_below)
					temp_points = min(t_points,temp_points)
				if temp_points != math.inf:
					points += temp_points
				else:		# if something is wrong in the above loop
					raise Exception("There is an exception here in practical batch")
			
			next_slot_point = check_availability(slot,subject_event)
			if next_slot_point == 0:		# if it is available
				next_slot_point += check_load_distribution(day_events,subject_event,True)
				next_slot_point += check_other_events_for_faculty(slot,all_events,subject_event,True)
				temp_points = math.inf
				for batch in batch_list:
					# get the least value from all the batches for the slot
					t_points = 0
					t_points += check_repetation(day_events,subject_event,True,batch)
					temp_points = min(t_points,temp_points)
				if temp_points != math.inf:
					points += temp_points
				else:		# if something is wrong in the above loop
					raise Exception("There is an exception here")
			points = min(points,next_slot_point)
			points += check_prac_on_prac(prac_event_on_slot,batch_list)

			tab.append([slot,points])
		if is_better_slot(points,best_pair,slot):
			best_pair[0] = points
			best_pair[1] = slot
			best_pair[2] = slot_below
	# if batch and subject_event.pk == 29:
	# print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair

def get_point_for_prac_class(subject_event,all_events):
	day = None
	best_pair = [-math.inf,"",""]
	tab = []
	for slot in usable_slots:
		next_slot_point = points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filt_slot_day(day)
		slot_below = get_slot_below(slot,day_slots)
		if slot_below:

			points = check_availability(slot,subject_event)
			if points == 0:		# if it is available
				points += check_repetation(day_events,subject_event,True)
				points += check_load_distribution(day_events,subject_event,True)
				points += check_other_events_for_faculty(slot,all_events,subject_event,True)
				points += check_other_events_for_slot(all_events,slot,subject_event,slot_below= slot_below)
			next_slot_point = check_availability(slot,subject_event)
			if next_slot_point == 0:		# if it is available
				next_slot_point += check_repetation(day_events,subject_event,True)
				next_slot_point += check_load_distribution(day_events,subject_event,True)
				next_slot_point += check_other_events_for_faculty(slot_below,all_events,subject_event,True)
			points = min(points,next_slot_point)
			
			tab.append([slot,points])
		if is_better_slot(points,best_pair,slot):	# if it is better slot
			best_pair[0] = points
			best_pair[1] = slot
			best_pair[2] = slot_below
	# print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair

def get_point_for_lect_batch(subject_event,all_events,batch_list):
	day = None
	best_pair = [-math.inf,""]
	tab = []
	for slot in usable_slots:
		points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filt_slot_day(day)
		lect_event_on_slot = day_events.filt_lect().filt_slot(slot).filt_batch(None)

		points = check_availability(slot,subject_event)
		if points == 0:		# if it is available
			points += check_load_distribution(day_events,subject_event)
			points += check_other_events_for_faculty(slot,all_events,subject_event)
			temp_points = math.inf
			for batch in batch_list:
				t_points = 0
				t_points += check_repetation(day_events,subject_event,is_prac = False,batch = batch)
				t_points += check_other_events_for_slot(all_events,slot,subject_event,batch)
				temp_points = min(t_points,temp_points)
			if temp_points != math.inf:
				points += temp_points
			else:		# if something is wrong in the above loop
				raise Exception("There is an exception here in lecture batch")
			points += check_prac_on_prac(lect_event_on_slot,batch_list)
		if is_better_slot(points,best_pair,slot):	# if it is better slot
			best_pair[0] = points
			best_pair[1] = slot
		# tab.append([slot,points])
	# print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair


def get_point_for_lect_class(subject_event,all_events):
	day = None
	best_pair = [-math.inf,""]
	tab = []
	for slot in usable_slots:
		points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filt_slot_day(day)

		points = check_availability(slot,subject_event)
		if points == 0:		# if it is available
			points += check_repetation(day_events,subject_event)
			points += check_load_distribution(day_events,subject_event)
			points += check_other_events_for_faculty(slot,all_events,subject_event)
			points += check_other_events_for_slot(all_events,slot,subject_event)			
		
		if is_better_slot(points,best_pair,slot):	# if it is better slot
			best_pair[0] = points
			best_pair[1] = slot


		# tab.append([slot,points])
	# print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair


#endregion

class main(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request, Division_id=None):
		import timeit
		starttime = timeit.default_timer()
		if not Division_id:
			Division_id = 2
		fill_global_vars(Division_id)

		my_division = Division.objects.get(pk = Division_id)
		_,my_sub_events = get_division_subjects_and_events(my_division)
		
		locked_events_json = json.loads(request.POST.get("locked_events"))
		mearging_obj = json.loads(request.POST.get("merging_events"))
		# we can use mearging subs also for sorted_sub_events
		# print(mearging_obj)
		# return Response()
		infinite = True
		priority_list = []
		
		# append the priority list by the sub_events causing -inf
		while infinite:
			l = []
			results_list = []
			all_events = event_list()		
			events_template = event_list()
			sorted_sub_events = get_sorted_events(my_division,my_sub_events,all_events,priority_list)
			#region make events_template
			for subject_event in sorted_sub_events:
				prac_carried = subject_event.prac_carried
				lect_carried = subject_event.lect_carried
				all_events_of_subject = events_template.filt_sub(subject_event.Subject_id)
				# print(all_events_of_subject)
				d = False
				if prac_carried:	# if the faculty has practicals here
					batches = subject_event.Subject_id.batch_set.filter(batch_for = "prac")
					subject_prac_per_week = subject_event.Subject_id.prac_per_week
					if batches:
						# print(batches)
						for batch_list in batches:
							locked_prac_for_subject_event = events_template.filt_sub_event(subject_event).filt_prac()
							locked_prac_count_for_batch = all_events_of_subject.filt_batch(batch_list).count()

							remaining_count = subject_prac_per_week-locked_prac_count_for_batch	
							# the practicals remaining for the batch after locking
							faculty_max_remaining = subject_event.prac_carried - locked_prac_for_subject_event.count()
							# the maximum number of practicals faculty can take

							remaining_count = min(remaining_count,faculty_max_remaining)
							# the remaining number of practicals that can be taken for batch and subject_event
							if False:
								print(f"locked_prac_count_for_batch- {locked_prac_count_for_batch}\nremaining_count-{remaining_count}\nfaculty_max_remaining-{faculty_max_remaining}")
							
							for i in range(remaining_count):
								temp_eve = Event(
												Slot_id_2_id = -1,
												Division_id = my_division,
												Batch_id = batch_list,
												Subject_event_id = subject_event
											)
								events_template.append(temp_eve)
								if d:
									print("Practical - ",batch_list,"-",subject_event)
								# locked_events |= Event.objects.active().filter(pk=algo.get_subject_events(Division_id,subject_event,True,locked_events,batch))
					else:
						locked_prac_for_subject_event = events_template.filt_sub_event(subject_event).filt_prac()

						locked_prac_count = all_events_of_subject.filt_prac().count()

						remaining_count = subject_prac_per_week-locked_prac_count	
						# the practicals remaining after locking

						faculty_max_remaining = subject_event.prac_carried - locked_prac_for_subject_event.count()
						# the maximum number of practicals faculty can take

						remaining_count = min(remaining_count,faculty_max_remaining)
						# the remaining number of practicals that can be taken for subject_event
						
						for i in range(remaining_count):
							temp_eve = Event(
											Slot_id_2_id = -1,
											Division_id = my_division,
											Subject_event_id = subject_event
										)
							events_template.append(temp_eve)
							if d:
								print("Practical - ",subject_event,"- Class")
							# locked_events |= Event.objects.active().filter(pk=algo.get_subject_events(Division_id,subject_event,True,locked_events))

				if lect_carried:
					batches = subject_event.Subject_id.batch_set.filter(batch_for = "lect")
					locked_lect_for_subject_event = events_template.filt_sub_event(subject_event).filt_lect()
					subject_lect_per_week = subject_event.Subject_id.lect_per_week
					if batches:		# if the subject has a batch
						for batch_list in batches:
							locked_lect_count_for_batch = all_events_of_subject.filt_batch(batch_list).count()

							remaining_count = subject_lect_per_week-locked_lect_count_for_batch	
							# the lectures remaining after locking
							faculty_max_remaining = subject_event.lect_carried - locked_lect_for_subject_event.count()
							# the maximum number of lectures faculty can take
							
							remaining_count = min(remaining_count,faculty_max_remaining)
							# if the faculty has no capicity then have the highest capability be remaining count
							
							for i in range(remaining_count):
								temp_eve = Event(
											Division_id = my_division,
											Batch_id = batch_list,
											Subject_event_id = subject_event
										)
								events_template.append(temp_eve)
								if d:
									print("Lecture - ",batch_list,"-",subject_event)
								# locked_events |= Event.objects.active().filter(pk=algo.get_subject_events(Division_id,subject_event,False,locked_events,batch))

					else:
						locked_lect_count = all_events_of_subject.filt_lect().count()

						remaining_count = subject_lect_per_week-locked_lect_count
						# the lectures remaining after locking
						faculty_max_remaining = subject_event.lect_carried - locked_lect_for_subject_event.count()
						# get the capability of the faculty to take this event
						
						# print(f"locked_lect_count- {locked_lect_count}\nremaining_count-{remaining_count}\nfaculty_max_remaining-{faculty_max_remaining}")

						remaining_count = min(remaining_count,faculty_max_remaining)
						# if the faculty has no capicity then have the highest capability be remaining count
						
						for i in range(remaining_count):
							temp_eve = Event(
											Division_id = my_division,
											Subject_event_id = subject_event
										)
							events_template.append(temp_eve)
							if d:
								print("Lecture - ",subject_event,"- Class")
							# locked_events |= Event.objects.active().filter(pk=algo.get_subject_events(Division_id,subject_event,False,locked_events))
			#endregion
			for locked_event in get_locked_events(locked_events_json,Division_id):
				all_events,events_template = append_event_list(all_events,locked_event,events_template)
			
			while events_template:
				# print(events_template[0])
				template = events_template.pop(0)
				is_prac = bool(template.Slot_id_2_id)
				batch_list = [template.Batch_id] if template.Batch_id else None
				subject_event = template.Subject_event_id
				mearging_batches = mearging_obj.get(str(subject_event.Subject_id_id))

				if mearging_batches:
					# if the subject has mearging batches
					if batch_list and str(batch_list[0].id) in mearging_batches:
						# if the current batch is in mearging batches
						event_type = "prac" if is_prac else "lect"
						batch_list = list(Batch.objects.filter(pk__in=mearging_batches,batch_for=event_type))
				
				if is_prac:		# if the subject_event is practical
					if batch_list:	# if there is a batch for us to put it in
						l.append([subject_event, batch_list,"Practical"])
						points,best_slot,slot_2 = get_point_for_prac_batch(subject_event,all_events,batch_list)
						if points != -math.inf:
							for batch in batch_list:
								all_events.append(
									Event(	
										Slot_id = best_slot,
										Slot_id_2 = slot_2,
										Division_id = my_division,
										Batch_id = batch,
										Subject_event_id = subject_event
									)
								)
						# print(template.Subject_event_id,template.Slot_id_2_id,template.Division_id,template.Batch_id)
						# print(batch_list.remove(template.Batch_id))
						for batch in batch_list:
							if batch != template.Batch_id:
								other_event_templates = events_template.filt_batch(batch).filt_prac().filt_sub(subject_event.Subject_id)[0]
								events_template.remove(other_event_templates)

						results_list.append([subject_event, batch_list,"Practical",best_slot,slot_2,points])

						# print([subject_event, batch_list,"Practical"])
						# points,best_slot,slot_2 = get_point_for_prac_batch(subject_event,all_events,batch)
						# print(subject_event,best_slot)
					else:		# if no batch
						l.append([subject_event,"Class","Practical"])
						points,best_slot,slot_2 = get_point_for_prac_class(subject_event,all_events)
						if points != -math.inf:
							all_events.append(
								Event(	
									Slot_id = best_slot,
									Slot_id_2 = slot_2,
									Batch_id=batch_list,
									Division_id = my_division,
									Subject_event_id = subject_event
								)
							)
						results_list.append([subject_event, batch_list,"Practical",best_slot,slot_2,points])
						# print([subject_event,"Class","Practical"])
						# points,best_slot,slot_2 = get_point_for_prac_class(subject_event,all_events)
						# print(points,best_slot)
				else:			# if the subject_event is lecture
					if batch_list:	# if there is a batch for us to put it in
						l.append([subject_event,batch_list,"Lecture"])
						points,best_slot = get_point_for_lect_batch(subject_event,all_events,batch_list)
						if points != -math.inf:
							for batch in batch_list:
								all_events.append(
									Event(
										Slot_id = best_slot,
										Division_id = my_division,
										Batch_id = batch,
										Subject_event_id = subject_event
									)
								)
						
						for batch in batch_list:
							if batch != template.Batch_id:
								other_event_templates = events_template.filt_batch(batch).filt_lect().filt_sub(subject_event.Subject_id)[0]
								events_template.remove(other_event_templates)
						# print([subject_event,batch_list,"Lecture"])
						# points,best_slot = get_point_for_lect_batch(subject_event,all_events,batch_list)
						results_list.append([subject_event, batch_list,"Lecture",best_slot,None,points])
					else:		# if no batch
						l.append([subject_event,"Class","Lecture"])
						points,best_slot = get_point_for_lect_class(subject_event,all_events)
						if points != -math.inf:
							all_events.append(
								Event(
									Slot_id = best_slot,
									Division_id = my_division,
									Subject_event_id = subject_event
								)
							)
						# print([subject_event,"Class","Lecture"])
						# points,best_slot = get_point_for_lect_class(subject_event,all_events)
						results_list.append([subject_event, batch_list,"Lecture",best_slot,None,points])
				print("Slot_id :: {} \n Point :: {}\n -----------------------------".format(best_slot,points))


			infinite = False
			# print("one")
			# get_sorted_events(subject_events,locked_events,priority_list)
			# print(tabulate(l,headers=["Subject_event","Batch","type"],tablefmt="grid"))
			# pprint(all_events)
		print(tabulate(results_list,headers=["Subject_event","Batch","type","Slot_1","Slot_2","Points"],tablefmt="grid"))
		data ={
			"my_events":all_events.get_json(),
		}
		print("The context time :", timeit.default_timer() - starttime)
		return Response(data)

