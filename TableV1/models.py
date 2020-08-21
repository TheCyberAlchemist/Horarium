from django.db import models

# Create your models here.

class event_class(models.Model):
	event_name = models.CharField(max_length = 20)
	event_link = models.CharField(max_length = 200)
	event_color = models.CharField(max_length = 50)
	def __str__(self):
		return self.event_name