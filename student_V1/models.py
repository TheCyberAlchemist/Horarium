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
		return str(self.User_id)
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
	
	def created_at_str(self):
		'returns when the note was created'
		from datetime import datetime
		from calendar import monthrange
		date_1 = str(self.timestamp)
		date_2 = str(datetime.today())
		date_format_str = '%Y-%m-%d %H:%M:%S.%f'

		start = datetime.strptime(date_1, date_format_str)
		end =  datetime.strptime(date_2, date_format_str)

		# Get interval between two timstamps as timedelta object
		diff = end - start
		# Get interval between two timstamps in hours
		diff_in_hours = diff.total_seconds() / 3600

		date = date_1.split(' ')[0]   ### gives date without time
		current_date = int(date.split('-')[0])  ## gives the current date 
		year = int(date.split('-')[2])  
		month = int(date.split('-')[1])

		if diff_in_hours <=24 :
			return "Created Today" 

		elif (diff_in_hours > 24 and diff_in_hours < 48) :
			return f"Created 1 day ago"

		elif (diff_in_hours >= 48 and diff_in_hours <  720):
			created = int(diff_in_hours/24)
			return f"Created {created} days ago at {date.split('-')[1]}/{current_date}"

		elif (diff_in_hours >=720) : 
			total_days_in_month = monthrange(year,month)[1]
			created = int(diff_in_hours/24/total_days_in_month)
			if created <= 1 :
				return(f"Created {created} month ago at {date}")
			return(f"Created {created} months ago at {date}")
	def save(self, *args, **kwargs):
		import cryptocode
		key_str = f"9ezXqxqL_{self.User_id.pk}"
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
