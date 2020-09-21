from django.db import models
################################################

from institute_V1.models import Department
from django.contrib.auth.models import User,Group
from institute_V1.models import Shift
from subject_V1.models import Subject_details

################################################

N_len = 50
S_len = 10

class Faculty_designation(models.Model):
	designation = models.CharField(max_length = N_len)
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.designation
	class Meta:
		verbose_name_plural = "Faculty Designation"

class Faculty_details(models.Model):
	User_id = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	email = models.EmailField(max_length=254)
	Designation_id = models.ForeignKey(Faculty_designation,on_delete=models.RESTRICT)
	Shift_id = models.ForeignKey(Shift,on_delete=models.RESTRICT)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Faculty Details"

class Faculty_load(models.Model):
	load = models.IntegerField()
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Faculty_id) + " - " + str(self.load) + " hrs"
	class Meta:
		verbose_name_plural = "Faculty load"

class Can_teach(models.Model):
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Faculty_id) + " - " + str(self.Subject_id)
	class Meta:
		verbose_name_plural = "Can teach"