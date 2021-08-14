from django.db import models

################################################

from institute_V1.models import Division,Batch,Institute
from django.contrib.auth import get_user_model

################################################

N_len = 50

class Student_details(models.Model):
	User_id = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
	display_image = models.ImageField(null=True,blank=True)
	
	roll_no = models.CharField(max_length = 20)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	Division_id = models.ForeignKey(Division,on_delete=models.SET_NULL,null=True)
	prac_batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True,related_name="practical_batch+")
	lect_batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True,related_name="lecture_batch+")
	# objects = WEF()
	def __str__(self):
		return self.User_id.first_name
	class Meta:
		verbose_name_plural = "Student Details"


class User_notes(models.Model):
	User_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)

	title = models.TextField()
	body = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		return f"{str(self.User_id)} -> {str(self.title)}"
	
	class Meta:
		verbose_name_plural = "User Notes"

	def save(self, *args, **kwargs):
		import cryptocode
		key_str = f"{self.User_id}_{self.User_id.pk}"
		encode = lambda x: cryptocode.encrypt(x,key_str)
		self.title = encode(self.title)
		self.body = encode(self.body)
		super(User_notes, self).save(*args, **kwargs)

class Student_logs(models.Model):
	user_id = models.ForeignKey(get_user_model(),default=None,null=True,on_delete = models.SET_NULL)
	action = models.CharField(max_length=64)
	Division_id = models.ForeignKey(Division,default=None,null=True,on_delete = models.SET_NULL)
	timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	ip = models.GenericIPAddressField(null=True)
	def __str__(self):
		if self.user_id:
			return '{0} - {1} - {2}'.format(self.user_id, self.action, self.ip)
	class Meta:
		verbose_name_plural = "Student Logs"