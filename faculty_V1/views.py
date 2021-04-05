from django.shortcuts import render
from django.core import serializers
import json
from datetime import timedelta as timedelta
from datetime import datetime as date
import calendar
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from calendar import monthrange,month_name
import math

from faculty_V1.models import Faculty_details, Chart
from Table_V2.models import Event
from institute_V1.models import Slots,Timings,Shift,Working_days

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


def faculty_home(request):
	# for i in Slots.objects.filter(day=2):
	faculty = request.user.faculty_details
	my_shift = faculty.Shift_id
	my_events = Event.objects.filter(Subject_event_id__Faculty_id = faculty)
	day = ""
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
	}
	if day:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=day))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=day))
	else:
		context['events_json'] = get_events_json(my_events.filter(Slot_id__day__Days_id__name=date.today().strftime("%A")))
		context['break_json'] = get_break_json(Slots.objects.filter(Timing_id__Shift_id=my_shift,Timing_id__is_break = True,day__Days_id__name=date.today().strftime("%A")))	
	
	return render(request,"Faculty/faculty_v1.html",context)


from faculty_V1.models import Feedback
def faculty_feedback(request) :
	f_name = Chart.name
	f_money = Chart.money
	data = serializers.serialize("json", Feedback.objects.all())
	data = json.loads(data)
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
	for d in data:
		del d['model'],d['pk']
	data = json.dumps(data)
	# print(data)
	context = {
		'data' : data,
		'name' : f_name,
		'money' : f_money,
		'questions' : questions
	}
	# context["qs"] = Chart.objects.all()

	return render(request,"Faculty/feedback.html",context)

