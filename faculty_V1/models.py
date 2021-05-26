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

# make fac id onetoone in load
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
	timestamp = models.DateTimeField(auto_now=False)
	# timestamp = models.DateTimeField(auto_now=True)
	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.CASCADE,null=True,blank=True)
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
	average = models.IntegerField(null=True,blank=True)
	def __str__(self):
		return str(self.Subject_event_id.Faculty_id) +" from "+ str(self.Given_by) + " at " + str(self.timestamp)

	def get_ave(self):
		arr = [self.Q1,self.Q2,self.Q3,self.Q4,self.Q5,self.Q6,self.Q7,self.Q8,self.Q9]
		# arr = filter(None,arr)
		arr = [int(x) for x in arr if x is not None]
		if len(arr):
			self.average = sum(arr)/len(arr)
		else:
			self.average = 0
		self.save()

	def save(self, *args, **kwargs):
		arr = [self.Q1,self.Q2,self.Q3,self.Q4,self.Q5,self.Q6,self.Q7,self.Q8,self.Q9]
		# arr = filter(None,arr)
		arr = [int(x) for x in arr if x is not None]
		if arr:
			self.average = sum(arr)/len(arr)
		else:
			self.average = 0
		super(Feedback, self).save(*args, **kwargs)
		
		# return None

	# def save(self, *args, **kwargs):
	# 	print(str(self))

