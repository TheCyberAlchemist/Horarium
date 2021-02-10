from django.forms import ModelForm


from faculty_V1.models import Feedback

class feedback_form(ModelForm):
	class Meta:
		model = Feedback
		fields = ["Event_id",'Q1',"Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","query"]