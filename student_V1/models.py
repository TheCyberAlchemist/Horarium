from django.db import models

################################################

from institute_V1.models import Division,Batch
from django.contrib.auth.models import User

################################################

N_len = 50

class Student_details(models.Model):

	User_id = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length = N_len)
	roll_no = models.CharField(max_length = 20)
	email = models.EmailField(max_length=254)
	Division_id = models.ForeignKey(Division,on_delete=models.SET_NULL,null=True)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Student Details"