from django.shortcuts import render
from django.views import View
from institute_V1.models import *
from .forms import *
# Create your views here.

class Exam(View):
	template_name = ".html"
	
	def get_context_data(self,Semester_id):
		'Returns the common context data for the methods'
		my_semester = Semester.objects.get(id=Semester_id).first()
		my_exams = Exam.objects.all().filter(Semester_id=my_semester)
		context = {
			'my_semester':my_semester,
			"my_exams":my_exams,
		}
		return context
	
	def get(self, request,Semester_id=None):
		pass
		context = self.get_context_data(Semester_id)
		# return render(request,self.template_name,context)

	def post(self, request):
		pass
		context = self.get_context_data(Semester_id)
		if request.is_ajax(): # if delete is called
			data = json.loads(request.body)
			for d in data:
				instance = Exam.filter(pk = d).first()
				if instance:
					instance.delete()
		else: # if form is submitted
			form = create_exam(request)
			if form.is_valid():
				form.save()
			else:
				context['errors'] = form.errors.as_ul()
				print(context['errors'])
		# return render(request,self.template_name,context)

class Subject_exam(View):
	template_name = ""
	def get(self, request):
		pass
		# context = {

		# }
		# return render(request,self.template_name,context)
	def post(self, request):
		pass
		# context = {
			
		# }
		# return render(request,self.template_name,context)