def monthlist_fast(dates):
    start, end = [date.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    mlist = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        mlist.append(date(y, m+1, 1))
    return mlist

from subject_V1.models import Subject_event
import django.utils.timezone as tz
def transpose(l1):
    l2 = list(map(list, zip(*l1)))
    return l2
def get_all_questions_list(qs):
	# Q1 = Q2 = Q3 = Q4 = Q5 = Q6 = Q7 = Q8 = Q9 = []
	Q = []
	Questions = list(qs.values_list("Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9"))
	ave = [[0,0] for _ in range(9)]
	# arr = np.array(Questions)
	# arr = arr.transpose()
	Questions = transpose(Questions)
	for i in range(len(Questions)):
		temp = [int(x) for x in Questions[i] if x != None]
		if temp:
			ave[i] = [round(sum(temp)/len(temp),2),len(temp)]
	return ave

class ChartData(APIView):
	# authentication_classes = []
	# permission_classes = []
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format = None):
		########################## general decleration ######################
		subject_event = Subject_event.objects.filter(Faculty_id=request.user.faculty_details)[0]
		wef = subject_event.Subject_id.Semester_id.WEF_id
		all_feeback  = Feedback.objects.filter(Event_id__Subject_event_id = subject_event)
		list_of_months = monthlist_fast([str(wef.start_date),str(wef.end_date)])
		Que1 ,Que2 ,Que3 ,Que4 ,Que5 ,Que6 ,Que7 ,Que8 ,Que9 = ([] for i in range(9))
		length1 ,length2 ,length3 ,length4 ,length5 ,length6 ,length7 ,length8 ,length9 = ([] for i in range(9))

		###################### if Graph name ######################
		if 'graph_name' in request.GET:
			current_graph,required_value = request.GET['graph_name'].split()
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
					day_feedback = all_feeback.filter(timestamp__date=s_d)
					q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9 = get_all_questions_list(day_feedback)
					Que1.append(q1[0])
					length1.append(q1[1])
					Que2.append(q2[0])
					length2.append(q2[1])
					Que3.append(q3[0])
					length3.append(q3[1])
					Que4.append(q4[0])
					length4.append(q4[1])
					Que5.append(q5[0])
					length5.append(q5[1])
					Que6.append(q6[0])
					length6.append(q6[1])
					Que7.append(q7[0])
					length7.append(q7[1])
					Que8.append(q8[0])
					length8.append(q8[1])
					Que9.append(q9[0])
					length9.append(q9[1])
					print("total - {}".format(day_feedback.count()))
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
					
				print(chartdata)
				data ={
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
					"button_id" : '#show_week',

				}
				return Response([data,"day_rating"]) # data and next chart_id
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
					week_feedback = all_feeback.filter(timestamp__date__gte=start_date, timestamp__date__lt=end_date)
					q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9 = get_all_questions_list(week_feedback)
					Que1.append(q1[0])
					length1.append(q1[1])
					Que2.append(q2[0])
					length2.append(q2[1])
					Que3.append(q3[0])
					length3.append(q3[1])
					Que4.append(q4[0])
					length4.append(q4[1])
					Que5.append(q5[0])
					length5.append(q5[1])
					Que6.append(q6[0])
					length6.append(q6[1])
					Que7.append(q7[0])
					length7.append(q7[1])
					Que8.append(q8[0])
					length8.append(q8[1])
					Que9.append(q9[0])
					length9.append(q9[1])
					print("total - {}".format(week_feedback.count()))
					arr = list(week_feedback.values_list("average",flat=True))
					arr = [x for x in arr if x != 0]
					week_ave = 0
					if arr:
						week_ave = round(sum(arr)/len(arr),2)
					ids.append("{}_{}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
					chartdata.append(week_ave)
				print("here")
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
					"button_id" : '#show_semester',
				}
				return Response([data,"week_rating"]) # data and next chart_id
			elif current_graph == "get_semester_rating":
				###################### month rating ##########################
				labels = []
				chartLabel = "Average Rating"
				chartdata = []
				ids = []

				for i in list_of_months:
					labels.append(month_name[i.month])
					ids.append(i.strftime("%B_%Y"))
					# print()
					month_feedback = all_feeback.filter(timestamp__month=i.month)
					q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9 = get_all_questions_list(month_feedback)
					Que1.append(q1[0])
					length1.append(q1[1])
					Que2.append(q2[0])
					length2.append(q2[1])
					Que3.append(q3[0])
					length3.append(q3[1])
					Que4.append(q4[0])
					length4.append(q4[1])
					Que5.append(q5[0])
					length5.append(q5[1])
					Que6.append(q6[0])
					length6.append(q6[1])
					Que7.append(q7[0])
					length7.append(q7[1])
					Que8.append(q8[0])
					length8.append(q8[1])
					Que9.append(q9[0])
					length9.append(q9[1])
					print("month {}->{}".format(i.month,month_feedback.count()))
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
				return Response([data,"month_rating"])
		
		###################### default day view #####################
		chartLabel ="Average Rating"
		labels = []
		chartdata = []
		delta = timedelta(1)
		today = date.now()
		week_number = math.ceil(today.day/7) - 1 # get the week number of the date
		s_d = today.replace(day=week_number*7) + delta
		# s_d = date.strptime(start_date, '%Y-%m-%d')
		for i in range(7):
			labels.append(s_d.strftime("%d-%m (%a)"))
			day_feedback = all_feeback.filter(timestamp__date=s_d)
			q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9 = get_all_questions_list(day_feedback)
			Que1.append(q1[0])
			length1.append(q1[1])
			Que2.append(q2[0])
			length2.append(q2[1])
			Que3.append(q3[0])
			length3.append(q3[1])
			Que4.append(q4[0])
			length4.append(q4[1])
			Que5.append(q5[0])
			length5.append(q5[1])
			Que6.append(q6[0])
			length6.append(q6[1])
			Que7.append(q7[0])
			length7.append(q7[1])
			Que8.append(q8[0])
			length8.append(q8[1])
			Que9.append(q9[0])
			length9.append(q9[1])
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
		print(Que2,len(Que2))
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
			"button_id" : '#show_week',
			"chartdata":chartdata,
		}
		###################### on click ######################
		return Response(data)