from django.http import JsonResponse
import json

from .forms import update_user_name
import login_V2.models as login_V2

def update_student(request):
	if request.method == 'POST':
		print(request.POST)		

def update_faculty(request):
	if request.method == 'POST':
		print(request.POST)

def faculty_edit_called(request):
	if request.method == 'POST':
		pk = json.loads(request.body)
		user = login_V2.CustomUser.objects.get(pk=pk)
		faculty_details = user.faculty_details
		# json_user = serializers.serialize('json', user)
		update_data = {
			'first_name':user.first_name,
			'last_name':user.last_name,
			'email':user.email,
			
		}
		print(update_data)
	return JsonResponse(update_data)

def student_edit_called(request):
	if request.method == 'POST':
		pk = json.loads(request.body)
		user = login_V2.CustomUser.objects.get(pk=pk)
		# json_user = serializers.serialize('json', user)
		update_data = {
			'first_name':user.first_name,
			'last_name':user.last_name,
			'email':user.email
		}
		print(update_data)
	return JsonResponse(update_data)
