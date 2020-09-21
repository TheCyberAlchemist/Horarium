from django.shortcuts import render,redirect
################################################
from django.http import HttpResponse
from institute_V1.models import Institute,Department,Course,Semester
################################################


def navtree(request):
	institute_pk = 1
	institute = Institute.objects.filter(pk=institute_pk)#.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute_pk)
	courses = {}
	for department in departments:
		c = Course.objects.filter(Department_id=department.id)
		courses[department.short] = c
	sems = {}
	print(courses)
	for key,values in courses.items():
		for value in values:
			c = Semester.objects.filter(Course_id=value.id)
			if c:
				sems[value.short] = c
	print(sems)
	context = {
		'institute':institute[0],
		'departments':departments,
		'courses':courses,
		'sems':sems,
	}
	return render(request,"login_V2/admin/home.html",context)

def dev(req):
	return "hii"
