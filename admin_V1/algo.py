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

def check_repetation(day_events,subject_event,is_prac):
	if is_prac:
		repetation = day_events.filter(Subject_event_id = subject_event).exclude(Slot_id_2 = None)		
	else:
		repetation = day_events.filter(Subject_event_id = subject_event,Slot_id_2 = None)
	if repetation:
		return REPETATION_WEIGHT * len(repetation)
	return 0

def check_availability(slot,subject_event):
	# returns -inf if the faculty is not available at that spot
	if get_or_none(Not_available,None,Faculty_id=subject_event.Faculty_id,Slot_id=slot):
		return NOT_AVAILABLE
	else:
		return 0

def check_load_distribution(day_events,subject_event):
	# returns -3(delta) if the load is more then the average load per day
	# same_events = Event.objects.filter(Subject_event_id__Faculty_id = subject_event.Faculty_id,Slot_id__day = day)
	same_events = day_events.filter(Subject_event_id__Faculty_id = subject_event.Faculty_id)
	todays_load = 0
	for event in same_events:
		if event.Slot_id_2:
			todays_load += 2
		else:
			todays_load += 1
	faculty_load = Faculty_load.objects.get(Faculty_id = subject_event.Faculty_id)
	ave_load = math.ceil((faculty_load.total_load - faculty_load.remaining_load())/len(Working_days.objects.filter(Shift_id=subject_event.Faculty_id.Shift_id)))
	delta = todays_load - ave_load + 1
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

def get_next_slot(slot,day_slots):
	next_slot = day_slots.get(Timing_id__start_time = slot.Timing_id.end_time)
	if next_slot:
		return next_slot
	return False

def check_slot_below(slot,day_slots):
	# print(day_slots)
	return 0

def get_points(subject_event,all_events,is_prac):
	point_dict = {}
	# won't work if ell_event is null so pass shift_id here
	all_slots = Slots.objects.filter(Timing_id__Shift_id = all_events[0].Slot_id.Timing_id.Shift_id).order_by("day")
	usable_slots = all_slots.exclude(Timing_id__is_break = True)
	prac,lect = subject_event.prac_carried,subject_event.lect_carried
	all_batches = Batch.objects.filter(Division_id=all_events[0].Division_id,batch_for="prac" if is_prac else "lect")
	# print(all_batches)
	# gets all the batches of lecture ar prac 
	day = None
	f_o = False
	for slot in usable_slots:
		if slot.day != day:		# changes the day_slot 
			day = slot.day
			day_slots = usable_slots.filter(day = day)
		
		# should use filter as two practicals can be on the same slot
		e = all_events.filter(Slot_id = slot) | all_events.filter(Slot_id_2 = slot)
		points = 0
		day_events = all_events.filter(Slot_id__day = day)
		if e and e[0].Batch_id:	# if there is a batch on the slot
			if e[0].Slot_id_2:	# if it is a practical slot
				if f_o:		# if it is the second slot 
					points = SLOT_BELOW
					f_o = False
				else:		# if it is the first slot
					f_o = True
					remaining_batches = all_batches.exclude(pk__in = e.values_list("Batch_id_id",flat=True))
					point_dict[slot.pk] = []
					for batch in remaining_batches:
						points += check_availability(slot,subject_event)
						if points == 0:		# if it is available
							points += check_repetation(day_events,subject_event,is_prac)
							points += check_load_distribution(day_events,subject_event)
							points += check_other_events(slot,subject_event)
							next_slot = get_next_slot(slot,day_slots)
							points += check_other_events(next_slot,subject_event) if next_slot else 0
							points += PRAC_ON_PRAC	
						# point_dict[slot.pk].append((batch,points))
				point_dict[slot.pk] = points
		elif not e:		# if there is not an event on that slot
			points += check_availability(slot,subject_event)
			if points == 0:		# if it is available
				if is_prac:
					points += check_slot_below(day_events,subject_event)
				points += check_repetation(day_events,subject_event,is_prac)
				points += check_load_distribution(day_events,subject_event)
				points += check_other_events(slot,subject_event)
			point_dict[slot.pk] = points
	if is_prac:
		# best_slot_pk = max(point_dict,key=point_dict.get)
		# best_slot = all_slots.get(pk = best_slot_pk)
		print(point_dict[43])
		# pass
	return point_dict
	# for slot in Slots.objects.filter(Timing_id = all_events[0].Slot_id.Timing_id):
	# 	print(slot)
	# for event in all_events:
	# 	if event.Subject_event_id == subject_event:
	# 		print(event)

def put_event(subject_event,all_events,is_prac):
	print(is_prac)
	return get_points(subject_event,all_events,is_prac)


def get_sorted_events(all_subject_events,locked_events = Event.objects.none()):
	events = []
	my_dict = {}
	for subject_event in all_subject_events:
		t = len(Not_available.objects.filter(Faculty_id = subject_event.Faculty_id))
		t += len(Event.objects.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		t += len(locked_events.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		my_dict[subject_event] = t

	my_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
	for i in my_dict:
		events.append(i[0])
	return events