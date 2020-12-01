from django.db import models

################################################

from institute_V1.models import Division,Batch,Slots
from subject_V1.models import Subject_event

################################################


class Event(models.Model):
	Slot_id = models.OneToOneField(Slots,on_delete=models.CASCADE)
	Division_id = models.ForeignKey(Division,on_delete=models.CASCADE)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Slot_id) + " - " + str(self.Subject_event_id)
	class Meta:
		verbose_name_plural = "Event"