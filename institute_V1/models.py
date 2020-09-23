from django.db import models

################################################
N_len = 50
S_len = 10

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
	Institute

class Department(models.Model):
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	Institute_id = models.ForeignKey(Institute,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Department"

class Shift(models.Model):
	name = models.CharField(max_length = N_len)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Shift"

class Course(models.Model):
	name = models.CharField(max_length = N_len)
	short = models.CharField(max_length = S_len)
	Department_id = models.ForeignKey(Department,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Course"

class Semester(models.Model):
	short = models.CharField(max_length = 20)
	Course_id = models.ForeignKey(Course,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.short
	class Meta:
		verbose_name_plural = "Semester"

class Division(models.Model):
	name = models.CharField(max_length = S_len)
	Semester_id = models.ForeignKey(Semester,default=None,on_delete = models.CASCADE)
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	def __str__(self):
		return self.name + " "+ str(self.Semester_id)
	class Meta:
		verbose_name_plural = "Division"

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
		
class Slots(models.Model):
	name = models.CharField(max_length = S_len)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	Shift_id = models.ForeignKey(Shift,default=None,on_delete = models.CASCADE)
	def __str__(self):
		s_min = "00" if self.start_time.minute == 0 else str(self.start_time.minute)
		e_min = "00" if self.end_time.minute == 0 else str(self.end_time.minute)
		return self.name + " [ " + str(self.start_time.hour) + ":"+ s_min + " - " + str(self.end_time.hour) + ":"+ e_min + " ]"
	class Meta:
		verbose_name_plural = "Slots"