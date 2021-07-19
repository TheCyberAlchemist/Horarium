from django.db import models
import datetime
from django.contrib.auth import get_user_model
################################################

from institute_V1.models import Department,WEF,Semester
from institute_V1.models import Shift,Institute,Slots
from subject_V1.models import Subject_details,Subject_event
from Table_V2.models import Event
################################################

N_len = 50
S_len = 10
MANDATORY_FEEDBACK_ACTIVE_DAYS = 3

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
	#  on delete called we can check if there is an active event and then only delete
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
	Faculty_id = models.OneToOneField(Faculty_details,on_delete=models.CASCADE)
	def remaining_load(self):
		all_events = Subject_event.objects.active().filter(Faculty_id=self.Faculty_id)
		total = 0
		for i in all_events:
			total += i.total_load_carried()
		return self.total_load - total
	def load_carried(self):
		all_events = Subject_event.objects.active().filter(Faculty_id=self.Faculty_id)
		total = 0
		for i in all_events:
			total += i.total_load_carried()
		return total

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

class Feedback_type_manager(models.Manager):
	def future(self):
		'Get all the feedback_type that are coming in future from the db (active=1)'
		return super().get_queryset().filter(active=1)
	def present(self):
		'Get all the feedback_type that are happening in present from the db (active=0)'
		return super().get_queryset().filter(active=0)
	def past(self):
		'Get all the feedback_type that have happened in past from the db (active=-1)'
		return super().get_queryset().filter(active=-1)

# need to delete all the feedback types after WEF ends
class Feedback_type(models.Model):
	name = models.CharField(max_length = N_len)
	WEF = models.ForeignKey(WEF,on_delete=models.CASCADE)
	for_date = models.DateField()
	active = models.IntegerField(null=True,blank=True)
	objects = Feedback_type_manager()

	def update(self,today):
		'''
		Update Feedback_type.actice to -1/0/1 as gone/happening/coming

		today < for_date
		9 < 10  -- coming

		for_date <= today < for_date + 3 --- now
		10 <= 10 < 13
		10 <= 11 < 13
		10 <= 12 < 13

		for_date + 3 <= today --- gone
		13 <= 13
		13 <= 14
		'''
		if today < self.for_date :
			# if coming
			self.active = 1
		elif self.for_date <= today < (self.for_date + datetime.timedelta(MANDATORY_FEEDBACK_ACTIVE_DAYS)):
			# if currently happening
			self.active = 0
		elif self.for_date + datetime.timedelta(MANDATORY_FEEDBACK_ACTIVE_DAYS) <= today:
			# if gone
			self.active = -1
	
	@staticmethod
	def update_all_feedback_types():
		'Function to update all Feedback_type object if they are active or inactive'
		today = datetime.date.today()
		for i in Feedback_type.objects.present():
			i.save()
		for i in Feedback_type.objects.future():
			i.save()
	
	def __str__(self):
		return "%s for %s" %(str(self.for_date),str(self.WEF.name))

	def save(self, *args, **kwargs):
		self.update(datetime.date.today())
		super(Feedback_type, self).save(*args, **kwargs)


class Feedback_manager(models.Manager):
	def active(self):
		'Get all the active feedbacks from the db (Feedback.Subject_event_id.active = True)'
		return super().get_queryset().filter(Subject_event_id__active=True)
	def regular(self):
		'Get all the regular feedbacks from the db (Feedback_type = null)'
		return super().get_queryset().filter(Feedback_type__isnull=True)
	def special(self):
		'Get all the special/mandatory feedbacks from the db (Feedback_type != null)'
		return super().get_queryset().filter(Feedback_type__isnull=False)
	def previous(self):
		'get all the feedbacks that are of previous WEFs (having no Subject_event)'
		return super().get_queryset().filter(Subject_event_id__isnull=True)

class Feedback(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	Given_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

	Subject_event_id = models.ForeignKey(Subject_event,on_delete=models.SET_NULL,null=True,blank=True)

	Feedback_type = models.ForeignKey(Feedback_type,default=None,on_delete=models.SET_NULL, null=True,blank=True)
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.SET_NULL,null=True,blank=True)
	
	objects = Feedback_manager()
	
	Faculty_id = models.ForeignKey(Faculty_details,on_delete=models.CASCADE,null=True,blank=True)
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
		if self.Subject_event_id:
			return str(self.Subject_event_id.Faculty_id) +" from "+ str(self.Given_by) + " at " + str(self.timestamp)
		else:
			if self.Subject_id:
				return "Mandatory %s from %s at %s" % (self.Subject_id.name,self.Given_by,self.timestamp)

	def get_ave(self):
		arr = [self.Q1,self.Q2,self.Q3,self.Q4,self.Q5,self.Q6,self.Q7,self.Q8,self.Q9]
		# arr = filter(None,arr)
		arr = [int(x) for x in arr if x is not None]
		if len(arr):
			self.average = sum(arr)/len(arr)
		else:
			self.average = 0

	def save(self, *args, **kwargs):
		self.get_ave()
		if self.Subject_event_id:
			self.Faculty_id = self.Subject_event_id.Faculty_id
		super(Feedback, self).save(*args, **kwargs)
		
		# return None

	# def save(self, *args, **kwargs):
	# 	print(str(self))
