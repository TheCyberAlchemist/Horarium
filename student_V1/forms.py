from django.forms import ModelForm

from .models import Student_details
from faculty_V1.models import Feedback

class add_student_form(ModelForm):
	class Meta:
		model = Student_details
		fields = ["User_id","display_image"]

class add_student_details(ModelForm):
	class Meta:
		model = Student_details
		fields = ["roll_no","Institute_id","Division_id","prac_batch","lect_batch"]


class feedback_form(ModelForm):
	class Meta:
		model = Feedback
		fields = ['Q1',"Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","query"]

class mandatory_feedback_form(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['Q1'].required = True
		self.fields['Q2'].required = True
		self.fields['Q3'].required = True
		self.fields['Q4'].required = True
		self.fields['Q5'].required = True
		self.fields['Q6'].required = True
		self.fields['Q7'].required = True
		self.fields['Q8'].required = True
		self.fields['Q9'].required = True

	class Meta:
		model = Feedback
		fields = ['Q1',"Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","query"]