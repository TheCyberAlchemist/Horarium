from django.forms import ModelForm
from institute_V1.models import Department,Branch,Semester,Division,Batch
from faculty_V1.models import Faculty_details,Faculty_designation,Faculty_load
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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

class faculty_user(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','password1','password2']