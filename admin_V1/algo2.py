import math
from django.core.exceptions import ObjectDoesNotExist
from institute_V1.models import Slots,Working_days,Batch
from faculty_V1.models import Not_available,Faculty_load
from Table_V2.models import *

# nothing done for resources

REPETATION_WEIGHT = -8
OTHER_EVENT_FACULTY = 16	
LOAD_IS_MORE = 3
NOT_AVAILABLE = -math.inf
SLOT_BELOW = -math.inf
PRAC_ON_PRAC = 2
WORKING_DAYS = 0
OTHER_EVENT_SLOT = -16
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

########## Get slot below ##########
def get_slot_below(slot,day_slots):	
	next_slot = get_or_none(qs = day_slots,Timing_id__start_time = slot.Timing_id.end_time)
	if next_slot:
		return next_slot
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


def check_other_events_for_faculty(slot,subject_event,is_prac=False):
	# sees if there is another event of the same faculty for the slot
	# print(slot)
	e = get_or_none(classmodel = Event,Slot_id = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id)
	e = get_or_none(classmodel = Event,Slot_id_2 = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id) if not e else e
	if e:
		return -OTHER_EVENT_FACULTY
	return 0


def check_other_events_for_slot(all_events,slot,subject_event,batch=None,slot_below=None):
	# checks the slot to see if there is another event already or not
	if slot_below: # if practical
		e = all_events.filter(Slot_id = slot)
		e = all_events.filter(Slot_id = slot_below) if not e else e
		if e :	# if there is any event
			if not batch:	# if class_prac
				return OTHER_EVENT_SLOT
			if not e[0].Slot_id_2:		# if the event is a lecture
				return OTHER_EVENT_SLOT
			if e[0].Slot_id_2 and (not e[0].Batch_id or e.filter(Batch_id=batch)) :	
				# if the event is a practical and the batch is empty  or
				# if the event does not have a batch i.e. not div_prac
				# print("{}--{}".format(e,e.filter(Batch_id=batch)))
				return OTHER_EVENT_SLOT
	else:	# if lecture
		e = all_events.filter(Slot_id = slot)
		e = all_events.filter(Slot_id_2 = slot) if not e else e
		if e:
			if e[0].Slot_id_2:		# if there is a prac event
				return OTHER_EVENT_SLOT
			if batch:	# if there is a batch_lect
				if e.filter(Batch_id=batch):
					return OTHER_EVENT_SLOT
			else:	# if there is a class_lect
				return OTHER_EVENT_SLOT
	return 0


from tabulate import tabulate
########## Get-point functions for the events ##########


def get_point_for_prac_batch(subject_event,all_events,batch):
	day = None
	best_pair = [-math.inf,"",""]
	tab = []
	for slot in usable_slots:
		next_slot_point = points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filter(Slot_id__day = day)
		slot_below = get_slot_below(slot,day_slots)
		if slot_below:
			# print(type(batch))
			prac_event = day_events.filter(Slot_id = slot,Slot_id_2 = slot_below)
			points = check_availability(slot,subject_event)
			if points == 0:		# if it is available
				points += check_repetation(day_events,subject_event,True,batch)
				points += check_load_distribution(day_events,subject_event,True)
				points += check_other_events_for_faculty(slot,subject_event,True)
				points += check_other_events_for_slot(all_events,slot,subject_event,batch,slot_below)
			next_slot_point = check_availability(slot,subject_event)
			if next_slot_point == 0:		# if it is available
				next_slot_point += check_repetation(day_events,subject_event,True,batch)
				next_slot_point += check_load_distribution(day_events,subject_event,True)
				next_slot_point += check_other_events_for_faculty(slot,subject_event,True)

			points = min(points,next_slot_point)
			if prac_event and not prac_event.filter(Batch_id=batch) and prac_event[0].Batch_id:
				points += PRAC_ON_PRAC
			tab.append([slot,points,check_other_events_for_faculty(slot,subject_event,True)])
		if points > best_pair[0]:
			best_pair[0] = points
			best_pair[1] = slot
			best_pair[2] = slot_below
	# if batch and subject_event.pk == 29:
	# 	print(tabulate(tab,headers=["slot","point","Other_faculty_events"],tablefmt="grid"))
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
			day_events = all_events.filter(Slot_id__day = day)
		slot_below = get_slot_below(slot,day_slots)
		if slot_below:
			points = check_availability(slot,subject_event)
			if points == 0:		# if it is available
				points += check_repetation(day_events,subject_event,True)
				points += check_load_distribution(day_events,subject_event,True)
				points += check_other_events_for_faculty(slot,subject_event,True)
				points += check_other_events_for_slot(all_events,slot,subject_event,slot_below= slot_below)
			next_slot_point = check_availability(slot,subject_event)
			if next_slot_point == 0:		# if it is available
				next_slot_point += check_repetation(day_events,subject_event,True)
				next_slot_point += check_load_distribution(day_events,subject_event,True)
				next_slot_point += check_other_events_for_faculty(slot_below,subject_event,True)
			points = min(points,next_slot_point)
			tab.append([slot,points])
		if points > best_pair[0]:
			best_pair[0] = points
			best_pair[1] = slot
			best_pair[2] = slot_below
	# print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair


