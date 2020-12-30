from django.forms import ModelForm
from institute_V1.models import Department,Branch,Semester,Division,Batch,Shift,Resource
from faculty_V1.models import Faculty_details,Faculty_designation,Faculty_load,Can_teach
from subject_V1.models import Subject_details,Subject_event
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
from student_V1.models import Student_details
from institute_V1.models import Timings

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
		fields = ['name','Shift_id']


class create_batch(ModelForm):
	class Meta:
		model = Batch
		fields = ['name','batch_for']


class faculty_details(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id','Designation_id']


class faculty_load(ModelForm):
	class Meta:
		model = Faculty_load
		fields = ['total_load']


class add_user(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','password1','password2']


class add_resource(ModelForm):
	class Meta:
		model = Resource
		fields = ["name","block"]

# class update_user_by_admin(AbstractUser):
# 	class Meta:
# 		# model = get_user_model()
# 		fields = ['first_name','last_name']

class add_subject_details(ModelForm):
	class Meta:
		model = Subject_details
		fields = ["name","Semester_id","short","lect_per_week", "prac_per_week", "color"]


class add_sub_event(ModelForm):
	class Meta:
		model = Subject_event
		fields = ["Faculty_id","lect_carried", "prac_carried","link"]

class update_sub_event(ModelForm):
	class Meta:
		model = Subject_event
		fields = ["lect_carried", "prac_carried","link"]

class student_details(ModelForm):
	class Meta:
		model = Student_details
		fields = ('roll_no','Division_id','Batch_id',)


class shift(ModelForm):
	class Meta:
		model = Shift
		fields = ('name','start_time','end_time')


class timing(ModelForm):
	class Meta:
		model = Timings
		fields = ('name','start_time','end_time','is_break')
