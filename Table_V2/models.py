from django.db import models

################################################

from institute_V1.models import Division,Batch,Slots,Resource
from subject_V1.models import Subject_event

################################################

class active_manager(models.Manager):
	def active(self):
		'Get all the events having Subject_events active in the db'
		return super().get_queryset().filter(Subject_event_id__active=True)
	def inactive(self):
		'Get all the events having Subject_events having active = False in the db'
		return super().get_queryset().filter(Subject_event_id__active=False)
	def filter_faculty(self,Faculty_object,active=True):
		'get all the `active`(default) or `inactive` Events having the Faculty_object as Faculty_id or Co_faculty_id'
		return super().get_queryset().filter(models.Q(Subject_event_id__Co_faculty_id=Faculty_object)|models.Q(Subject_event_id__Faculty_id=Faculty_object),Subject_event_id__active=active)

class Event(models.Model):
	Slot_id = models.ForeignKey(Slots,on_delete=models.CASCADE,related_name='lecture')
	Slot_id_2 = models.ForeignKey(Slots,on_delete=models.CASCADE,null=True,blank=True,related_name='Practical')
	Division_id = models.ForeignKey(Division,on_delete=models.CASCADE)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.CASCADE)
	Resource_id = models.ForeignKey(Resource,on_delete=models.CASCADE,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)
	objects = active_manager()
	def __str__(self):
		try:
			if self.Slot_id_2 and self.Slot_id_2_id != -1:
				return str(self.Slot_id) +" | " + str(self.Slot_id_2.get_time()) + " - " + str(self.Subject_event_id)	
			if self.Slot_id:
				return str(self.Slot_id) + " - " + str(self.Subject_event_id)
		except:
			return str(self.Batch_id) + " - " + str(self.Subject_event_id)
	class Meta:
		verbose_name_plural = "Event"