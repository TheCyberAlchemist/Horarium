from django.db import models
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
################################################
import datetime

N_len = 50
S_len = 10

class Days(models.Model):
	name = models.CharField(max_length = N_len)
	def __str__(self):
		return self.name

class Institute(models.Model):
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Institute"

class Resource(models.Model):
	name = models.CharField(max_length = N_len)
	block = models.CharField(max_length = N_len, null=True, blank=True)
	is_lab = models.BooleanField(default=False)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)

	def get_type_by_shift(self,Shift_id):
		'return if the resource is attached to a class or a faculty '
		pass
	
	def is_free(self,Slot_id):
		'returns True if the resource is free on the slot else returns False'
		# is free must check for the the start time and end time rather then the slot itself
		from Table_V2.models import Event
		all_events_for_resource = Event.objects.all().filter(Resource_id = self)
		qs = all_events_for_resource.filter(Q(Slot_id_2=Slot_id) | Q(Slot_id=Slot_id))	
		if len(qs): 
			# if there is an event having the resource on the slot
			return False
		st = Slot_id.Timing_id.start_time
		et = Slot_id.Timing_id.end_time
		same_day_events = all_events_for_resource.filter(Slot_id__day__Days_id = Slot_id.day.Days_id)
		if same_day_events.filter(start_time__lt=et,end_time__gte = st):
			# (start_time1 < end_time2) and (start_time2 < end_time1) 
			# => (start_time1 < end_time2) and (end_time1 >= start_time2)
			# if other slots time overlaps except the end points
			return False
		return True

	def get_name(self):
		type = "Lab" if self.is_lab else "Classroom"
		return f"{self.name} -- {type}"
	# from institute_V1.models import *
	# from Table_V2.models import *
	# Slot_id=Slots.objects.all().order_by("Timing_id__start_time")[10]
	# Institute_id = Institute.objects.get(pk=1)
	@staticmethod
	def get_all_free_for_slot_in_division(Slot_id,Institute_id,Division_id=None):
		'Returns the QS of all the resources that are free for a slot in the institute that are not in the same division'
		from Table_V2.models import Event
		st = Slot_id.Timing_id.start_time
		et = Slot_id.Timing_id.end_time
		Institute_events = Event.objects.active().filter(Division_id__Semester_id__Branch_id__Department_id__Institute_id=Institute_id)
		# Institute_events = Event.objects.all().filter(Division_id__Semester_id__Branch_id__Department_id__Institute_id=Institute_id)
		same_day_events = Institute_events.filter(Slot_id__day__Days_id = Slot_id.day.Days_id).exclude(Division_id=Division_id)
		# remove the events from the same division as they should not be considered
		resources_in_use = same_day_events.filter(start_time__lt=et,end_time__gte = st).values_list("Resource_id",flat=True)
		temp = [i for i in list(resources_in_use) if i]	# remove None from the array
		return Resource.objects.all().filter(Institute_id=Institute_id).exclude(pk__in=temp)
	
	@staticmethod
	def get_all_filled_for_slot(Slot_id,Institute_id,Division_id=None):
		'returns all the filled resources during the slot'
		from Table_V2.models import Event
		st = Slot_id.Timing_id.start_time
		et = Slot_id.Timing_id.end_time
		Institute_events = Event.objects.active().filter(Division_id__Semester_id__Branch_id__Department_id__Institute_id=Institute_id)
		# Institute_events = Event.objects.all().filter(Division_id__Semester_id__Branch_id__Department_id__Institute_id=Institute_id)
		same_day_events = Institute_events.filter(Slot_id__day__Days_id = Slot_id.day.Days_id).exclude(Division_id=Division_id)
		# remove the events from the same division as they should not be considered
		resources_in_use = same_day_events.filter(start_time__lt=et,end_time__gte = st).values_list("Resource_id",flat=True)
		temp = [i for i in list(resources_in_use) if i]	# remove None from the array
		return Resource.objects.all().filter(Institute_id=Institute_id,pk__in=temp)

	@staticmethod
	def get_unattached_resources_for_shift(Shift_id):
		from faculty_V1.models import Faculty_details
		'Returns a qs of all the resources that are not attached to a class or faculty'
		arr = list(Division.objects.active().filter(Shift_id=Shift_id).values_list("Resource_id",flat=True))
		arr1 = list(Faculty_details.objects.filter(Shift_id=Shift_id).values_list("Resource_id",flat=True))
		temp = [i for i in arr + arr1 if i]	# remove None from the array
		all_free_resources = Resource.objects.all().filter(Institute_id = Shift_id.Department_id.Institute_id).exclude(pk__in=temp)
		return all_free_resources
	
	def __str__(self):
		return f"{self.name}"
	
	class Meta:
		verbose_name_plural = "Resource"
		constraints = [
            models.UniqueConstraint(fields=['name', 'Institute_id'], name='Resource Name is Unique for Institute'),
        ]

