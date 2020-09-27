from django.forms import ModelForm
from institute_V1.models import Department,Branch,Semester,Division,Batch


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
