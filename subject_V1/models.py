from django.db import models

################################################

from institute_V1.models import Semester,Division
################################################

N_len = 50
S_len = 10
# class Subject_manager(models.Manager):
# 	def get(self, *args, **kwargs):
# 		qs = super(Subject_manager, self).get( *args, **kwargs)
# 		# for i in qs:
# 		qs.set_load(False)
# 		return qs
	
# 	def filter(self, *args, **kwargs):
# 		qs = super(Subject_manager, self).filter( *args, **kwargs)
# 		for i in qs:
# 			i.set_load(False)
# 		return qs


class Subject_details(models.Model):
	Semester_id = models.ForeignKey(Semester,on_delete=models.RESTRICT)
	name = models.CharField(max_length=N_len)
	short = models.CharField(max_length=S_len)
	lect_per_week = models.PositiveIntegerField(null= True,blank = True)
	prac_per_week = models.PositiveIntegerField(null= True,blank = True)
	load_per_week = models.PositiveIntegerField(default = 0)
	color = models.CharField(max_length = 7)
	# objects = Subject_manager()
	def remaining_lect_prac(self):
		p,l = self.get_prac_lect()
		total_prac = p * self.prac_per_week
		total_lect = l * self.lect_per_week
		taken_lect = taken_prac = 0
		for event in Subject_event.objects.active().filter(Subject_id=self):
			taken_prac += event.prac_carried
			taken_lect += event.lect_carried
		remaining_prac = total_prac - taken_prac
		remaining_lect = total_lect - taken_lect
		return remaining_lect,remaining_prac
		
	def get_prac_lect(self):
		prac_batch = lect_batch = 0
		no_of_div = len(Division.objects.filter(Semester_id=self.Semester_id))

		lect_batch = self.batch_set.filter(batch_for = "lect").count()
		prac_batch = self.batch_set.filter(batch_for = "prac").count()

		lect_batch = no_of_div if lect_batch == 0 else lect_batch
		prac_batch = no_of_div if prac_batch == 0 else prac_batch
		return prac_batch,lect_batch

	def set_load(self,save = False):
		if not self.lect_per_week:
			self.lect_per_week = 0
		if not self.prac_per_week:
			self.prac_per_week = 0
		prac_batch,lect_batch = self.get_prac_lect()
			# if batch  is 0 make it 1 for the formula
		self.load_per_week = (self.lect_per_week * lect_batch) + 2 * (self.prac_per_week * prac_batch)
		# print(f"changing load of {self.name} to {self.load_per_week}")

	def save(self, *args, **kwargs):	# for calculating the load before saving
		self.set_load()
		super(Subject_details, self).save(*args, **kwargs)

	def __str__(self):
		return self.short

	class Meta:
		verbose_name_plural = "Subject Details"
		constraints = [
			models.UniqueConstraint(fields=['short', 'Semester_id'], name='Subject Short is Unique for Semester.'),
			models.UniqueConstraint(fields=['name', 'Semester_id'], name='Subject Name is Unique for Semester.')
        ]	

class active_manager(models.Manager):
	def active(self):
		'Get all the Subject_events having active in the db'
		return super().get_queryset().filter(active=True)
	def inactive(self):
		'Get all the Subject_events having active = False in the db'
		return super().get_queryset().filter(active=False)

class Subject_event(models.Model):
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	Faculty_id = models.ForeignKey("faculty_V1.Faculty_details",on_delete=models.CASCADE)
	# link = models.URLField(max_length=200, null=True, blank=True)
	prac_carried = models.PositiveIntegerField()
	lect_carried = models.PositiveIntegerField()
	objects = active_manager()
	# RelatedManager
	active = models.BooleanField(default=True)
	start_date = models.DateField(auto_now_add=False,null=True, blank=True,default=None)
	end_date = models.DateField(auto_now_add=False,null=True, blank=True,default=None)
	'''
		default is active. When WEF starts startdate and enddate are set 
		and when it ends actve=False
	'''
	# add a function to count the load remaining from the Event table and use distince(Slot_id)
	# this will be usefull for timetable algo when the batches will be mearged
	def total_load_carried(self):
		return (self.prac_carried * 2) + self.lect_carried
	
	def __str__(self):
		self.Subject_id.get_prac_lect()
		return str(self.pk) + " "+ self.Subject_id.short + " by " + str(self.Faculty_id)

	class Meta:
		verbose_name_plural = "Subject events"
		constraints = [
			models.UniqueConstraint(fields=['Faculty_id', 'Subject_id'], name='Subject can have only one Unique Faculty.'),
		]