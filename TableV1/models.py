from django.db import models

# Create your models here.
# class time:
# 	hrs
# 	min
# 	sec
class event_class(models.Model):
	event_name = models.CharField(max_length = 20)
	event_link = models.CharField(max_length = 200)
	event_color = models.CharField(max_length = 50)
	# event_time = time(hrs)
	def __str__(self):
		return self.event_name