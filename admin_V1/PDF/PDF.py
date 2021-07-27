from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from Table_V2.models import *

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

def export_pdf(request):
	path_to_admin_pdf = path.join(settings.BASE_DIR,"admin_V1","PDF")
	config = pdfkit.configuration(wkhtmltopdf=path.join(path_to_admin_pdf,"wkhtmltopdf","bin","wkhtmltopdf.exe"))
	html_string = render_to_string("try/html2pdf/time_table_sample.html",{"asd":"data"})
	options = {
	'margin-top': '0cm',
	'margin-right': '0cm',
	'margin-bottom': '0cm',
	'margin-left': '0cm',
	'encoding': "UTF-8",
	'custom-header' : [
		('Accept-Encoding', 'gzip')
	],
	'no-outline': None
	}
	# print(settings.STATIC_ROOT)
	temp_file_path = path.join(path_to_admin_pdf,'temp.pdf')
	css = [path.join(settings.STATIC_ROOT,"Bootstrap","bootstrap.min.css")]
	# a = pdfkit.from_string(html_string,False,configuration=config,css=css)
	a = pdfkit.from_string(html_string,False,configuration=config,css=css,options=options)
	print(type(a))	

	response = HttpResponse(a,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=asd.pdf'
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