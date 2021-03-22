import math
from django.core.exceptions import ObjectDoesNotExist
from institute_V1.models import Slots,Working_days,Batch
from faculty_V1.models import Not_available,Faculty_load
from Table_V2.models import *


REPETATION_WEIGHT = -8
NO_REPETATION_WEIGHT = 4
OTHER_EVENT = 12
LOAD_IS_MORE = 3
NOT_AVAILABLE = -math.inf
SLOT_BELOW = -math.inf
PRAC_ON_PRAC = 2

########## returns all the subject events but sorted ############
def get_sorted_events(all_subject_events,locked_events):
	events = []
	my_dict = {}
	for subject_event in all_subject_events:
		t = len(Not_available.objects.filter(Faculty_id = subject_event.Faculty_id))
		t += len(Event.objects.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		if locked_events:
			t += len(locked_events.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		my_dict[subject_event] = t

	my_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
	for i in my_dict:
		events.append(i[0])
	return events

########## condition checking functions ##########
def get_or_none(classmodel = None,qs = None, **kwargs):
	if classmodel:
		try:
			return classmodel.objects.get(**kwargs)
		except classmodel.DoesNotExist:
			return False
	elif qs:
		try:
			return qs.get(**kwargs)
		except ObjectDoesNotExist:
			return False

def check_repetation(day_events,subject_event,is_prac = False,batch = None):
	if is_prac: 	# for all day events if there is same practical for same batch
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filter(Subject_event_id = subject_event,batch=batch).exclude(Slot_id_2 = None).count()
		else:		# if no batch
			repetation = day_events.filter(Subject_event_id = subject_event).exclude(Slot_id_2 = None).count()
	else:
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filter(Subject_event_id = subject_event,batch = batch,Slot_id_2 = None).count()
		else:		# if no batch
			repetation = day_events.filter(Subject_event_id = subject_event,Slot_id_2 = None).count()
	
	if repetation:
		return REPETATION_WEIGHT * repetation

	return 0


def get_points():
	pass
########## gets the subject_event and the batch or none to place it ##########

def get_subject_events(subject_event,is_prac,all_events,batch = None):
	point_dict = {}
	best_obj = None
	# won't work if all_event is null so pass shift_id here
	all_slots = Slots.objects.filter(Timing_id__Shift_id = all_events[0].Slot_id.Timing_id.Shift_id).order_by("day")
	usable_slots = all_slots.exclude(Timing_id__is_break = True)

	if is_prac:		# if the subject_event is practical
		if batch:	# if there is a batch for us to put it in
			print(batch,"-",subject_event,"-- Practical")
			print()
		else:		# if no batch
			print(subject_event,"- Class","-- Practical")
	else:			# if the subject_event is lecture
		if batch:	# if there is a batch for us to put it in
			print(batch,"-",subject_event,"-- Lecture")
		else:		# if no batch
			print(subject_event,"- Class -- Lecture")
	# return get_points(subject_event,all_events,is_prac)

