from django.db import models
from institute_V1.models import *
from subject_V1.models import *

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length = 100)
	start_date = models.DateField(auto_now=False, auto_now_add=False)
	end_date = models.DateField(auto_now=False, auto_now_add=False)
	Semester_id = models.ForeignKey(Semester,default=None,on_delete = models.CASCADE)
	other_details = models.TextField(null=True,blank=True)
	def __str__(self):
		return self.name
		# s_min = "00" if self.start_time.minute == 0 else str(self.start_time.minute)
		# e_min = "00" if self.end_time.minute == 0 else str(self.end_time.minute)
		# return self.name + " [ " + str(self.start_time.hour) + ":"+ s_min + " - " + str(self.end_time.hour) + ":"+ e_min + " ]"
	class Meta:
		verbose_name_plural = "Exams"
		constraints = [
        ]
	def save(self, *args, **kwargs):
		super(Shift, self).save(*args, **kwargs)
		pass

class Subject_exam(models.Model):
	Exam_id = models.ForeignKey(Exam,default=None,on_delete = models.CASCADE)
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	Batch_id = models.ForeignKey(Batch,on_delete=models.CASCADE)
	date = models.DateField(auto_now=False, auto_now_add=False)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	link = models.CharField(max_length=200, null=True, blank=True)
	def __str__(self):
		return f'{self.Batch_id}-{self.Subject_id} [{self.date}]'
	class Meta:
		verbose_name_plural = "Subject Exams"
		constraints = [
        ]