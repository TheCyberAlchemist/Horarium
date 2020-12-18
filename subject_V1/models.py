from django.db import models

################################################

from institute_V1.models import Semester,Batch,Division

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

	def get_prac_lect(self):
		prac_batch = lect_batch = 0
		no_of_div = len(Division.objects.filter(Semester_id=self.Semester_id))
		for batch in Batch.objects.filter(Division_id__Semester_id = self.Semester_id):
			lect_batch += 1 if batch.batch_for == "lect" else 0	# total batches of lecture
			prac_batch += 1 if batch.batch_for == "prac" else 0	# total batches of practical
		lect_batch = no_of_div if lect_batch == 0 else lect_batch
		prac_batch = no_of_div if prac_batch == 0 else prac_batch
		return prac_batch,lect_batch

	def save(self, *args, **kwargs):	# for calculating the load before saving
		if not self.lect_per_week:
			self.lect_per_week = 0
		if not self.prac_per_week:
			self.prac_per_week = 0
		prac_batch,lect_batch = self.get_prac_lect()
			# if batch  is 0 make it 1 for the formula
		self.load_per_week = (self.lect_per_week * lect_batch) + 2 * (self.prac_per_week * prac_batch)
		super(Subject_details, self).save(*args, **kwargs) 

	def __str__(self):
		return self.short

	class Meta:
		verbose_name_plural = "Subject Details"	
		constraints = [
            models.UniqueConstraint(fields=['short', 'Semester_id'], name='Subject Short is Unique for Semester.'),
			models.UniqueConstraint(fields=['name', 'Semester_id'], name='Subject Name is Unique for Semester.')
        ]	

class Subject_event(models.Model):
	Subject_id = models.ForeignKey(Subject_details,on_delete=models.CASCADE)
	Faculty_id = models.ForeignKey("faculty_V1.Faculty_details",on_delete=models.CASCADE)
	link = models.URLField(max_length=200, null=True, blank=True)
	prac_carried = models.PositiveIntegerField()
	lect_carried = models.PositiveIntegerField()
	def total_load_carried(self):
		return (self.prac_carried * 2) + self.lect_carried
	def __str__(self):
		self.Subject_id.get_prac_lect()
		return self.Subject_id.short + " by " + str(self.Faculty_id)
	class Meta:
		verbose_name_plural = "Subject events"	