def get_point_for_lect_batch(subject_event,all_events,batch):
	day = None
	best_pair = [-math.inf,""]
	tab = []
	for slot in usable_slots:
		points = -math.inf
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
			day_events = all_events.filter(Slot_id__day = day)
		points = check_availability(slot,subject_event)
		lect_event = day_events.filter(Slot_id = slot,Slot_id_2 = None).exclude(Batch_id = None)
		if lect_event:
			print(lect_event)
		if points == 0:		# if it is available
			points += check_repetation(day_events,subject_event,batch = batch)
			points += check_load_distribution(day_events,subject_event)
			points += check_other_events_for_faculty(slot,subject_event)
			points += check_other_events_for_slot(all_events,slot,subject_event,batch)
			if lect_event and not lect_event.filter(Batch_id=batch):
				points += PRAC_ON_PRAC
		if points > best_pair[0]:
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
			day_events = all_events.filter(Slot_id__day = day)
		points = check_availability(slot,subject_event)
		if points == 0:		# if it is available
			points += check_repetation(day_events,subject_event)
			points += check_load_distribution(day_events,subject_event)
			points += check_other_events_for_faculty(slot,subject_event)
			points += check_other_events_for_slot(all_events,slot,subject_event)			
		if points > best_pair[0]:
			best_pair[0] = points
			best_pair[1] = slot
		tab.append([slot,points])
	if subject_event.pk == 29:
		print(tabulate(tab,headers=["slot","point"],tablefmt="grid"))
	return best_pair

########## gets the subject_event and the batch or none to place it ##########

l = []
def put_vars(Division_id):
	global WORKING_DAYS,usable_slots,l
	WORKING_DAYS = Working_days.objects.filter(Shift_id=Division_id.Shift_id).count()
	all_slots = Slots.objects.filter(Timing_id__Shift_id = Division_id.Shift_id).order_by("day")
	usable_slots = all_slots.exclude(Timing_id__is_break = True)
	l = []


def get_subject_events(Division_id,subject_event,is_prac,all_events,batch = None):
	points = 0
	best_slot = None
	slot_2 = None
	# won't work if all_event is null so pass shift_id here

	if is_prac:		# if the subject_event is practical
		if batch:	# if there is a batch for us to put it in
			l.append([subject_event, batch,"Practical"])
			print([subject_event, batch,"Practical"])
			points,best_slot,slot_2 = get_point_for_prac_batch(subject_event,all_events,batch)
			# print(subject_event,best_slot)
		else:		# if no batch
			l.append([subject_event,"Class","Practical"])
			print([subject_event,"Class","Practical"])
			points,best_slot,slot_2 = get_point_for_prac_class(subject_event,all_events)
			# print(points,best_slot)
	else:			# if the subject_event is lecture
		if batch:	# if there is a batch for us to put it in
			l.append([subject_event,batch,"Lecture"])
			print([subject_event,batch,"Lecture"])
			points,best_slot = get_point_for_lect_batch(subject_event,all_events,batch)
		else:		# if no batch
			l.append([subject_event,"Class","Lecture"])
			print([subject_event,"Class","Lecture"])
			points,best_slot = get_point_for_lect_class(subject_event,all_events)
	print("Slot_id :: {} \n Point :: {}\n -----------------------------".format(best_slot,points))
	return Event.objects.create(Slot_id = best_slot, Slot_id_2 = slot_2, Division_id_id = Division_id, Batch_id = batch, Subject_event_id = subject_event).pk
	# return points,best_slot


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