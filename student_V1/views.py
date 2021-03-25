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
from django.core.mail import send_mail

def get_events_json(qs):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		this = qs.get(pk = d['pk'])
		d["start_time"] = str(this.Slot_id.Timing_id.start_time)
		if this.Slot_id_2:  # if practical
			d["end_time"] = str(this.Slot_id_2.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id) + " Practical"
			# d["link"] = if this. this.Batch_id.link
		else:			# if lecture
			d["end_time"] = str(this.Slot_id.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id)
			# d["link"] = this.Division_id.link
		d["link"] = this.link
		# print(d["link"])
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

import student_V1.forms as _
import datetime

mail_body_template = """
Feedback for {} teaching the subject {}({}) has been submitted from {} ({},{},{}).

The following has been quoted by the student :- 
"{}"

This mail was sent by horarium.The views and opinions included in this quote belong to their author and do not necessarily mirror the views and opinions of the company.
"""
mail_subject_template = """Feedback for {} from {} ({},{},{})"""
# faculty,user name, department,semester,enno 
@login_required(login_url="login")
@allowed_users(allowed_roles=['Student'])
def student_home(request):
	student_name = request.user
	student_details = request.user.student_details
	semester = student_details.Division_id.Semester_id
	department = semester.Branch_id.Department_id
	enno = student_details.roll_no
	print("asd")
	if request.method == 'POST':
		form = _.feedback_form(request.POST)
		# print(form)
		if form.is_valid():
			candidate = form.save(commit=False)
			event = form.instance.Event_id
			end_slot = event.Slot_id_2 if event.Slot_id_2 else event.Slot_id
			end_time = end_slot.Timing_id.end_time
			ct = datetime.datetime(year=1990, month=1, day=1,hour=9,minute=14,second=1).time()
			# testing 
			# ct = datetime.datetime.now().time()
			end = datetime.datetime(2000, 1, 1,hour=end_time.hour, minute=end_time.minute, second=end_time.second)
			if (end-datetime.timedelta(minutes=2)).time() < ct < (end+datetime.timedelta(minutes=5)).time() and request.POST['query']:
				event = candidate.Event_id
				faculty_name = event.Subject_event_id.Faculty_id.User_id
				subject_name = event.Subject_event_id.Subject_id.name
				event_type = "Practical" if event.Slot_id_2 else "Lecture"
				# message_name = request.POST['message_name']
				message_name = mail_subject_template.format(faculty_name,student_name,department,semester,enno)
				# message_name = "mail_subject_template.format()"
				# print()
				message = mail_body_template.format(faculty_name,subject_name,event_type,student_name,department,semester,enno,request.POST['query'])
				# message = 				
				if message:
					send_mail(
						message_name, #subject
						message, #message
						from_email = None, # from email 
						recipient_list = ['yogeshrathod19@gnu.ac.in'] # to email
					)
					# pass
			else :
				print("hello")
			candidate.Given_by = request.user
			# print((end-datetime.timedelta(minutes=2)).time()," - ",ct," - ",(end+datetime.timedelta(minutes=5)).time())
			candidate.save()
			# if candidate.Event_id
			# candidate.Event_id = 




	student = request.user.student_details
	my_shift = student.Division_id.Shift_id
	my_events = Event.objects.filter(Q(Batch_id=student.Batch_id) | Q(Batch_id=None),Division_id=student.Division_id)
	day = ""
	questions = [
		"Lecture or Lab Session Began and End on scheduled Time",
		"I felt the Teacher well prepared for this particular session",
		"The Pedagogy (Teaching methods) of the Teacher is effective",
		"I am able to learn the topic effectively and with clear understanding",
		"The teacher encourages students to ask questions for better understanding",
		"If asked, the teacher answers all questions appropriately and clearly",
		"The Teacher has excellent knowledge about the subject ",
		"The teacher's behaviour is respectful and treats all students respectfully",
		"I don't hesitate to ask to the Teacher if I have any doubt",
	]
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
		'questions' : questions,
	}
	if day:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=day))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=day))
	else:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=date.today().strftime("%A")))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A")))
	return render(request,"Student/student_v1.html",context)

def sendMail(request) :
	if request.method == "POST" :
		message_name = request.POST['message_name']
		# message_name = "Hello"
		message_email = request.POST['message']
		# message_email = "yogeshrathod19@gnu.ac.in"
		message = request.POST['message']

		send_mail(
			message_name, #subject
			message, #message
			message_email, # from email 
			['yogeshrathod19@gnu.ac.in'] # to email
		)
		return render(request,'Student/submitted.html',{'message':message})	
	else : 
		return render(request,'Student/submitted.html', {})