from django.db import models
from django.contrib.auth import get_user_model
from institute_V1.models import Institute
# Create your models here.

class Admin_details(models.Model):
	User_id = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,primary_key=True)
	Institute_id = models.ForeignKey(Institute,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.User_id)
	class Meta:
		verbose_name_plural = "Admin Details"
	
