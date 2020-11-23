from django.db import models

################################################

from institute_V1.models import Semester,Batch

################################################

N_len = 50
S_len = 10

class Subject_details(models.Model):
	Semester_id = models.ForeignKey(Semester,on_delete=models.RESTRICT)
	name = models.CharField(max_length=N_len)
	short = models.CharField(max_length=S_len)
	lect_per_week = models.PositiveIntegerField(null= True,blank = True)
	prac_per_week = models.PositiveIntegerField(null= True,blank = True)
	load_per_week = models.PositiveIntegerField(default = 0)
	color = models.CharField(max_length = 7)
	
	def save(self, *args, **kwargs):	# for calculating the load before saving
		prac_batch = lect_batch = 0
		if not self.lect_per_week:
			self.lect_per_week = 0
		if not self.prac_per_week:
			self.prac_per_week = 0
		for batch in Batch.objects.all():
			if batch.Division_id.Semester_id == self.Semester_id:	# checking all the batches in same Sem as the subject
				lect_batch += 1 if batch.batch_for == "lect" else 0	# total batches of lecture
				prac_batch += 1 if batch.batch_for == "prac" else 0	# total batches of practical

		lect_batch = 1 if lect_batch == 0 else lect_batch
		prac_batch = 1 if prac_batch == 0 else prac_batch
			# if batch  is 0 make it 1 for the formula
		self.load_per_week = (self.lect_per_week * lect_batch) + 2 * (self.prac_per_week * prac_batch)
		super(Subject_details, self).save(*args, **kwargs) 

	def __str__(self):
		return self.short

	class Meta:
		verbose_name_plural = "Subject Details"	

class Subject_event(models.Model):
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	# from faculty_V1.models import Faculty_details
	Faculty_id = models.ForeignKey("faculty_V1.Faculty_details",on_delete=models.CASCADE)
	link = models.URLField(max_length=200, null=True, blank=True)
	load_carried = models.PositiveIntegerField()

	def __str__(self):
		return self.Subject_id.short + " by " + self.Faculty_id.short
	class Meta:
		verbose_name_plural = "Subject events"	