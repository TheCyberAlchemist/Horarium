from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views import View

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
		periods = timings.objects.all().order_by('start_time')
		events = event_class.objects.all()
		context = {
			'days': global_days,
			'table_width': len(global_days) * 240,
			'periods' : periods,
			'events' : events,
		}
		return render(self.request, self.template_name,context)


	def post(self, request):
		if request.method == "POST" and request.is_ajax():
			try:
			# Parse the JSON payload
				data = json.loads(request.body)
				for i in data:
					for day in global_days:
						value = i[day]
						if value['name'] and value['event_pk'] and value['time_pk']:
							# print(i[day])
							event_obj = event_class.objects.get(pk=value['event_pk'])
							time_obj = timings.objects.get(pk=value['time_pk'])
							obj = event(event_obj = event_obj,time_obj = time_obj)
							print(obj)
							obj.save()

			# Loop over our list order. The id equals the question id. Update the order and save
			# for idx,question in enumerate(data):
			#     pq = PaperQuestion.objects.get(paper=pk, question=question['id']) 
			#     pq.order = idx + 1
			#     pq.save()
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
			print(global_days,"hii")
			return redirect('table')

		return render(request,"abc.html",{'form':form})

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