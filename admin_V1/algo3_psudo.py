# keep the main function in the same folder

main_list = []
json_events = json.loads(request.body)
for i in json_events:
	del i['locked']
	form = add_event(i)
	candidate = form.save(commit=False)
	candidate.Division_id_id = Division_id
	main_list.append(candidate)
	# add all the locked events to main_list

# get all the subjects that can be merged
# merged_subjects =

priority_list = []

while not_infinite:
	get_sorted_events(subject_events,locked_events,priority_list)

	if infinite:
		priority_list.append(subject_causing_infinite)

##############################################

def get_sorted_events(subject_events,locked_events,priority_list): 
	events = []
	my_dict = {}
	for subject_event in all_subject_events:
		t = len(Not_available.objects.filter(Faculty_id = subject_event.Faculty_id))
		t += len(Event.objects.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		if locked_events:
			t += len(locked_events.filter(Subject_event_id__Faculty_id=subject_event.Faculty_id))
		# t =  length of all not_available
		# t += length of all the events of faculty
		# t += same events in the locked_events
		my_dict[subject_event] = t
	# now sort by decending order of t
	# now make a list of sorted events 
	my_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
	for i in my_dict:
		events.append(i[0])
	final_list = [i for i in events if i not in priority_list]
	for e in priority_list:
		for i in events:
			if i == e:
				final_list = [i] + final_list
	# set according to priority list 
	# PL = [more,most]
	# final_list = [most,more,...]
	return final_list
	
				
# if mearge is available then we should make events
# for those in slots for all the batches it is 
# associated with 

# DWM is checked to merge
# for all slots 
# check if any events there doesn't have the same
# batches and if not give it rating accordingly 
# for the best slot put event for all the associated
# batches in that slot

# for i in sorted_events:
	points,event = get_point_event()
	