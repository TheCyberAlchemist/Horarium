from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.template.loader import render_to_string
from django.core import serializers
from rest_framework.response import Response
import login_V2.models as login_V2
import jsonfield
import json

# https://pypi.org/project/django-ajax-datatable/#sorting-columns
class student_user_table(AjaxDatatableView):
	
	model = login_V2.CustomUser
	title = 'Permissions'
	initial_order = [["Department", "asc"]]
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': True,
		},
		{'name': 'Name', 'visible': True,'searchable': False,'orderable': False},
		{'name': 'email', 'visible': True,'searchable': True,  },
		{
			'name': 'Roll No',
			'foreign_field': 'student_details__roll_no',
			'visible': True,
			'searchable': True,
		}, # roll no showing
		{
			'name':'Department',
			'foreign_field': 'student_details__Division_id__Semester_id__Branch_id__Department_id__short',
			'visible': True,
			'searchable':True,
		}, # department showing
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':
				'Delete',
			# 'title': '''<div class="form-check" onclick="checkAll();">
			# 		<input class="form-check-input" type="checkbox" value="parent"
			# 			id="parent" name="parent">
			# 	</div>''',
			'visible': True,
			'searchable': False,
			'orderable': False
		},
		### search fields ###

		{'name': 'first_name', 'visible': False,'searchable': True},
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
		html = '<table class="row-details">'
		for key in fields:
		    html += '<tr><td>%s</td><td>%s</td></tr>' % (key, fields[key])

		html += '</table>'
		return html
	
	def get_show_column_filters(self, request):
		return None

	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['Name'] = str(obj)
		row['Edit'] = '''<td class="border-0">
							<a href = "{{url ('')}}">
								<i class="fas fa-edit"></i>
							</a>
						</td>''' % (
			# obj.id,
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