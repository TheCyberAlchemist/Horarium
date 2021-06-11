from django.db import models

################################################

from institute_V1.models import Division,Batch,Institute
from django.contrib.auth import get_user_model

################################################

N_len = 50
class WEF(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(WEF__is_active = True)


class Student_details(models.Model):
	User_id = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
	display_image = models.ImageField(null=True,blank=True)
	
	roll_no = models.CharField(max_length = 20)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	Division_id = models.ForeignKey(Division,on_delete=models.SET_NULL,null=True)
	prac_batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True,related_name="practical_batch+")
	lect_batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True,related_name="lecture_batch+")
	# objects = WEF()
	def __str__(self):
		return self.User_id.first_name
	class Meta:
		verbose_name_plural = "Student Details"