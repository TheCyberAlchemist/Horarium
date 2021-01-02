from django.shortcuts import render

# Create your views here.

def student_home(request):
	return render(request,"Student/student_v1.html")