from django.shortcuts import render
from .models import try_model
# Create your views here.
import base64

from django.core.files.base import ContentFile

from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponseForbidden, HttpResponse
from django.views import View
from django.conf.urls.static import static
from django.conf import settings

def try_function(request):
	if request.method == 'POST':
		# print()
		format, imgstr = request.POST['img_str'].split(';base64,') 
		ext = format.split('/')[-1] 
		data = ContentFile(base64.b64decode(imgstr))
		file_name = "%s.%s" % (request.user,ext)
		obj = try_model()
		obj.user = request.user
		obj.display_image.save(file_name, data, save=True)
		# print(data)
		# img_data = request.POST['img_str']
		# img_file = open("photo.png", "wb")
		# img_file.write(base64.b64decode(imgstr))
		# img_file.close()
	return render(request,'try/abc.html')

def open_try(request):
	return render(request,'try/asd.html')
from student_V1.models import Student_details
def DocumentDownload(request,relative_path):
	print(relative_path)
	document = get_object_or_404(Student_details, display_image=relative_path)
	print(document)
	if not request.user.is_superuser and document.User_id != request.user:
		return HttpResponseForbidden()
	absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, relative_path)
	response = FileResponse(open(absolute_path, 'rb'))
	# queryset = Document.objects.all()
	# user = request.user

	# if not user.is_superuser:
	# 	queryset = queryset.filter(
	# 		created_by=user
	# 	)

	# return queryset
	return response
