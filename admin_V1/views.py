from django.shortcuts import render
from django.http import Http404
from institute_V1.models import Institute,Department,Branch,Semester,Division,Batch
from login_V2.decorators import allowed_users

def return_context(request):
	institute = request.user.admin_details.Institute_id #.values_list('name', flat=True)
	departments = Department.objects.filter(Institute_id=institute.id)

	courses = {}
	for department in departments: # for all the departments in the institute
		temp = Branch.objects.filter(Department_id=department.id)	# filter all the courses in the same department
		if temp:	# if temp is not null
			courses[department.id] = temp 	# make a key having department id
											# and value having all the courses related to it

	sems = {}
	for key,values in courses.items():	# for all the key(department) and values(courses)
		for value in values:			# for all the coure in courses
			temp = Semester.objects.filter(Branch_id=value.id)	# find all the sems related to the course
			if temp:	# if temp is not null
				sems[value.id] = temp		# make a key having course id
											# and value having all the sems related to it

	divs = {}
	for key,values in sems.items():	# for all the key(course) and values(sems)
		for value in values:			# for all the sem in sems
			temp = Division.objects.filter(Semester_id=value.id)	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				divs[value.id] = temp		# make a key having sem id
											# and value having all the divs related to it

	batches = {}
	for key,values in divs.items():	# for all the key(sem) and values(divs)
		for value in values:			# for all the div in divss
			temp = Batch.objects.filter(Division_id=value.id)	# find all the Divs related to the Sem
			if temp:	# if temp is not null
				batches[value.id] = temp		# make a key having div id
												# and value having all the batches related to it

	context = {
		'institute':institute,
		'departments':departments,
		'courses':courses,
		'sems':sems,
		'divs':divs,
		'batches':batches,
	}
	return context

@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
	context = return_context(request)
	return render(request,'admin/homepage/home.html',context)


def navtree(request):	
	context = return_context(request)
	return render(request,"admin/navtree.html",context)


def show_branch(request,Department_id):
	institute = request.user.admin_details.Institute_id
	context = return_context(request)
	if institute == Department.objects.get(id = Department_id).Institute_id:
		courses = Branch.objects.filter(Department_id=Department_id)
		# context = {
		# 	'courses':courses,
		# 	'department': Department.objects.get(id = Department_id)
		# }
		context['my_courses'] = courses
		context['my_department']= Department.objects.get(id = Department_id)
		return render(request,"admin/details/show_branch.html",context)
	else:
		raise Http404

