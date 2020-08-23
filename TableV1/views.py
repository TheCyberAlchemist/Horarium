from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import event_class,timings
import json
import datetime
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
# Create your views here.

class view_table(View):
	template_name = "table.html"
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
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
		periods = timings.objects.all().order_by('start_time')
		# sorted_periods = periods
		periods[0].delta()
		events = event_class.objects.all()
		days = ['Monday','Tuesday','Wednesday','Thursday','Friday']#,'Saturday','Sunday'
		context = {
			'days': days,
			'table_width': len(days) * 240,
			# 'periods' : ['9-9:50','9:50-10:40','10:40-11:30'],
			'periods' : periods,
			'events' : events,
		}
		return render(self.request, self.template_name,context)


	def post(self, request):
		if request.method == "POST" and request.is_ajax():
			try:
			# Parse the JSON payload
				data = json.loads(request.body)
				# for i in data:
				# 	for j in i:
				# 		print(j)
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