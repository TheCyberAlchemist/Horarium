from django.db import models
from django.contrib.auth.models import User
import datetime as dt
class event_class(models.Model):
	event_name = models.CharField(max_length = 20)
	event_link = models.CharField(max_length = 200, null=True,blank=True)
	event_color = models.CharField(max_length = 50)
	owner = models.ForeignKey(User,default=None ,on_delete = models.CASCADE)
	def __str__(self):
		return self.event_name

class timings(models.Model):
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	owner = models.ForeignKey(User,default=None,on_delete = models.CASCADE)

	def delta(self): # Returns the time of the event 
					 # ( always +ve for correct input and -ve for false input)
		end_time = dt.datetime.combine(dt.date.today(), self.end_time)
		start_time = dt.datetime.combine(dt.date.today(), self.start_time)
		diff = end_time - start_time
		return diff.total_seconds()
		
	def __str__(self):
		return str(self.start_time) + " - " + str(self.end_time)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class event(models.Model):
	event_obj = models.ForeignKey(event_class, on_delete=models.CASCADE)
	time_obj = models.ForeignKey(timings, on_delete=models.CASCADE)
	day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
	owner = models.ForeignKey(User,default=None,on_delete = models.CASCADE)

	def __str__(self):
		return str(self.event_obj.event_name) + " at " + str(self.time_obj) + " on " + str(self.day)
	
