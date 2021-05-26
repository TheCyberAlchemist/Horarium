from django.db import models
from django.contrib.auth import get_user_model
from django.db import IntegrityError

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
	block = models.CharField(max_length = N_len)

	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	def __str__(self):
		return self.name
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
		return super().get_queryset().filter(active=True)
	def inactive(self):
		return super().get_queryset().filter(active=False)

# add what is related to wef (Branch)
class WEF(models.Model):
	Department_id = models.ForeignKey(Department,default=None	,on_delete = models.CASCADE)
	name = models.CharField(max_length=N_len)
	start_date = models.DateField(auto_now_add=False)
	end_date = models.DateField(auto_now_add=False)
	active = models.BooleanField(default=False)
	objects = models.Manager()
	WEF_manager = WEF_manager()

	def __str__(self):
		return "{} ({}---{})".format(self.name,str(self.start_date),str(self.end_date))
	
	def get_percent_completed(self):
		# if the WEF is completed
		if completed:
			return 100
		# if it is still going
		import time
		
		t = lambda dt:time.mktime(dt.timetuple())
		def percent(start_time, end_time, current_time):
			total = t(end_time) - t(start_time)
			current = t(current_time) - t(start_time)
			return (100.0 * current) / total

		return percent(self.start_date,self.end_date,datetime.date.now())

	def update(self,today):
		self.active = self.start_date <= today < self.end_date
		print("this is update")
		self.save()
		# active = True if today is between start and end
		# else active = False
			
	@staticmethod
	def update_all_WEF():
		today = datetime.date.today()
		for i in WEF.objects.all():
			i.update(today)

	class Meta:
		verbose_name_plural = "WEF"

# from django_q.tasks import schedule

# schedule('WEF.update_all_WEF', name=None, schedule_type='M',
# 	minutes=None, repeats=-1, next_run=datetime.datetime.now()+datetime.timedelta(minutes=1), q_options=None)


class Semester(models.Model):
	short = models.CharField(max_length = 20)
	Branch_id = models.ForeignKey(Branch,default=None,on_delete = models.CASCADE)
	WEF_id = models.ForeignKey(WEF,on_delete=models.RESTRICT,null=True,blank=True)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Semester"
		constraints = [
			models.UniqueConstraint(fields=['short', 'Branch_id'], name='Semester Short is Unique for Branch'),
		]

class Division(models.Model):
	name = models.CharField(max_length = S_len)
	Semester_id = models.ForeignKey(Semester,default=None,on_delete = models.CASCADE)
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	link = models.URLField(max_length=200, null=True, blank=True)
	def __str__(self):
		return self.name + " "+ str(self.Semester_id)
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

	def delete(self, *args, **kwargs):
		subjects_for_batch = list(self.subjects_for_batch.all())
		super(Batch, self).delete(*args, **kwargs)
		for subject in subjects_for_batch:
			subject.set_load()


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
		s_min = "00" if self.start_time.minute == 0 else str(self.start_time.minute)
		e_min = "00" if self.end_time.minute == 0 else str(self.end_time.minute)
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