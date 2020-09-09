from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views import View
from json import dumps
#################
import json
import datetime
from .models import event_class,timings,event
from .forms import selectdays
######################

global_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
class view_table(View):
	template_name = "Table/table.html"
	global global_days
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		periods = timings.objects.filter(owner=request.user).order_by('start_time')
		event_butts = event_class.objects.filter(owner=request.user)
		events = event.objects.filter(owner=request.user)
		for e in events:
			print(e.time_obj,e.day)
		context = {
			'days': global_days,
			'table_width': len(global_days) * 200,
			'periods' : periods,
			'event_butts' : event_butts,
			'events' : events,
		}
		return render(self.request, self.template_name,context)


	def post(self, request):
		if request.method == "POST" and request.is_ajax():
			try:
				data = json.loads(request.body)
				print(data)
				for i in data:
					for day in global_days:
						value = i[day]
						if value['name'] and value['event_pk'] and value['time_pk']:
							# print(i[day])
							temp_obj = event_class.objects.filter(owner=request.user)
							event_obj = temp_obj.get(pk=value['event_pk'])
							temp_obj = timings.objects.filter(owner=request.user)
							time_obj = temp_obj.get(pk=value['time_pk'])
							# times = timings.objects.filter(user = request.user)
							print(request.user.id)
							obj = event(event_obj = event_obj,time_obj = time_obj,day=value['day'],owner=request.user)
							print(obj)
							obj.save()
				return HttpResponse("<p>Done</p>")
			except KeyError:
				HttpResponseServerError("Malformed data!")
				return JsonResponse({"success": True}, status=200)
		else:
			return JsonResponse({"success": False}, status=400)

	def selectday(request):
		form = selectdays()
		if request.method == 'POST':
			form = selectdays(request.POST)
			global global_days
			global_days = request.POST.getlist('Days')
			return redirect('table')
		return render(request,"abc.html",{'form':form})



# def view_nav(request) :
# 	return render(request,'navbar.html')
########### adding objects
# dbms = event_class(event_name = 'DBMS',event_link = "",event_color = "red")
# ds = event_class(event_name = 'DS',event_link = "",event_color = "#0f0")
# aem = event_class(event_name = 'AEM',event_link = "",event_color = "salmon")
# math = event_class(event_name = 'Math',event_link = "",event_color = "cyan")
# dbms.save()
# ds.save()
# aem.save()
# math.save()
# s = datetime.time(1,30,0)
# e = datetime.time(2,30,0)
# # lect1 = timings.objects.create(start_time = s,end_time = e)
# # print(lect1.start_time.hour,lect1.end_time.hour)
# # print(lect1)
