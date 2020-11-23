from django.db import models
################################################

from institute_V1.models import Department
from django.contrib.auth import get_user_model
from institute_V1.models import Shift,Institute
from subject_V1.models import Subject_details

################################################

N_len = 50
S_len = 10

class Faculty_designation(models.Model):
	designation = models.CharField(max_length = N_len)
	Institute_id = models.ForeignKey(Institute,default=None,on_delete = models.CASCADE,null=True,blank=True)
	def __str__(self):
		return self.designation
	class Meta:
		verbose_name_plural = "Faculty Designation"
		constraints = [
			models.UniqueConstraint(fields=['designation', 'Institute_id'], name='Designation is Unique for Institute'),
		]

class Faculty_details(models.Model):
	User_id = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,null=True)
	short = models.CharField(max_length = S_len)
	Designation_id = models.ForeignKey(Faculty_designation,on_delete=models.RESTRICT)
	Shift_id = models.ForeignKey(Shift,on_delete=models.RESTRICT)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Faculty Details"

class Faculty_load(models.Model):
	total_load = models.PositiveIntegerField()
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Faculty_id) + " - " + str(self.total_load) + " hrs"
	class Meta:
		verbose_name_plural = "Faculty load"

class Can_teach(models.Model):
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Faculty_id) + " - " + str(self.Subject_id)
	class Meta:
		verbose_name_plural = "Can teach"