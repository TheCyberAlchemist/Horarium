from django.forms import ModelForm
from institute_V1.models import Department,Branch,Semester,Division,Batch
from faculty_V1.models import Faculty_details,Faculty_designation,Faculty_load
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from student_V1.models import Student_details


class create_department(ModelForm):
	class Meta:
		model = Department
		fields = ['name','short']


class create_branch(ModelForm):
	class Meta:
		model = Branch
		fields = ['name','short']


class create_semester(ModelForm):
	class Meta:
		model = Semester
		fields = ['short']


class create_division(ModelForm):
	class Meta:
		model = Division
		fields = ['name']


class create_batch(ModelForm):
	class Meta:
		model = Batch
		fields = ['name','batch_for']


class faculty_details(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id']


class faculty_load(ModelForm):
	class Meta:
		model = Faculty_load
		fields = ['total_load']


class add_user(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','password1','password2']


class student_details(ModelForm):
	class Meta:
		model = Student_details
		fields = ('roll_no','Division_id','Batch_id',)

from institute_V1.models import Slots
import datetime
class slot(ModelForm):
	def add(self,addend):

		a = datetime.datetime(100,1,1,self.instance.start_time.hour,self.instance.start_time.minute,00)
		b = a + datetime.timedelta(minutes=addend) # days, seconds, then other fields.
		self.instance.start_time = b.time()

		a = datetime.datetime(100,1,1,self.instance.end_time.hour,self.instance.end_time.minute,00)
		b = a + datetime.timedelta(minutes=addend) # days, seconds, then other fields.
		self.instance.end_time = b.time()

	def duration(self):
		return self.instance.end_time - self.instance.start_time
	class Meta:
		model = Slots
		fields = ('name','start_time','end_time','is_break')
