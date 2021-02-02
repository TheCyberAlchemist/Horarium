import math
from django.core.exceptions import ObjectDoesNotExist
from institute_V1.models import Slots,Working_days
from faculty_V1.models import Not_available,Faculty_load
from Table_V2.models import *
REPETATION_WEIGHT = -8
# NO_REPETATION_WEIGHT = 4
OTHER_EVENT = 12
LOAD_IS_MORE = 3
NOT_AVAILABLE = -math.inf


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

def check_load_distribution(day,subject_event):
	# returns -3(delta) if the load is more then the average load per day
	same_events = Event.objects.filter(Subject_event_id__Faculty_id = subject_event.Faculty_id,Slot_id__day = day)
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

def check_other_events(slot,subject_event):
	e = get_or_none(classmodel = Event,Slot_id = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id)
	e = get_or_none(classmodel = Event,Slot_id_2 = slot,Subject_event_id__Faculty_id = subject_event.Faculty_id) if not e else e
	if e:
		return -OTHER_EVENT
	return 0

def get_points(subject_event,all_events,is_prac):
	point_dict = {}
	all_slots = Slots.objects.filter(Timing_id__Shift_id = all_events[0].Slot_id.Timing_id.Shift_id).exclude(Timing_id__is_break = True).order_by("day")
	prac,lect = subject_event.prac_carried,subject_event.lect_carried
	day = None
	for slot in all_slots:
		if slot.day != day:
			day = slot.day
			day_slots = all_slots.filter(day = day)
		# should use filter as two practicals can be on the same slot
		e = all_events.filter(Slot_id = slot) | all_events.filter(Slot_id_2 = slot)
		
		if e and e[0].Batch_id:	# if there is a batch on the slot
			print("here")
		elif not e:		# if there is not an event on that slot
			points = 0
			day_events = all_events.filter(Slot_id__day = day)
			points += check_availability(slot,subject_event)
			if points == 0:		# if it is available
				points += check_repetation(day_events,subject_event,is_prac)
				points += check_load_distribution(day,subject_event)
				points += check_other_events(slot,subject_event)
			point_dict[slot.pk] = points
	return point_dict
	# for slot in Slots.objects.filter(Timing_id = all_events[0].Slot_id.Timing_id):
	# 	print(slot)
	# for event in all_events:
	# 	if event.Subject_event_id == subject_event:
	# 		print(event)
