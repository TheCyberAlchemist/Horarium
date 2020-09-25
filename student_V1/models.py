from django.db import models

################################################

from institute_V1.models import Division,Batch,Institute
from django.contrib.auth import get_user_model

################################################

N_len = 50

class Student_details(models.Model):
	User_id = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
	roll_no = models.CharField(max_length = 20)
	Division_id = models.ForeignKey(Division,on_delete=models.SET_NULL,null=True)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Student Details"