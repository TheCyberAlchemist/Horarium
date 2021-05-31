from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from student_V1.forms import * 
from subject_V1.models import Subject_details,Subject_event
from student_V1.models import Student_details
from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from Table_V2.models import Event
from institute_V1.models import Slots,Timings,Shift,Working_days,Batch
from faculty_V1.models import Feedback,Feedback_type

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

def one_selected(instance):
	'returns True if one question is selected or query is filled'
	a = instance.Q1 or instance.Q2 or instance.Q3 or instance.Q4 or instance.Q5 or instance.Q6 or instance.Q7 or instance.Q8 or instance.Q9 or instance.query
	if a:
		return True
	return False


mail_body_template = """Feedback for {} teaching the subject {}({}) has been submitted from {} ({},{},{}).
The following has been quoted by the student :- 
"{}"

This mail was sent by horarium.The views and opinions included in this quote belong to their author and do not necessarily mirror the views and opinions of the company.
"""
mail_subject_template = """Feedback for {} from {} ({},{},{})"""
def send_regular_email(user,my_subject_event,my_event,query):	
	'send email for regular feedback query'
	student_name = user
	student_details = user.student_details
	semester = student_details.Division_id.Semester_id
	department = semester.Branch_id.Department_id
	enno = student_details.roll_no
	subject_name = my_subject_event.Subject_id
	faculty_name = my_subject_event.Faculty_id.User_id
	event_type = "Practical" if my_event.Slot_id_2 else "Lecture"

	subject =  mail_subject_template.format(faculty_name,student_name,department,semester,enno)
	body = mail_body_template.format(faculty_name,subject_name,event_type,student_name,department,semester,enno,query)
	if body:
		send_mail(
			subject, #subject
			body, #message
			from_email = None, # from email 
			recipient_list = ['devmpatel19@gnu.ac.in'] # to email
		)
	# print(subject,body)

def send_mandatory_email():
	'send email for mandatory feedback query'
	pass

# faculty,user name, department,semester,enno 
@login_required(login_url="login")
@allowed_users(allowed_roles=['Student'])
def student_home(request):
	if request.method == 'POST':
		my_event = Event.objects.all().get(pk = request.POST['Event_id'])
		my_subject_event = my_event.Subject_event_id
		form = feedback_form(request.POST.copy())
		# print(request.POST)
		if form.is_valid():
			candidate = form.save(commit=False)
			if not one_selected(candidate) or str(my_event.Slot_id.day) != datetime.date.today().strftime("%A"):
				# if nothing is submitted
				# or the event is not on the same day as today
				return render(request,"Student/student_v1.html",context)
			candidate.Subject_event_id = my_subject_event
			candidate.Given_by = request.user
			if candidate.query:
				send_regular_email(request.user,my_subject_event,my_event,request.POST['query'])
			candidate.save()

	get_all_subjects_of_student(request)
	fill_mandatory_feedback(request)
	student = request.user.student_details
	my_shift = student.Division_id.Shift_id
	my_events = Event.objects.filter(Q(Batch_id=student.prac_batch)|Q(Batch_id=student.lect_batch)| Q(Batch_id=None),Division_id=student.Division_id)
	day = "Monday"
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
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=datetime.datetime.today().strftime("%A")))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=datetime.datetime.today().strftime("%A")))
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
			['devmpatel19@gnu.ac.in'] # to email
		)
		return render(request,'Student/submitted.html',{'message':message})	
	else : 
		return render(request,'Student/submitted.html', {})

class subject_serializer(serializers.python.Serializer):
	def end_object( self, obj ):
		self._current['id'] = obj._get_pk_val()
		include_list = ["id","name","short"]
		res = dict([(key, val) for key, val in self._current.items() if key in include_list]) 
		for i in res:
			if not res[i]:
				res[i] = ""
		self.objects.append( res )

def get_all_subjects_of_student(request):
	''' returns all the subjects to be filled for the mandatory feedback and the feedback_type in the last element'''
	my_subjects = []
	student = request.user.student_details
	my_feedback_type = Feedback_type.objects.present().filter(WEF=student.Division_id.Semester_id.WEF_id)
	data = []
	if my_feedback_type.count():
		my_batches = {student.prac_batch,student.prac_batch}

		all_sub = Subject_details.objects.all().filter(Semester_id = student.Division_id.Semester_id)
		done_subjects = Feedback.objects.special().filter(Given_by=request.user,Feedback_type=my_feedback_type[0]).values_list("Subject_id")
		remaining_subjects = all_sub.exclude(pk__in=done_subjects)

		for i in remaining_subjects:
			subject_batches = set(i.batch_set.all())
			if len(subject_batches) == 0:
				# if the subject has no batches
				my_subjects.append(i)
				continue
			if my_batches.intersection(subject_batches):
				# if the batches of the subject has the student's batch
				my_subjects.append(i)
				continue
		data = subject_serializer().serialize(my_subjects)
		data.append({'feedback_type':str(my_feedback_type[0].pk)})
		print(data)
	return JsonResponse(data, safe=False)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Student'])	
def fill_mandatory_feedback(request):
	if request.method == 'POST':
		my_feedback_type = Feedback_type.objects.active().filter(pk = request.POST['Feedback_type']).first()
		if my_feedback_type.active:
			my_subject = Subject_details.objects.get(pk=request.POST['Subject_id'])
			form = feedback_form(request.POST.copy())
			if form.is_valid():
				candidate = form.save(commit=False)
				candidate.Subject_id = my_subject
				candidate.Feedback_type = my_feedback_type
				candidate.Given_by = request.user
				if candidate.query:
					send_mandatory_email(request.user,my_subject_event,my_event,request.POST['query'])
				candidate.save()
		

# get_all_subjects_of_student()



from .forms import add_student_form
from django.views.generic.edit import FormView
from .models import Student_details


import base64

from django.core.files.base import ContentFile
def add_student(request):
	instance = Student_details.objects.get(User_id__first_name='Dev')
	form = add_student_form(instance = instance)
	# print (dict(form.instance))
	if request.method == 'POST':
		# print(form.fields['display_image'])
		form = add_student_form(request.POST,request.FILES, instance = instance)
		# print(form.fields['display_image'])
		# if not request.POST['display_image']:
		# 	format, imgstr = request.POST['img_str'].split(';base64,') 
		# 	ext = format.split('/')[-1] 
		# 	data = ContentFile(base64.b64decode(imgstr))
		# 	file_name = "%s.%s" % (form.instance.User_id,ext)
		# 	# print(request.POST)
		# 	form.instance.display_image.save(file_name, data)
		# 	# obj.display_image.save(file_name, data, save=True)
		# 	# print(form)
		if form.is_valid():
			form.save()
			print("here")
		
	return render(request,'/try/asd.html',{'form':form})