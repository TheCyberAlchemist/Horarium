from django.forms import ModelForm
from .models import *
class faculty_details(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id','Designation_id']

class faculty_details_csv(ModelForm):
	class Meta:
		model = Faculty_details
		fields = ['short','Shift_id','Designation_id','Department_id']

class faculty_load(ModelForm):
	class Meta:
		model = Faculty_load
		fields = ['total_load']

