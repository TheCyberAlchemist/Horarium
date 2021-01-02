from django.shortcuts import render
from Table_V2.models import Event
from institute_V1.models import Slots,Timings,Shift,Working_days
from student_V1.models import Student_details
# Create your views here.

def student_home(request):
	# for i in Slots.objects.filter(day=2):
	student = request.user.student_details
	my_shift = student.Division_id.Shift_id
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : Event.objects.filter(Division_id=student.Division_id),
		'timings' : Timings.objects.filter(Shift_id = my_shift),
	}
	print(context)
	# for i in range(5):
	# 	a = Event(Slot_id_id=Slots.objects.filter(day__Days_id=i+1)[i].id,Division_id_id=2,Subject_event_id_id=7,Resource_id_id=1)
	# print(Event.objects.filter(Division_id=student.Division_id).values("Batch_id"))

	return render(request,"Student/student_v1.html",context)