from django.db import models
################################################

from institute_V1.models import Department
from django.contrib.auth import get_user_model
from institute_V1.models import Shift,Institute,Slots
from subject_V1.models import Subject_details,Subject_event
from Table_V2.models import Event
from login_V2.models import CustomUser
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
	Department_id = models.ForeignKey(Department,on_delete=models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Faculty Details"

class Faculty_load(models.Model):
	total_load = models.PositiveIntegerField()
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	def remaining_load(self):
		all_events = Subject_event.objects.filter(Faculty_id=self.Faculty_id)
		total = 0
		for i in all_events:
			total += i.total_load_carried()
		return self.total_load - total
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

class Not_available(models.Model):
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE)
	Slot_id = models.ForeignKey(Slots,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.Faculty_id) + " - " + str(self.Slot_id)
	class Meta:
		verbose_name_plural = "Not Available"

class Chart(models.Model) :
	name = models.CharField(max_length=20)
	money = models.IntegerField()

	def __str__(self):
		return str(self.name) + ' - ' + str(self.money)
	

class Feedback(models.Model):
	timestamp = models.TimeField(auto_now=True)
	Event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
	Given_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

	rating = (
		('5',"5"),
		('4',"4"),
		('3',"3"),
		('2',"2"),
		('1',"1"),
	)

	Q1 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q2 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q3 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q4 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q5 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q6 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q7 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q8 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	Q9 = models.CharField(max_length = 1 ,choices=rating,null=True,blank=True)
	query = models.TextField(null=True,blank=True)

	def __str__(self):
		return str(self.Event_id.Subject_event_id.Faculty_id) +" from "+ str(self.Given_by)

	# def save(self, *args, **kwargs):
	# 	print(str(self))

