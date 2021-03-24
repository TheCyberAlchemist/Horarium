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
WORKING_DAYS = 0
usable_slots = []
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

########## Get or none ##########
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

########## condition checking functions ##########

def check_repetation(day_events,subject_event,is_prac = False,batch = None):
	if is_prac: 	# for all day events if there is same practical for same batch
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filter(Subject_event_id = subject_event,Batch_id=batch).exclude(Slot_id_2 = None).count()
		else:		# if no batch
			repetation = day_events.filter(Subject_event_id = subject_event).exclude(Slot_id_2 = None).count()
	else:
		if batch:	# if there is a batch for us to put it in
			repetation = day_events.filter(Subject_event_id = subject_event,Batch_id = batch,Slot_id_2 = None).count()
		else:		# if no batch
			repetation = day_events.filter(Subject_event_id = subject_event,Slot_id_2 = None).count()
	
	if repetation:
		return REPETATION_WEIGHT * repetation

	return 0

def check_availability(slot,subject_event):
	# returns -inf if the faculty is not available at that spot
	if get_or_none(Not_available,None,Faculty_id=subject_event.Faculty_id,Slot_id=slot):
		return NOT_AVAILABLE
	else:
		return 0

def check_load_distribution(day_events,subject_event,is_prac = False):
	# returns -3(delta) if the load is more then the average load per day
	
	same_events = day_events.filter(Subject_event_id__Faculty_id = subject_event.Faculty_id)
	todays_load = 0
	for event in same_events:
		if event.Slot_id_2:
			todays_load += 2
		else:
			todays_load += 1
	faculty_load = Faculty_load.objects.get(Faculty_id = subject_event.Faculty_id)
	ave_load = math.ceil((faculty_load.total_load - faculty_load.remaining_load())/WORKING_DAYS)
	delta = todays_load - ave_load + (2 if is_prac else 1)
	if delta > 0:
		return -LOAD_IS_MORE*delta
	return 0

def check_other_events(slot,subject_event,is_prac=False):
	# sees if there is another event of the same faculty for the slot
	# print(slot)
	# print(Event.objects.filter(Slot_id = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id))
	e = get_or_none(classmodel = Event,Slot_id = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id)
	e = get_or_none(classmodel = Event,Slot_id_2 = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id) if not e else e
	if e:
		return -OTHER_EVENT
	return 0

def get_slot_below(slot,day_slots):	
	next_slot = get_or_none(qs = day_slots,Timing_id__start_time = slot.Timing_id.end_time)
	if next_slot:
		return next_slot
	return False

########## Get-point functions for the events ##########
def get_point_for_prac_batch(subject_event,all_events,batch):
	day = None
	best_pair = []
	for slot in usable_slots:
		next_slot_point = points = 0
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filter(Slot_id__day = day)
		slot_below = get_slot_below(slot,day_slots)
		if slot_below:
			e = all_events.filter(Slot_id = slot,Slot_id_2 = slot_below)
			if e and not e.filter(Batch_id=batch):	# if there is a practical on the slot and the batch is empty
				# seee if the batches are the same as the subject
				# print("Empty here :: ",slot,subject_event)
				# print()
				points += check_availability(slot,subject_event)
				if points == 0:		# if it is available
					points += check_repetation(day_events,subject_event,True,batch)
					points += check_load_distribution(day_events,subject_event,True)
					points += check_other_events(slot,subject_event,True)
				next_slot_point += check_availability(slot,subject_event)

				if next_slot_point == 0:		# if it is available
					next_slot_point += check_repetation(day_events,subject_event,True,batch)
					next_slot_point += check_load_distribution(day_events,subject_event,True)
					next_slot_point += check_other_events(slot,subject_event,True)
				points = min(points,next_slot_point)
				points += PRAC_ON_PRAC
				print(points)
				# remaining_batches = all_batches.exclude(pk__in = e.values_list("Batch_id_id",flat=True))

				# for batch in remaining_batches:
		# print(day_events)
		

		

		

def get_point_for_prac_class(all_events):
	pass

def get_point_for_lect_batch(all_events,batch):
	pass

def get_point_for_lect_class(all_events):
	pass

########## gets the subject_event and the batch or none to place it ##########

l = []
def put_vars(Division_id):
	global WORKING_DAYS,usable_slots,l
	WORKING_DAYS = Working_days.objects.filter(Shift_id=Division_id.Shift_id).count()
	all_slots = Slots.objects.filter(Timing_id__Shift_id = Division_id.Shift_id).order_by("day")
	usable_slots = all_slots.exclude(Timing_id__is_break = True)
	l = []

def get_subject_events(Division_id,subject_event,is_prac,all_events,batch = None):
	point_dict = {}
	best_obj = None
	# won't work if all_event is null so pass shift_id here
	
	if is_prac:		# if the subject_event is practical
		if batch:	# if there is a batch for us to put it in
			l.append([subject_event, batch,"Practical"])
			# print([subject_event, batch,"Practical"])
			point = get_point_for_prac_batch(subject_event,all_events,batch)
		else:		# if no batch
			l.append([subject_event,"Class","Practical"])
			# print([subject_event,"Class","Practical"])
			point = get_point_for_prac_class(all_events)

	else:			# if the subject_event is lecture
		if batch:	# if there is a batch for us to put it in
			l.append([subject_event,batch,"Lecture"])
			# print([subject_event,batch,"Lecture"])
			point = get_point_for_lect_batch(all_events,batch)
		else:		# if no batch
			l.append([subject_event,"Class","Lecture"])
			# print([subject_event,"Class","Lecture"])
			point = get_point_for_lect_class(all_events)

	# return get_points(subject_event,all_events,is_prac)


# if is_prac: 	# for all day events if there is same practical for same batch
# 		if batch:	# if there is a batch for us to put it in
# 			pass
# 		else:		# if no batch
# 			pass
# 	else:
# 		if batch:	# if there is a batch for us to put it in
# 			pass
# 		else:		# if no batch
# 			pass
	