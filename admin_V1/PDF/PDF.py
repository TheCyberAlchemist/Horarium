from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from Table_V2.models import *
from institute_V1.models import *

#region //////////////////// view_functions //////////////////
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 
from pprint import pprint

class GeneratePdf(View):
	template = 'try/html2pdf/time_table_sample.html'
	def get_events_by_batch(self,Division_id,prac_batch_list,lect_batch_list):
		all_division_events = Event.objects.active().filter(Division_id=Division_id)
		my_events = all_division_events.filter(Q(Batch_id=None) | Q(Batch_id__in = prac_batch_list) | Q(Batch_id__in =lect_batch_list))
		print(my_events.count(),all_division_events.count())
		
	def post(self,request,*args,**kwargs):
		Division_id = self.kwargs['Division_id']
		print(all_division_events)
		pdf = render_to_pdf(self.template,{"asd":"data","print":True})
		# rendering the template
		# pprint(list(all_division_events))

		return HttpResponse(pdf, content_type='application/pdf')

	def get(self, request, *args, **kwargs):
		#getting the template
		Division_id = self.kwargs['Division_id']

		lect_batch_list=request.GET.getlist("lect_batch")
		prac_batch_list=request.GET.getlist("prac_batch")
		self.get_events_by_batch(Division_id,prac_batch_list,lect_batch_list)
		
		return render(request,self.template,{"asd":"data"})
		# return HttpResponse(pdf, content_type='application/pdf')

from admin_V1.views import return_context
def select_batch_for_pdf(request,Division_id):
	context = return_context(request)
	batch_list = Batch.objects.all().filter(Division_id_id=Division_id)
	context['my_prac_batches'] = batch_list.filter(batch_for="prac")
	context['my_lect_batches'] = batch_list.filter(batch_for="lect")
	post_result = {
		'lect_batch': ['53', '55'],
		'prac_batch': ['59', '60']
	}
	
	# if request.method == 'POST':
	# 	print(request.POST)

	return render(request,"admin/create_table/select_batch.html",context)

#endregion

#region //////////////////// weasy_print //////////////////
from django.template.loader import render_to_string
# from weasyprint import HTML
import pdfkit
import tempfile
from os import path,remove
from django.conf import settings
def lcm(x, y):
	# choose the greater number
	x = 1 if not x else x
	y = 1 if not y else y
	greater = max(x,y)
	while(True):
		if greater % x == 0 and greater % y == 0:
			ans = greater
			break
		greater += 1
	return ans

def table_template(request,Division_id):
	template = "admin/print_table/table_template.html"
	Division_id = Division.objects.get(pk=Division_id)
	my_shift = Division_id.Shift_id

	# lect_batch_list = ["58","59","60"]
	# prac_batch_list = ['53', '55',"57"]

	lect_batch_list=request.GET.getlist("lect_batch")
	prac_batch_list=request.GET.getlist("prac_batch")

	prac_batches = Batch.objects.all().filter(pk__in=prac_batch_list)
	lect_batches = Batch.objects.all().filter(pk__in=lect_batch_list)

	all_division_events = Event.objects.all().filter(Division_id=Division_id)
	my_events = all_division_events.filter(Q(Batch_id=None) | Q(Batch_id__in = prac_batch_list) | Q(Batch_id__in =lect_batch_list))

	lect_batch_count,prac_batch_count = len(lect_batch_list),len(prac_batch_list)
	unit_col = lcm(lect_batch_count,prac_batch_count)
	lect_batch_col = unit_col/lect_batch_count if lect_batch_count else unit_col
	prac_batch_col = unit_col/prac_batch_count if prac_batch_count else unit_col
	context = {
		'days' : Working_days.objects.filter(Shift_id=my_shift),
		'events' : my_events,
		'timings' : Timings.objects.filter(Shift_id = my_shift),
		"prac_batches": prac_batches,
		"lect_batches": lect_batches,
		'unit_col': unit_col,
		"lect_batch_col": lect_batch_col,
		"prac_batch_col": prac_batch_col,
	}
	if request.method == "POST":	# if print is called
		context['print'] = True
		prac_str = ','.join([str(batch.name) for batch in prac_batches])
		lect_str = ','.join([str(batch.name) for batch in lect_batches])
		return export_pdf(template,f"{Division_id.name} ({prac_str}) ({lect_str})",context)
	return render(request,template,context)

def export_pdf(template_name,file_name,context):
	path_to_admin_pdf = path.join(settings.BASE_DIR,"admin_V1","PDF")
	config = pdfkit.configuration(wkhtmltopdf=path.join(path_to_admin_pdf,"wkhtmltopdf","bin","wkhtmltopdf.exe"))
	html_string = render_to_string(template_name,context)
	
	temp_file_path = path.join(path_to_admin_pdf,'temp.pdf')
	css = [path.join(settings.STATIC_ROOT,"Bootstrap","bootstrap.min.css")]
	pdf_binary_object = pdfkit.from_string(html_string,False,configuration=config,css=css)

	response = HttpResponse(pdf_binary_object,content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename={file_name}.pdf'
	response['Content-Transfer-Encoding'] = "binary"
	
	# with tempfile.NamedTemporaryFile(delete=True) as output:
	# 	output.write(a)
	# 	output.flush()
	# 	o = open(output.name,'rb')
	# 	response.write(o.read())
	# remove(temp_file_path)
	return response

#endregion
# print(export_pdf())
# in template we could keep the download buttton in {% if print %}
# this could be donw so that when we initially load the page as preview we keem print = faculty_settings
# when we are converting the page to pdf we send print = true hence only the table will be printed