class Department(models.Model):
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	Institute_id = models.ForeignKey(Institute,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Department"
		constraints = [
            models.UniqueConstraint(fields=['short', 'Institute_id'], name='DepartmentShort is Unique for Institute'),
			models.UniqueConstraint(fields=['name', 'Institute_id'], name='DepartmentName is Unique for Institute')
        ]

class Shift(models.Model):
	name = models.CharField(max_length = N_len)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	def __str__(self):
		s_min = "00" if self.start_time.minute == 0 else str(self.start_time.minute)
		e_min = "00" if self.end_time.minute == 0 else str(self.end_time.minute)
		return self.name + " [ " + str(self.start_time.hour) + ":"+ s_min + " - " + str(self.end_time.hour) + ":"+ e_min + " ]"
	class Meta:
		verbose_name_plural = "Shift"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Department_id'], name='ShiftName is Unique for Department')
        ]
	def save(self, *args, **kwargs):
		if self.end_time > self.start_time:
			super(Shift, self).save(*args, **kwargs)
		else :
			raise BaseException("End time must be greater then start time")

class Working_days(models.Model):
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	Days_id = models.ForeignKey(Days,default=None,on_delete=models.RESTRICT)
	def __str__(self):
		return str(self.Days_id) #+ " "+ str(self.Shift_id)
	class Meta:
		verbose_name_plural = "Working Days"
		constraints = [
			models.UniqueConstraint(fields=['Shift_id', 'Days_id'], name='Day only once for shift')
        ]

class Branch(models.Model):
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Branch"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Department_id'], name='BranchName is Unique for Department'),
			models.UniqueConstraint(fields=['short', 'Department_id'], name='BranchShort is Unique for Department'),
		]

class WEF_manager(models.Manager):
	def active(self):
		'Get all the active WEFs in the db'
		return super().get_queryset().filter(active=True)
	def inactive(self):
		'Get all the inactive WEFs in the db'
		return super().get_queryset().filter(active=False)

class WEF(models.Model):
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	name = models.CharField(max_length=N_len)
	start_date = models.DateField(auto_now_add=False)
	end_date = models.DateField(auto_now_add=False)
	active = models.BooleanField(default=False)
	objects = WEF_manager()

	def __str__(self):
		return "{} ({})".format(self.name,self.get_range())
	
	def get_start_date(self):
		return self.start_date.strftime("%d/%m/%Y")

	def get_end_date(self):
		return self.end_date.strftime("%d/%m/%Y")

	def get_percent_completed(self):
		# if it is still going
		import time	
		t = lambda dt:time.mktime(dt.timetuple())
		def percent(start_time, end_time, current_time):
			total = t(end_time) - t(start_time)
			current = t(current_time) - t(start_time)
			return int((100.0 * current) / total)
		per = percent(self.start_date,self.end_date,datetime.datetime.now())
		if per < 0 :
			return 0
		if per > 100:
			return 100
		return per

	def get_range(self):
		'return formated date range as dd/mm/yyyy - dd/mm/yyyy'
		return "%s - %s"%(self.start_date.strftime("%d/%m/%Y"),self.end_date.strftime("%d/%m/%Y"))
	
	def update(self,today):		
		# active= True if today is between start and end
		if self.start_date <= today < self.end_date:
			if not self.active: # if it was inactive and now is switched
				from subject_V1.models import Subject_event
				active_subj_events = Subject_event.objects.active().filter(Subject_id__Semester_id__in = self.semester_set.all())
				# get all the active subj_events and 
				# add the start_date and end_date to subject_events
				for i in active_subj_events:
					i.start_date = self.start_date
					i.end_date = self.end_date
					i.save()
				self.active = True
		else:
			if self.active: # if it was active and now is switched
				from subject_V1.models import Subject_event
				active_subj_events = Subject_event.objects.active().filter(Subject_id__Semester_id__in = self.semester_set.all())
				# get all the active subj_events and 
				# make subject_event.active = False
				for i in active_subj_events:
					i.active = False
					i.save()
				# change the subject_event__active to False
				pass
				self.active = False
			
	@staticmethod
	def update_all_WEF():
		today = datetime.date.today()
		for i in WEF.objects.all():
			i.save()

	def save(self,*args, **kwargs):
		self.update(datetime.date.today())
		super(WEF,self).save(*args,**kwargs)

	class Meta:
		verbose_name_plural = "WEF"

# from django_q.tasks import schedule

# schedule('WEF.update_all_WEF', name=None, schedule_type='M',
# 	minutes=None, repeats=-1, next_run=datetime.datetime.now()+datetime.timedelta(minutes=1), q_options=None)

class Semester_WEF_manager(models.Manager):
	def active(self):
		'Get all the Semesters having active WEFs or future WEFs in the db'
		return super().get_queryset().filter(Q(WEF_id__active=True) |Q(WEF_id__start_date__gte=datetime.datetime.today()))

	def inactive(self):
		'Get all the Semesters having inactive WEFs in the db'
		return super().get_queryset().filter(WEF_id__active=False)

