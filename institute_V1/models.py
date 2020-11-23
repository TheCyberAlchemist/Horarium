from django.db import models
from django.contrib.auth import get_user_model
from django.db import IntegrityError
################################################
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
	name = models.CharField(max_length = S_len)
	block = models.CharField(max_length = S_len)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	def __str__(self):
		return self.name

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

class Working_days(models.Model):
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	Days_id = models.ForeignKey(Days,default=None,on_delete=models.RESTRICT)
	def __str__(self):
		return str(self.Shift_id) + " "+ str(self.Days_id)
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

class Semester(models.Model):
	short = models.CharField(max_length = 20)
	Branch_id = models.ForeignKey(Branch,default=None,on_delete = models.CASCADE)
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
	def __str__(self):
		return self.name + " "+ str(self.Semester_id)
	class Meta:
		verbose_name_plural = "Division"
		constraints = [
			models.UniqueConstraint(fields=['name', 'Semester_id'], name='Division Name is Unique for Semester'),
		]

class Batch(models.Model):
	BATCH_FOR = (
		('lect', 'Lecture'),
		('prac', 'Practical'),
	)
	name = models.CharField(max_length = S_len)
	batch_for = models.CharField(max_length = 4 ,choices=BATCH_FOR)
	Division_id = models.ForeignKey(Division,default=None,on_delete = models.CASCADE)
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
	day = models.ForeignKey(Days,blank=False,on_delete=models.RESTRICT)
	Timing_id = models.ForeignKey(Timings,blank=False,on_delete=models.RESTRICT)
	def __str__(self):
		return str(self.day) + " [ " + self.Timing_id.return_time() +" ]"
	class Meta:
		verbose_name_plural = "Slots"