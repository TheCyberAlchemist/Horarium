from django.db import models

################################################

from institute_V1.models import Division,Batch,Slots,Resource
from subject_V1.models import Subject_event

################################################


class Event(models.Model):
	Slot_id = models.ForeignKey(Slots,on_delete=models.CASCADE,related_name='lecture')
	Slot_id_2 = models.ForeignKey(Slots,on_delete=models.CASCADE,null=True,blank=True,related_name='Practical')
	Division_id = models.ForeignKey(Division,on_delete=models.CASCADE)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.CASCADE)
	Resource_id = models.ForeignKey(Resource,on_delete=models.CASCADE,null=True,blank=True)
	link = models.CharField(max_length=200, null=True, blank=True)
	def __str__(self):
		if self.Slot_id_2:
			return str(self.Slot_id) +" | " + str(self.Slot_id_2.get_time()) + " - " + str(self.Subject_event_id)	
		return str(self.Slot_id) + " - " + str(self.Subject_event_id)
	class Meta:
		verbose_name_plural = "Event"