from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from institute_V1.models import *
from faculty_V1.models import *
from subject_V1.models import Subject_details,Subject_event
from student_V1.models import Student_details
from institute_V1.models import Timings
from Table_V2.models import Event


class create_department(ModelForm):
	class Meta:
		model = Department
		fields = ['name','short']


class create_branch(ModelForm):
	class Meta:
		model = Branch
		fields = ['name','short']

class create_feedback_type(ModelForm):
	class Meta:
		model = Feedback_type
		fields = ['name','for_date']

class create_semester(ModelForm):
	class Meta:
		model = Semester
		fields = ['short',"WEF_id"]


class create_division(ModelForm):
	class Meta:
		model = Division
		fields = ['name','Shift_id','link','Resource_id']

class create_batch(ModelForm):
	class Meta:
		model = Batch
		fields = ['name','batch_for','link','subjects_for_batch']


class faculty_details(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id','Designation_id','Resource_id']

class faculty_details_csv(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id','Designation_id','Department_id']

class faculty_load(ModelForm):
	class Meta:
		model = Faculty_load
		fields = ['total_load']


class add_user(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','password1','password2']


class update_user_name_email(ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email']


class add_resource(ModelForm):
	class Meta:
		model = Resource
		fields = ["name","block","is_lab"]


class add_subject_details(ModelForm):
	class Meta:
		model = Subject_details
		fields = ["name","Semester_id","short","lect_per_week", "prac_per_week", "color"]


class add_sub_event(ModelForm):
	class Meta:
		model = Subject_event
		fields = ["Faculty_id","Co_faculty_id","lect_carried", "prac_carried"]
	def clean(self):
		cleaned_data = super().clean()
		Co_faculty_id = cleaned_data.get('Co_faculty_id')
		Faculty_id = cleaned_data.get('Faculty_id')
		print(Faculty_id,Co_faculty_id)
		if Faculty_id and Co_faculty_id:
			if Co_faculty_id == Faculty_id:
				raise ValidationError("Same faculty in both fields.")
			elif Co_faculty_id.Shift_id != Faculty_id.Shift_id:
				raise ValidationError("Both faculties have different shifts.")
class update_sub_event(ModelForm):
	class Meta:
		model = Subject_event
		fields = ["lect_carried", "prac_carried"]

class student_details(ModelForm):
	class Meta:
		model = Student_details
		fields = ('roll_no','Division_id','prac_batch','lect_batch')


class shift(ModelForm):
	class Meta:
		model = Shift
		fields = ('name','start_time','end_time')


class timing(ModelForm):
	class Meta:
		model = Timings
		fields = ('name','start_time','end_time','is_break')


class add_event(ModelForm):
	
	class Meta:
		model = Event
		fields = ("Slot_id","Slot_id_2","Batch_id","Subject_event_id","Resource_id","link")