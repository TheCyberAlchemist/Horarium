from django.shortcuts import render
from .models import event_class
# Create your views here.

def view_table(request):
	dbms = event_class(event_name = 'DBMS',event_link = "",event_color = "red")
	ds = event_class(event_name = 'DS',event_link = "",event_color = "#0f0")
	aem = event_class(event_name = 'AEM',event_link = "",event_color = "salmon")
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday']#,'Sat','Sun'
	context = {
		'days': days,
		'table_width': len(days) * 200,
		'periods' : ['9-9:50','9:50-10:40','10:40-11:30'],
		'events' : [dbms,ds,aem],

	}
	return render(request,"table.html",context)
