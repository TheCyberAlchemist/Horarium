from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta as timedelta
from rest_framework.response import Response
from calendar import monthrange,month_name
from rest_framework.views import APIView
from datetime import datetime as date
from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
import calendar
import json
import math

from faculty_V1.models import Faculty_details,Feedback_type,Feedback,Can_teach
from institute_V1.models import Slots,Timings,Shift,Working_days
from login_V2.decorators import allowed_users,unauthenticated_user,get_home_page
from django.contrib.auth.decorators import login_required
from subject_V1.models import Subject_event
from Table_V2.models import Event
from student_V1.models import Student_logs
# Create your views here.

def get_events_json(qs):
	data = serializers.serialize("json", qs)
	data = json.loads(data)
	for d in data:
		this = qs.get(pk = d['pk'])
		d["start_time"] = str(this.Slot_id.Timing_id.start_time)
		if this.Slot_id_2:
			d["end_time"] = str(this.Slot_id_2.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id) + " Practical"
		else:
			d["end_time"] = str(this.Slot_id.Timing_id.end_time)
			d["name"] = str(this.Subject_event_id.Subject_id)
		d["link"] = this.link
		d["resource"] = str(this.Resource_id)
		del d['model'],d['fields']
	# print(qs)
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['Faculty'])
def faculty_home(request):
	# for i in Slots.objects.filter(day=2):
	faculty = request.user.faculty_details
	my_shift = faculty.Shift_id
	my_events = Event.objects.filter_faculty(faculty)
	day = ""
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
		'faculty_detail':faculty,
	}
	if day:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=day))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=day))
	else:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=date.today().strftime("%A")))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A")))	
	
	ip = request.META.get('REMOTE_ADDR')
	Student_logs.objects.create(
		user_id = request.user,
		action='Faculty Details called',
		ip=ip,
	)
	return render(request,"Faculty/faculty_v1.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Faculty'])
def faculty_settings(request) :
	user = request.user
	faculty = user.faculty_details
	context = {
		"my_email":user.email,
		"my_institute":faculty.Department_id.Institute_id,
		"my_department":faculty.Department_id,
		"my_designation":faculty.Designation_id,
		"my_load":faculty.faculty_load,
	}
	subj_str = ""
	for can_teach in Can_teach.objects.all().filter(Faculty_id=faculty):
		subj_str +=  f"{can_teach.Subject_id} ,"
	if len(subj_str) > 2 :
		subj_str = subj_str[0:-1]
	context["my_subjects"] = subj_str
	return render(request,'AccountSetting/faculty_settings.html',context)	

def faculty_feedback(request,Faculty_id = None) :
	subject_events_list = []
	subjects_list = []
	if Faculty_id:	# if called by admin_dashboard
		# get the faculty_id from the user_id and then filter by function
		subject_events =  Subject_event.objects.active().filter(Q(Faculty_id__User_id=Faculty_id)|Q(Co_faculty_id__User_id=Faculty_id))
	else:
		subject_events =  Subject_event.objects.filter_faculty(request.user.faculty_details)
	# print(subject_events)
	for subject_event in subject_events:
		subject_events_list.append({'Subject_name':str(subject_event.Subject_id),"id":subject_event.pk})
		subjects_list.append({'Subject_name':str(subject_event.Subject_id),"id":subject_event.Subject_id_id})
	# data = json.loads(data)
	my_types = {}
	my_types_list = []
	for i in subject_events:
		# print(i.Subject_id.Semester_id)
		my_types_filtered = Feedback_type.objects.past().filter(WEF = i.Subject_id.Semester_id.WEF_id).union(Feedback_type.objects.present().filter(WEF = i.Subject_id.Semester_id.WEF_id))
		my_types[i.pk] = my_types_filtered
		for j in my_types_filtered:
			my_types_list.append({'type_name':str(j.name),'id':j.pk})
	print(my_types_list)

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
		'is_admin':bool(Faculty_id),
		'subject_events_json': json.dumps(subject_events_list),
		'subjects_json':json.dumps(subjects_list),
		'subject_events':subject_events,
		'my_types':my_types,
		'my_types_json':json.dumps(my_types_list),
		'questions' : questions,
	}
	return render(request,"Faculty/feedback.html",context)

