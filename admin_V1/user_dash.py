from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.urls import reverse


from ajax_datatable.views import AjaxDatatableView
import login_V2.models as login_V2
from subject_V1.models import Subject_event
from faculty_V1.models import Faculty_load

# https://pypi.org/project/django-ajax-datatable/#sorting-columns
class student_user_table(AjaxDatatableView):
	model = login_V2.CustomUser
	title = 'Student_details'
	initial_order = [["Department", "asc"]]
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{'name': 'first_name', 'visible': True,'searchable': True,'orderable': True,'title': 'Name',},
		{'name': 'email', 'visible': True,'searchable': True,'title': 'Email', },
		{
			'name': 'Roll No',
			'foreign_field': 'student_details__roll_no',
			'visible': True,
			'searchable': True,
			'placeholder':'roll no.'
		}, # roll no showing
		{			
			'name':'Department',
			'foreign_field': 'student_details__Division_id__Semester_id__Branch_id__Department_id__short',
			'visible': True,
			'searchable':True,
			'placeholder':"Dept.",
		}, # department showing
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False
		}, # delete field
		### search fields ###

		{'name': 'last_name', 'visible': False,'searchable': True},
		{
			'name':'Division',
			'foreign_field': 'student_details__Division_id__name',
			'visible': False,
			'searchable':True,
		}, # division not showing
		{
			'name':'Semester',
			'foreign_field': 'student_details__Division_id__Semester_id__short',
			'visible': False,
			'searchable':True,
		}, # Semester not showing
		{
			'name':'Branch',
			'foreign_field': 'student_details__Division_id__Semester_id__Branch_id__short',
			'visible': False,
			'searchable':True,
		}, # Branch not showing
	]

	def get_initial_queryset(self, request=None):
		if not request.user.is_authenticated:
			raise PermissionDenied
		queryset = self.model.objects.filter(student_details__pk__isnull=False)
		# queryset = self.model.objects.all()
		return queryset

	def render_row_details(self, pk, request=None):
		obj = self.model.objects.get(pk=pk)
		# fields = [f for f in self.model._meta.get_fields() if f.concrete]
		student_details = obj.student_details
		fields = {
			'Division':student_details.Division_id,
			'Batch':student_details.Batch_id,
		}
		fields['Semester'] = fields['Division'].Semester_id
		fields['Branch'] = fields['Semester'].Branch_id
		# print(student_details.Division_id.Semester_id)
		html = '<table class="row-details" style="width:100%">'
		for key in fields:
		    html += '<tr><td class="fw-bold">%s</td><td class="fw-bold">%s</td></tr>' % (key, fields[key])

		html += '</table>'
		return html
	
	def get_show_column_filters(self, request):
		return None

	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['first_name'] = '<div class="gixi gixi-md float-start" data-gixiseed="%s_%s"></div>'%(obj,obj.pk) + str(obj)
		row['Edit'] = '''<td class="border-0">
							<i class="fas fa-edit" onclick="student_edit_called(%s)"></i>
						</td>''' % (
			obj.id
		)
		row['Delete'] ='''<div class="form-check" onclick="checkSelected()">
							<input class="form-check-input del_input" type="checkbox"
							name="del" value="%s" input_name="%s">
						</div>''' % (
						obj.pk,str(obj)
					)
		# if obj.recipe is not None:
		# 	row['recipe'] = obj.recipe.display_as_tile() + ' ' + str(obj.recipe)
		return

class faculty_user_table(AjaxDatatableView):
	
	model = login_V2.CustomUser
	title = 'Faculty details'
	initial_order = [["first_name", "asc"]]
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{'name': 'first_name', 'visible': True,'searchable': True,'orderable': True,'title': 'Name',},
		{
			'name': 'Short',
			'foreign_field': 'faculty_details__short',
			'visible': True,
			'searchable': True,
			'placeholder':'short'
		}, # short showing
		{
			'name': 'Designation',
			'foreign_field': 'faculty_details__Designation_id__designation',
			'visible': True,
			'searchable': True,
			'placeholder':'desig..'
		}, # designation showing
		{'name': 'email', 'visible': True,'searchable': True,'title': 'Email', },
		# {
		# 	'name': 'Load',
		# 	'visible': True,
		# 	'searchable': False,
		# 	'orderable':False,
		# }, # load showing
		{'name': 'Feedback', 'visible': True,'searchable': False, 'orderable': False},
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete_faculty',
			'visible': True,
			'searchable': False,
			'orderable': False,
			'title':"Delete",
		}, # delete field
		### search fields ###
		{			
			'name':'Department',
			'foreign_field': 'faculty_details__Department_id__name',
			'visible': False,
			'searchable':True,
		}, # department not showing

		{'name': 'last_name', 'visible': False,'searchable': True},
	]

	def get_initial_queryset(self, request=None):
		if not request.user.is_authenticated:
			raise PermissionDenied
		queryset = self.model.objects.filter(faculty_details__pk__isnull=False)
		# queryset = self.model.objects.all()
		return queryset

	def render_row_details(self, pk, request=None):
		obj = self.model.objects.get(pk=pk)
		# fields = [f for f in self.model._meta.get_fields() if f.concrete]
		faculty_details = obj.faculty_details
		sub_events = list(Subject_event.objects.active().filter(Faculty_id=faculty_details).values_list('Subject_id__name','Subject_id__Semester_id__short'))
		fields = {
			"Load":Faculty_load.objects.get(Faculty_id=faculty_details).total_load,
			'Department':faculty_details.Department_id,
			"Shift":faculty_details.Shift_id,
		}

		html = '<table class="row-details">'
		for key in fields:
		    html += '<tr><td class="fw-bold">%s</td><td class="fw-bold">%s</td></tr>' % (key, fields[key])
		html += '<tr><td class="fw-bold">Subject Events</td><td class="fw-bold"><ul>'
		for event in sub_events:
			html += '<li stlye="font-weight:600">%s (%s)</li>' % (event[0],event[1])
		html+='</ul></td></tr>'
		html += '</table>'
		return html
	
	def get_show_column_filters(self, request):
		return None

	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['first_name'] = f'<div class="gixi gixi-md float-start" data-gixiseed="%s_%s"></div>'%(obj,obj.pk) + str(obj)
		row['Edit'] = '''<td class="border-0">
							<i class="fas fa-edit" onclick="faculty_edit_called(%s)"></i>
						</td>''' % (
			obj.id
		)
		# row["Load"] = Faculty_load.objects.get(Faculty_id=obj.faculty_details).total_load
		row['Feedback'] = ''' <a href="%s"><i class="fas fa-chart-line" style="font-size:25px"></i></a>'''%(reverse('faculty_feedback',args=[obj.pk]))
		row['Delete_faculty'] ='''<div class="form-check" onclick="checkSelected('del1')">
							<input class="form-check-input del1_input" type="checkbox"
							name="del1" value="%s" input_name="%s">
						</div>''' % (
						obj.pk,str(obj)
					)
		
		
		return

def faculty_feedback(request,Faculty_id = None):
	return render(request,"admin/user_dash/faculty_feedback.html")

