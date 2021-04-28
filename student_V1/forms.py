from django.forms import ModelForm

from .models import Student_details
from faculty_V1.models import Feedback

class add_student_form(ModelForm):
	class Meta:
		model = Student_details
		fields = ["User_id","display_image"]

class feedback_form(ModelForm):
	class Meta:
		model = Feedback
		fields = ["Event_id",'Q1',"Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","query"]