def monthlist_fast(dates):
    start, end = [date.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    mlist = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        mlist.append(date(y, m+1, 1))
    return mlist

def transpose(l1):
    l2 = list(map(list, zip(*l1)))
    return l2

def get_ave_len(qs,debug = False):
	# Q1 = Q2 = Q3 = Q4 = Q5 = Q6 = Q7 = Q8 = Q9 = []
	Q = []
	Questions = list(qs.values_list("Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9"))
	ave = [0 for _ in range(9)]
	length = [0 for _ in range(9)]
	# arr = np.array(Questions)
	# arr = arr.transpose()
	Questions = transpose(Questions)
	for i in range(len(Questions)):
		temp = [int(x) for x in Questions[i] if x != None]
		if temp:
			ave[i] = round(sum(temp)/len(temp),2)
			length[i] = len(temp)
			if debug:
				print(round(sum(temp)/len(temp),2),len(temp))
	if debug:
		print(ave,length)
	return ave,length


class average_all_questions(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format = None):
		labels = ['Q1', 'Q2', 'Q3', 'Q4','Q5','Q6','Q7','Q8','Q9']
		chartLabel = 'Overall Feedback'
		all_feedbacks = Feedback.objects.all().filter(Subject_event_id=request.GET['id'])
		chartdata,feedback_counts = get_ave_len(all_feedbacks)
		data ={
			"labels":labels,
			"chartLabel":chartLabel,
			"chartdata":chartdata,
			"feedback_counts":feedback_counts,
		}
		###################### on click ######################
		return Response(data)

class mandatory_feedbacks(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format = None):
		my_type = Feedback_type.objects.all().get(pk=request.GET['id'])
		labels = ['Q1', 'Q2', 'Q3', 'Q4','Q5','Q6','Q7','Q8','Q9']
		chartLabel = my_type.name
		all_feedbacks = my_type.feedback_set.all()
		chartdata,_ = get_ave_len(all_feedbacks)
		data ={
			"labels":labels,
			"chartLabel":chartLabel,
			"chartdata":chartdata,
			"feedback_count":all_feedbacks.count(),
		}
		###################### on click ######################
		return Response(data)

class feedback(APIView):
	# authentication_classes = []
	# permission_classes = []
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format = None):
		########################## general decleration ######################
		# print(request.GET)
		subject_event = Subject_event.objects.active().get(pk = request.GET['id'])
		# print(subject_event)
		wef = subject_event.Subject_id.Semester_id.WEF_id
		all_feedback  = Feedback.objects.filter(Subject_event_id = subject_event)
		list_of_months = monthlist_fast([str(wef.start_date),str(wef.end_date)])
		Que1 ,Que2 ,Que3 ,Que4 ,Que5 ,Que6 ,Que7 ,Que8 ,Que9 = ([] for i in range(9))
		length1 ,length2 ,length3 ,length4 ,length5 ,length6 ,length7 ,length8 ,length9 = ([] for i in range(9))

		###################### if Graph name ######################
		if 'graph_name' in request.GET:
			current_graph,required_value = request.GET['graph_name'].split()
			# print(request.GET['graph_name'])
			if current_graph == "week_rating":
				start_date,end_date = required_value.split("_")
				chartLabel ="Average Rating"
				labels = [
				]
				chartdata = []
				# ids = []
				delta = timedelta(1)
				s_d = date.strptime(start_date, '%Y-%m-%d')
				for i in range(7):
					labels.append(s_d.strftime("%d-%m (%a)"))
					# print(s_d.strftime("%d-%m-%Y"))
					day_feedback = all_feedback.filter(timestamp__date=s_d)
					[q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9],[l1, l2, l3, l4, l5, l6, l7, l8, l9] = get_ave_len(day_feedback)
					Que1.append(q1)
					length1.append(l1)
					Que2.append(q2)
					length2.append(l2)
					Que3.append(q3)
					length3.append(l3)
					Que4.append(q4)
					length4.append(l4)
					Que5.append(q5)
					length5.append(l5)
					Que6.append(q6)
					length6.append(l6)
					Que7.append(q7)
					length7.append(l7)
					Que8.append(q8)
					length8.append(l8)
					Que9.append(q9)
					length9.append(l9)
					# print("total - {}".format(day_feedback.count()))
					arr = list(day_feedback.values_list("average",flat=True))
					arr = [x for x in arr if x != 0]
					day_ave = 0
					if arr:
						day_ave = round(sum(arr)/len(arr),2)
					# ids.append("{}_{}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
					chartdata.append(day_ave)
					temp = s_d + delta
					if s_d.month==temp.month:
						s_d = temp 
					else :
						break
					
				# print(chartdata)
				data = {
					"labels":labels,
					"chartLabel":chartLabel,
					"chartdata":chartdata,
					"Q1":Que1,"len1":length1,
					"Q2":Que2,"len2":length2,
					"Q3":Que3,"len3":length3,
					"Q4":Que4,"len4":length4,
					"Q5":Que5,"len5":length5,
					"Q6":Que6,"len6":length6,
					"Q7":Que7,"len7":length7,
					"Q8":Que8,"len8":length8,
					"Q9":Que9,"len9":length9,
					"button_name":"month_rating {}".format(s_d.strftime("%B_%Y")),
					"button_id" : '#show_week__%s'%(request.GET['id']),
				}
				return Response([data,'day_rating__%s'%(request.GET['id'])]) # data and next chart_id
			elif current_graph == "month_rating": 	# see weekly rating
				chartLabel = "Average Rating"
				labels = [
					'1-7',
					'8-14', 
					'15-21', 
					'22-28'
				]
				chartdata = []
				ids = []
				###################### data process ######################
				# wrong output
				datetime_object = date.strptime(required_value, "%B_%Y")
				month_number = datetime_object.month
				year = datetime_object.year
				_,days_in_months = monthrange(year, month_number)
				# print(month_number)
				if days_in_months > 28:		# for the last week
					labels.append('29-{}'.format(days_in_months))
				for i in labels:
					dates = i.split('-')
					start_date = date.strptime('{}-{}-{}'.format(year,month_number,dates[0]),"%Y-%m-%d")
					end_date = date.strptime('{}-{}-{} 23:59:59'.format(year,month_number,dates[1]),"%Y-%m-%d %H:%M:%S")
					week_feedback = all_feedback.filter(timestamp__date__gte=start_date, timestamp__date__lt=end_date)
					[q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9],[l1, l2, l3, l4, l5, l6, l7, l8, l9] = get_ave_len(week_feedback)
					Que1.append(q1)
					length1.append(l1)
					Que2.append(q2)
					length2.append(l2)
					Que3.append(q3)
					length3.append(l3)
					Que4.append(q4)
					length4.append(l4)
					Que5.append(q5)
					length5.append(l5)
					Que6.append(q6)
					length6.append(l6)
					Que7.append(q7)
					length7.append(l7)
					Que8.append(q8)
					length8.append(l8)
					Que9.append(q9)
					length9.append(l9)
					# print("total - {}".format(week_feedback.count()))
					arr = list(week_feedback.values_list("average",flat=True))
					arr = [x for x in arr if x != 0]
					week_ave = 0
					if arr:
						week_ave = round(sum(arr)/len(arr),2)
					ids.append("{}_{}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
					chartdata.append(week_ave)
				data ={
					"labels":labels,
					"ids":ids,
					"chartLabel":chartLabel,
					"chartdata":chartdata,
					"Q1":Que1,"len1":length1,
					"Q2":Que2,"len2":length2,
					"Q3":Que3,"len3":length3,
					"Q4":Que4,"len4":length4,
					"Q5":Que5,"len5":length5,
					"Q6":Que6,"len6":length6,
					"Q7":Que7,"len7":length7,
					"Q8":Que8,"len8":length8,
					"Q9":Que9,"len9":length9,
					"button_name":"get_semester_rating junk",
					"button_id" : '#show_semester__%s'%(request.GET['id']),
				}
				return Response([data,'week_rating__%s'%(request.GET['id'])]) # data and next chart_id
			elif current_graph == "get_semester_rating":
				###################### month rating ##########################
				labels = []
				chartLabel = "Average Rating"
				chartdata = []
				ids = []

				for i in list_of_months:
					labels.append(month_name[i.month])
					ids.append(i.strftime("%B_%Y"))
					month_feedback = all_feedback.filter(timestamp__month=i.month)
					[q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9],[l1, l2, l3, l4, l5, l6, l7, l8, l9] = get_ave_len(month_feedback)
					Que1.append(q1)
					length1.append(l1)
					Que2.append(q2)
					length2.append(l2)
					Que3.append(q3)
					length3.append(l3)
					Que4.append(q4)
					length4.append(l4)
					Que5.append(q5)
					length5.append(l5)
					Que6.append(q6)
					length6.append(l6)
					Que7.append(q7)
					length7.append(l7)
					Que8.append(q8)
					length8.append(l8)
					Que9.append(q9)
					length9.append(l9)
					# print("month {}->{}".format(i.month,month_feedback.count()))
					arr = list(month_feedback.values_list("average",flat=True))
					arr = [x for x in arr if x != 0]
					month_ave = 0
					if arr:
						month_ave = round(sum(arr)/len(arr),2)
					chartdata.append(month_ave)
				
				data ={
					"labels":labels,
					'ids':ids,
					"chartLabel":chartLabel,
					"chartdata":chartdata,
					"Q1":Que1,"len1":length1,
					"Q2":Que2,"len2":length2,
					"Q3":Que3,"len3":length3,
					"Q4":Que4,"len4":length4,
					"Q5":Que5,"len5":length5,
					"Q6":Que6,"len6":length6,
					"Q7":Que7,"len7":length7,
					"Q8":Que8,"len8":length8,
					"Q9":Que9,"len9":length9,
				}
				return Response([data,'month_rating__%s'%(request.GET['id'])])
		
		###################### default day view #####################
		chartLabel ="Average Rating"
		labels = []
		chartdata = []
		delta = timedelta(1)
		today = date.now()
		week_number = math.ceil(today.day/7) - 1 # get the week number of the date
		if week_number == 0:	# if it is first week 
			s_d = today.replace(day=1)
		else:
			s_d = today.replace(day=week_number*7) + delta
		# s_d = date.strptime(start_date, '%Y-%m-%d')
		for i in range(7):
			labels.append(s_d.strftime("%d-%m (%a)"))
			day_feedback = all_feedback.filter(timestamp__date=s_d)
			[q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9],[l1, l2, l3, l4, l5, l6, l7, l8, l9] = get_ave_len(day_feedback)

			Que1.append(q1)
			length1.append(l1)
			Que2.append(q2)
			length2.append(l2)
			Que3.append(q3)
			length3.append(l3)
			Que4.append(q4)
			length4.append(l4)
			Que5.append(q5)
			length5.append(l5)
			Que6.append(q6)
			length6.append(l6)
			Que7.append(q7)
			length7.append(l7)
			Que8.append(q8)
			length8.append(l8)
			Que9.append(q9)
			length9.append(l9)
			arr = list(day_feedback.values_list("average",flat=True))
			arr = [x for x in arr if x != 0]
			day_ave = 0
			if arr:
				day_ave = round(sum(arr)/len(arr),2)
			# ids.append("{}_{}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
			chartdata.append(day_ave)
			temp = s_d + delta
			if temp.month == s_d.month:
				s_d = temp
			else:
				break
		# print("graph_name {}".format(today.strftime("%B_%Y")))
		data ={
			"labels":labels,
			"chartLabel":chartLabel,
			"Q1":Que1,"len1":length1,
			"Q2":Que2,"len2":length2,
			"Q3":Que3,"len3":length3,
			"Q4":Que4,"len4":length4,
			"Q5":Que5,"len5":length5,
			"Q6":Que6,"len6":length6,
			"Q7":Que7,"len7":length7,
			"Q8":Que8,"len8":length8,
			"Q9":Que9,"len9":length9,
			"button_name":"month_rating {}".format(today.strftime("%B_%Y")),
			"button_id" : '#show_week__%s'%(request.GET['id']),
			"chartdata":chartdata,
		}
		###################### on click ######################
		return Response([data,'day_rating__%s'%(request.GET['id'])])

def attendance(request):
	return render(request,"Faculty/Attendance/attendance.html")