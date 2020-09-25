from django.db import models

################################################

from institute_V1.models import Division,Batch,Slots
from subject_V1.models import Subject_event

################################################


class Event(models.Model):
	Slot_id = models.ForeignKey(Slots,on_delete=models.CASCADE)
	Division_id = models.ForeignKey(Division,on_delete=models.CASCADE)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.CASCADE)
	Day = models.CharField(max_length=9)