class Semester(models.Model):
	short = models.CharField(max_length = 20)
	Branch_id = models.ForeignKey(Branch,default=None,on_delete = models.CASCADE)
	WEF_id = models.ForeignKey(WEF,on_delete=models.SET_NULL,null=True,blank=True)
	objects = Semester_WEF_manager()	
	
	def __str__(self):
		return self.short
	
	class Meta:
		verbose_name_plural = "Semester"
		constraints = [
			models.UniqueConstraint(fields=['short', 'Branch_id'], name='Semester Short is Unique for Branch'),
		]

class Division_WEF_manager(models.Manager):
	def active(self):
		'Get all the Division having active WEFs in the db'
		return super().get_queryset().filter(Semester_id__WEF_id__active=True)
	def inactive(self):
		'Get all the Division having inactive WEFs in the db'
		return super().get_queryset().filter(Semester_id__WEF_id__active=False)

class Division(models.Model):
	name = models.CharField(max_length = S_len)
	Semester_id = models.ForeignKey(Semester,default=None,on_delete = models.CASCADE)
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	link = models.URLField(max_length=200, null=True, blank=True)
	objects = Division_WEF_manager()
	Resource_id = models.ForeignKey(Resource,default=None,on_delete = models.SET_NULL, null=True, blank=True)
	

	def __str__(self):
		return "%s (%s)" % (self.name,str(self.Semester_id))
	
	def save(self, *args, **kwargs):
		from subject_V1.models import Subject_details
		super(Division, self).save(*args,**kwargs)
		subjects_for_semester = self.Semester_id.subject_details_set.all()
		for subject in subjects_for_semester:
			subject.set_load()
			subject.save()

	def delete(self, *args, **kwargs):
		from subject_V1.models import Subject_details
		subjects_for_semester = self.Semester_id.subject_details_set.all()
		super(Division, self).delete(*args, **kwargs)
		for subject in subjects_for_semester:
			subject.set_load()
			subject.save()

	class Meta:
		verbose_name_plural = "Division"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Semester_id'], name='Division Name is Unique for Semester'),
		]


# import subject_V1.models.Subject_details as subject
from subject_V1.models import Subject_details
class Batch(models.Model):
	BATCH_FOR = (
		('lect', 'Lecture'),
		('prac', 'Practical'),
	)
	name = models.CharField(max_length = S_len)
	batch_for = models.CharField(max_length = 4 ,choices=BATCH_FOR)
	Division_id = models.ForeignKey(Division,default=None,on_delete = models.CASCADE)
	link = models.URLField(max_length=200, null=True, blank=True)
	subjects_for_batch = models.ManyToManyField(Subject_details)

	def save(self, *args, **kwargs):
		super(Batch, self).save(*args,**kwargs)
		subjects_for_batch = list(self.subjects_for_batch.all())
		for subject in subjects_for_batch:
			subject.set_load()
			subject.save()

	def delete(self, *args, **kwargs):
		subjects_for_batch = list(self.subjects_for_batch.all())
		super(Batch, self).delete(*args, **kwargs)
		for subject in subjects_for_batch:
			subject.set_load()
			subject.save()


	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Batch"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Division_id'], name='BatchName is Unique for Division'),
		]


class Timings(models.Model):
	name = models.CharField(max_length = 20)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	is_break = models.BooleanField(default=False)
	def return_time(self):
		def get_minutes(min):
			if min < 10:
				return f'0{min}'
			return f'{min}'
		s_min = get_minutes(self.start_time.minute)
		e_min = get_minutes(self.end_time.minute)

		return str(self.start_time.hour) + ":"+ s_min + " - " + str(self.end_time.hour) + ":"+ e_min 
	def __str__(self):
		return self.name + " [ " + self.return_time() +" ]"
	class Meta:
		verbose_name_plural = "Timings"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Shift_id'], name='SlotName is Unique for Shift'),
		]
	def save(self, *args, **kwargs):
		if self.end_time > self.start_time:
			super(Timings, self).save(*args, **kwargs)
		else :
			raise BaseException("End time must be greater then start time")
	
class Slots(models.Model):	
	day = models.ForeignKey(Working_days,blank=False,on_delete=models.CASCADE)
	Timing_id = models.ForeignKey(Timings,blank=False,on_delete=models.RESTRICT)
	def __str__(self):
		if self.Timing_id.is_break:
			return "Break" + " [ " + self.Timing_id.return_time() +" ]"	
		return str(self.day) + " [ " + self.Timing_id.return_time() +" ]"
	def get_time(self):
		return " [ " + self.Timing_id.return_time() +" ]"
	class Meta:
		verbose_name_plural = "Slots"

class try_model(models.Model):
	user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True,blank=True)
	display_image = models.ImageField(null=True, blank=True)