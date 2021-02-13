from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.views import View
#################
import json
import datetime
from .models import event_class,timings,event
from .forms import selectdays,add_event	# for selecting the days
from admin_V1.views import return_context
######################

global_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
@method_decorator(login_required(login_url='login'), name='dispatch')
class view_table(View):
	template_name = "ED_project/table.html"	# Main Table
	global global_days
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		periods = timings.objects.filter(owner=request.user).order_by('start_time')
		# Get all the timimg obojects of a user and sort them

		event_butts = event_class.objects.filter(owner=request.user)
		# Get all the event_buttons for a user 

		events = event.objects.filter(owner=request.user)
		#	Get all the exesting objects of the user
		print(events)
		context = return_context(request)
		context['days']= global_days 					# For displaying days
		context['table_width']= len(global_days) * 200	# For the width of the table
		context['periods'] = periods					# All the timings
		context['event_butts'] = event_butts			# All the buttons
		context['events'] = events						# All the existing events
		# 'day_len': len(global_days)+1,		# For the tfoot button
		return render(self.request, self.template_name,context)

	def post(self, request):
		if request.method == "POST" and request.is_ajax():
			try:
				data = json.loads(request.body)	# data is the json object returned after saving
				# print(data)
				old_obj = event.objects.filter(owner=request.user) # gets all the old data
				# gets all the old data and deletes them 
				new_objs = []
				for i in data:
					for day in global_days:	# for all the days in the table
						value = i[day]		# value is the event-object
						if value['name'] and value['event_pk'] and value['time_pk']:
							try:
								temp_obj = event_class.objects.filter(owner=request.user)
								# temp_obj is the all the event_class objects of the user

								event_obj = temp_obj.get(pk=value['event_pk']) or None
								# event_obj is the same event_obj if it is of the same user
								# else it is null

								temp_obj = timings.objects.filter(owner=request.user)
								# temp_obj is the all the timing objects of the user

								time_obj = temp_obj.get(pk=value['time_pk'])
								# time_obj is the same time_obj if it is of the same user
								# else it is null

								obj = event(event_obj = event_obj,time_obj = time_obj,day=value['day'],owner=request.user)
								# made a event object succefully
								# obj.save()
								new_objs.append(obj);	# appends all the objects
								saved = True
							except:
								print("Stop Messing Around ...")
								# if the primary keys of any of the objects do not match
				old_obj.delete() # deletes all the old data if no error is there
				for obj in new_objs:# saves all the new data
					obj.save()
				# print()
				return HttpResponse("<p>Done</p>")
			except KeyError:
				HttpResponseServerError("Malformed data!")
				return JsonResponse({"success": True}, status=200)
			return render(self.request, self.template_name,context)
		else:
			return JsonResponse({"success": False}, status=400)
	
	def selectday(request):
		# renders the form to select the days to display in the table
		form = selectdays()
		if request.method == 'POST':
			form = selectdays(request.POST)
			global global_days
			global_days = request.POST.getlist('Days')
			# changing the global days variable so when the get is called it has new days
			return redirect('table')
		return render(request,"Table/select_days.html",{'form':form})

	def add_event(request):
		form = add_event()
		if request.method == 'POST':
			form = add_event(request.POST)
			candidate = form.save(commit=False)
			candidate.owner = request.user
			candidate.save()
			return redirect('table')
		return render(request,"Table/add_event.html",{'form':form})
