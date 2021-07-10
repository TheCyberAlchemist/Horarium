from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import numpy as np

from login_V2.models import CustomUser
from institute_V1.models import *
from django.db.models import Q
from admin_V1.forms import add_user
from student_V1.forms import add_student_details
from faculty_V1.forms import faculty_details_csv,faculty_load
from faculty_V1.models import *
#region //////////////////// view_functions //////////////////
from django.shortcuts import render,redirect

def csv_view_func(request):
	# return render(request,"try/upload_csv.html")
	return render(request,'admin/details/csv_upload.html')

def csv_try_view_func(request):
	return render(request,"try/upload_csv.html")
	# return render(request,'admin/details/csv_upload.html')

#endregion


table_classes = ["table","mb-0","text-center"] # add classes for table tag here
NULL_CELL_STR = "------"
# if to_json for rows doesn't work make it to_dict with changing NAN to ""
# clean functions
def clear_empty_rows(df):
	df = df.dropna(how='all')
	return df

def clear_duplicate_rows(df):
	df = df.drop_duplicates()
	return df

#region //////////////////// Student Check Functions //////////////////
def check_student_headers(df):
	error_json = {}
	header_set = {
		'E-mail','Password',
		'First name','Last name','Roll_no',
		'Department','Semester',"Branch",'Division',
		'Practical Batch','Lecture Batch'
	}
	# print(header_set,set(df.head(0)))
	if header_set != set(df.head(0)):
		# if the header is not as needed
		error_json['error_name'] = "Proper headers not Found!"
		error_json['error_body'] = ['The header of the file need to follow the format as mentioned :',
									'E-mail','Password','First name','Last name','Roll_no','Department','Semester','Branch','Division','Practical Batch','Lecture Batch']

	return error_json

def check_student_details(df):
	' check student details such as Roll_no, Department, Semester, Branch, Division for empty cell '
	error_json = {}
	user_info_headers = ["Roll_no","Department","Semester","Branch","Division"]
	a = df.loc[pd.isna(df["Roll_no"]) | pd.isna(df["Department"]) | pd.isna(df["Semester"]) | pd.isna(df["Branch"]) | pd.isna(df["Division"]) , :]
	if not a.empty:
		error_json["error_name"] = "Student details missing!"
		error_json["error_body"] = [' The mentioned fields must be filled in order to save the student :',
									'(Roll_no,Department,Semester,Division)']
		error_json["table"] = a.to_html(classes = table_classes,na_rep=NULL_CELL_STR)
		# print(a)
		return error_json
	return False

def validate_and_make_student_details(df,my_institute):
	'''validate the student_info (i.e. Department, Branch, Division, Batch ) and returns details 
		and error_json details have the following fields (roll_no,Institute,Division,User-id,prac_batch,lect_batch)
		from database models
	'''
	error_json = {}
	error_json["error_name"] = "Student Detials invalid! "
	error_json["error_body"] = []
	row_list = []
	prac_is_null = pd.isna(df['Practical Batch'])
	lect_is_null = pd.isna(df['Lecture Batch'])
	error_df = pd.DataFrame(data=None, columns=df.columns)
	
	for i,row in df.iterrows():
		# need institute division batches
		my_department = Department.objects.all().filter(Q(short = row['Department']) |Q(name = row['Department']),Institute_id=my_institute).first()
		my_branch = my_department.branch_set.filter(Q(short = row['Branch']) | Q(name = row['Branch'])).first() if my_department else None
		my_semester = my_branch.semester_set.filter(short = row['Semester']).first() if my_branch else None
		my_division = my_semester.division_set.filter(name= row['Division']).first() if my_semester else None
		my_prac_batch = my_division.batch_set.filter(name = row['Practical Batch'],batch_for="prac").first() if my_division else None
		my_lect_batch = my_division.batch_set.filter(name = row['Lecture Batch'],batch_for="lect").first() if my_division else None

		dict1 = {}
		dict1.update({
			"roll_no" : row['Roll_no'],
			"Institute_id" : my_institute,
			"Division_id" : my_division,
		})
		# check if none
		# print(dict1,my_division)
		if not all(dict1.values()):
			# if any of the dict1 is empty

			# print(dict1.values())
			if not my_department:
				# if institute is empty meaning department is None
				error_json["error_body"].append("No Department named %s" % (row["Department"]))
				error_df = error_df.append(row)
			elif not my_division:
				if not my_branch:
					# if branch is not found
					error_json["error_body"].append("No Branch named %s in %s" % (row["Branch"],row["Department"]))
				elif not my_semester:
					error_json["error_body"].append("No Semester named %s in %s" % (row['Semester'],row["Branch"]))
				elif not my_division:
					error_json["error_body"].append("No Division named %s in %s" % (row["Division"],row['Semester']))				
				error_df = error_df.append(row)
		else:
			user = CustomUser(email=row['E-mail'],first_name=row['First name'],last_name=row['Last name'],password=row['Password'])
			# print(type(user))
			dict1.update({
				"User_id" : user,
				"prac_batch" : my_prac_batch,
				"lect_batch": my_lect_batch
			})
			# print(my_prac_batch)
			if not prac_is_null[i] and not my_prac_batch:
				# if filled by default and still empty
				error_json["error_body"].append("No Practical Batch named %s in %s" % (row["Practical Batch"],row['Division']))
				error_df = error_df.append(row)
			if not lect_is_null[i] and not my_lect_batch:
				# if filled by default and still empty
				error_json["error_body"].append("No Lecture Batch named %s in %s" % (row["Lecture Batch"],row['Division']))
				error_df = error_df.append(row)
				
		row_list.append(dict1)
	
	student_details = pd.DataFrame(row_list)
	if not error_df.empty:
		error_json["error_body"] = list(dict.fromkeys(error_json["error_body"]))
		error_df = error_df.drop_duplicates()
		error_json["table"] = error_df.to_html(classes = table_classes,na_rep=NULL_CELL_STR)
		return student_details,error_json
	
	return student_details,False

#endregion

#region //////////////////// Faculty Check Functions //////////////////
def check_faculty_headers(df):
	''' check for faculty headers ('E-mail','Password','First name','Last name','Short'
		,'Department','Shift','Designation','Load','Can Teach')
	'''
	error_json = {}
	# 
	header_set = {
		'E-mail','Password',
		'First name','Last name','Short',
		'Department','Shift',
		'Designation','Load','Can Teach'
	}
	# print(header_set,set(df.head(0)))
	if header_set != set(df.head(0)):
		# if the header is not as needed
		error_json['error_name'] = "Proper headers not Found!"
		error_json['error_body'] = ['The header of the file need to follow the format as mentioned :',
									'E-mail','Password','First name','Last name','Short','Department','Shift','Designation','Load','Can Teach']

	return error_json

def check_faculty_details(df):
	' check faculty details such as Short,Department,Shift,Designation,Load for empty cell '
	error_json = {}
	a = df.loc[pd.isna(df["Short"]) | pd.isna(df["Department"]) | pd.isna(df["Shift"]) | 
				pd.isna(df["Designation"]) | pd.isna(df["Load"]) 
			,:]
	if not a.empty:
		error_json["error_name"] = "Faculty details missing! "
		error_json["error_body"] = [' The mentioned fields must be filled in order to save the student :',
									'(Short,Department,Shift,Designation,Load)']
		error_json["table"] = a.to_html(classes = table_classes,na_rep=NULL_CELL_STR)
		# print(a)
		return error_json
	return False

def validate_and_make_faculty_details(df,my_institute):
	'''check if the Faculty details for valid '''
	'''
		validate the Faculty_details (i.e. Department,Shift,Designation,Can Teach ) and returns details 
		and error_json details have the following fields (Institute,Division,Batches)
		from database models
	'''
	error_json = {}
	error_json["error_name"] = " Faculty Detials invalid! "
	error_json["error_body"] = []
	row_list = []
	# prac_is_null = pd.isna(df['Practical Batch'])
	# lect_is_null = pd.isna(df['Lecture Batch'])
	error_df = pd.DataFrame(data=None, columns=df.columns)
	
	for i,row in df.iterrows():
		my_department = Department.objects.all().filter(Q(short = row['Department']) | Q(name = row['Department']),Institute_id=my_institute).first()
		my_shift = Shift.objects.all().filter(name = row['Shift'],Department_id=my_department).first() if my_department else None
		my_designation,_ = Faculty_designation.objects.get_or_create(Institute_id=my_institute,designation=row['Designation'])
		all_subjects = Subject_details.objects.all().filter(Semester_id__Branch_id__Department_id = my_department)
		my_subjects = []
		for i in row['Can Teach'].split(","):
			this_subj = all_subjects.filter(Q(short = i) | Q(name = i))
			if this.subj.count() > 1: # if more then one subject of same name in department
				error_json["error_body"].append("More then one subjects named %s in %s.Please insert the subject manually in user Dashbord." % (i,row['Department']))
				error_df = error_df.append(row)
			else:
				this_subj = this_subj.first()
				if this_subj:
					my_subjects.append(this_subj)
				else:	# no subject found
					error_json["error_body"].append("No Subject named <b> %s</b> in %s" % (i,my_department))
					error_df = error_df.append(row)

		dict1 = {}
		dict1.update({
			"short" : row['Short'],
			'Institute_id':my_institute,
			"Department_id" : my_department,
			"Designation_id" : my_designation,
			"Shift_id" : my_shift,
		})
		# check if none
		# print(dict1,my_division)
		if not all(dict1.values()):
			# if any of the dict1 is empty
			# print(dict1.values())
			if not my_department:
				# if institute is empty meaning department is None
				error_json["error_body"].append("No Department named %s" % (row['Department']))
				error_df = error_df.append(row)
			elif not my_shift:
				error_json["error_body"].append("No Shift named %s in %s" % (row['Shift'],row['Department']))
				error_df = error_df.append(row)
		else:
			user = CustomUser(email=row['E-mail'],first_name=row['First name'],last_name=row['Last name'],password=row['Password'])
			# print(type(user))
			dict1.update({
				"User_id" : user,
				'total_load' : row['Load'],
				'my_subjects' :my_subjects,
			})	
		row_list.append(dict1)
	
	faculty_details = pd.DataFrame(row_list)
	if not error_df.empty:
		error_json["error_body"] = list(dict.fromkeys(error_json["error_body"]))
		error_df = error_df.drop_duplicates()
		error_json["table"] = error_df.to_html(classes= table_classes,na_rep=NULL_CELL_STR)
		return faculty_details,error_json
	
	return faculty_details,False
#endregion

#region //////////////////// User and email Check Functions //////////////////
def check_user_details(df):
	' check user details such as Password, E-mail, First name, Last name for empty cell '
	error_json = {}
	user_info_headers = ["Password","E-mail","First name","Last name"]
	a = df.loc[pd.isna(df["Password"]) | pd.isna(df["E-mail"]) | pd.isna(df["First name"]) | pd.isna(df["Last name"])]
	# print(df.loc[pd.isna(df["Password"]) | pd.isna(df["E-mail"]) | pd.isna(df["First name"]) | pd.isna(df["Last name"])])
	if not a.empty:
		error_json["error_name"] = "User Details is missing!"
		error_json["error_body"] = [' The mentioned fields must be filled in order to save the user ',"\t(Password,E-mail,First name,Last name)"]
		pd.options.mode.chained_assignment = None
		error_json["table"] = a.to_html(classes = table_classes,na_rep=NULL_CELL_STR)
		# print(a)
		return error_json
	return False

	# arr = np.where(df[user_info_headers].isna())[0]
	# # print(bool(arr.any()))
	# if arr.any():
	# 	error_json["error_name"] = "User info is missing (Password,E-mail,First name,Last name)"
	# 	error_json["error_body"] = ''' The mentioned fields must be filled in order to save the user '''
	# 	error_json["table"] = []
	# 	# if any rows have empty Password,E-mail,....
	# 	for i in arr:
	# 		error_json["table"].append(df.loc[i].to_frame().to_json(orient="columns"))
	# 		# a.loc[pd.isna(a["Password"]) | pd.isna(a["E-mail"]), :].to_html()
	# return error_json

def check_email_for_duplication_internal(df):
	'Checks if there is email duplication in the file '
	error_json = {}
	error_json["error_name"] = "Email duplication found in the file! "
	error_json["error_body"] = ''' Emails of the following rows have been found to be same in the file. '''
	df = df.sort_values("E-mail")
	# print(df[df.duplicated(['E-mail'],keep=False)])
	arr = df[df.duplicated(['E-mail'],keep=False)]
	if not arr.empty:
		error_json["table"] = arr.to_html(classes= table_classes,na_rep=NULL_CELL_STR)
		return error_json
	return False

def check_email_for_duplication_external(df):
	'Checks if there is same email in the file as in the database '
	error_json = {}
	same_email_users = CustomUser.objects.all().filter(email__in=df['E-mail'].tolist())	
	duplicate_list = list(same_email_users.values_list("email",flat=True))
	error_json["error_name"] = "Email duplication found in the database! "
	error_json["error_body"] = ''' Emails of the following rows have been found to be same in the database '''
	arr = df[df['E-mail'].isin(duplicate_list)]
	# print(df[df['E-mail'].isin(duplicate_list)].to_json(orient="index"))
	if not arr.empty:
		error_json["table"] = arr.to_html(classes=table_classes,na_rep=NULL_CELL_STR)
		return error_json
	return False

#endregion

#region //////////////////// Main validation functions //////////////////
import traceback
def validate_student_csv(df,request):
	'runs all the steps of validation and returns the error_json and details_df'
	error_list = []
	details = None
	app = lambda new: error_list.append(new) if new else None
	# check headers
	try:
		app(check_student_headers(df))
	except Exception as e:
		print("Something went wrong in headers function ")
		print(e)

	# check user cells 
	try:
		app(check_user_details(df))
	except Exception as e:
		print("Something went wrong in user details function ")
		print(e)
	

	# check student details cells
	try:
		app(check_student_details(df))
	except Exception as e:
		print("Something went wrong in student details function ")
		print(e)
	#region try_catch
	# check if the emails are duplicated in df 
	try:
		app(check_email_for_duplication_internal(df))
		# print("Asdasd")
	except Exception as e:
		print("Something went wrong in internal email duplication function ")
		print(e)	

	# check if the emails are duplicated in database
	try:
		app(check_email_for_duplication_external(df))
	except Exception as e:
		print("Something went wrong in external email duplication function ")
		print(e)

	# check if the Student details for valid department,branch,class,batch
	try:
		details,json = validate_and_make_student_details(df,request.user.admin_details.Institute_id)
		app(json)
	except Exception as e:
		print("Something went wrong in student details function ")
		traceback.print_exc()
		print(e)
	#endregion
	
	return error_list,details

def validate_faculty_csv(df,request):
	'runs all the steps of validation and returns the error_json and details_df'
	error_list = []
	details = None
	app = lambda new: error_list.append(new) if new else None

	# check headers
	try:
		app(check_faculty_headers(df))
	except Exception as e:
		print("Something went wrong in headers function ")
		print(e)

	# check user cells 
	try:
		app(check_user_details(df))
	except Exception as e:
		print("Something went wrong in user details function ")
		print(e)

	try:
		app(check_faculty_details(df))
	except Exception as e:
		print("Something went wrong in faculty details function ")
		print(e)
	
	# check if the emails are duplicated in df 
	try:
		app(check_email_for_duplication_internal(df))
		# print("Asdasd")
	except Exception as e:
		print("Something went wrong in internal email duplication function ")
		print(e)	

	# check if the emails are duplicated in database
	try:
		app(check_email_for_duplication_external(df))
	except Exception as e:
		print("Something went wrong in external email duplication function ")
		print(e)
	
	# check if the Faculty details for valid Department,Shift,Designation,Load,Can Teach
	try:
		details,json = validate_and_make_faculty_details(df,request.user.admin_details.Institute_id)
		app(json)
	except Exception as e:
		print("Something went wrong in faculty details function ")
		print(e)
	return error_list,details
#endregion

class csv_check_api(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request):
		error_list = []
		csv_file = request.FILES['file']

		csv_type = request.POST['csv_input']
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'THIS IS NOT A CSV FILE')
			error_list.append({"error_name":"The file must be csv"})
			return Response(context)
		df = pd.read_csv(csv_file, na_filter= True)

		# df = pd.read_csv("admin_V1\student_details.csv", na_filter= True)
		# df = pd.read_csv("admin_V1\\faculty_details.csv", na_filter= True)
		
		# clear empty rows
		df = clear_empty_rows(df)
		df = clear_duplicate_rows(df)
		
		if csv_type == "student":
			error_list,details = validate_student_csv(df,request)
			all_saved_pks = []
			if not error_list:
				for i,row in details.iterrows():
					student_form = add_student_details(row)
					if student_form.is_valid():
						user = row["User_id"]
						# user.save()
						candidate = student_form.save(commit=False)
						candidate.User_id = user
						try:
							# user.save()
							# all_saved_pks.append(user.pk)
							# candidate.save()
							# print("done safely, self destructing .. ",user.email)
							# user.delete()
							pass
						except Exception as e:
							# print("Something went wrong deleting all .. ",e)
							# print(all_saved_pks)
							# for j in all_saved_pks:
							# 	CustomUser.objects.filter(pk=j).delete()
							pass
					print(all_saved_pks)
			
		elif csv_type == "faculty":
			print("faculty csv found refining ")
			error_list,details = validate_faculty_csv(df,request)
			print(error_list)
			all_saved_pks = []
			if not error_list:
				for i,row in details.iterrows():
					faculty_form = faculty_details_csv(row)
					faculty_load_form = faculty_load(row)
					if faculty_form.is_valid() and faculty_load_form.is_valid():
						user = row["User_id"]
						# user.save()
						faculty_details = faculty_form.save(commit=False)
						faculty_details.User_id = user
						faculty_load_candidate = faculty_load_form.save(commit=False)
						faculty_load_candidate.Faculty_id = faculty_details
						try:
							user.save()
							all_saved_pks.append(user.pk)
							faculty_details.save()
							faculty_load_candidate.save()
							for subjects in row['my_subjects']:
								Can_teach.objects.create(Faculty_id=faculty_details,Subject_id=subjects)
							print("done safely, self destructing .. ",user.email)
							user.delete()
							pass
						except Exception as e:
							print("Something went wrong deleting all .. ",e)
							print(all_saved_pks)
							for j in all_saved_pks:
								CustomUser.objects.filter(pk=j).delete()
							pass
					# print(all_saved_pks)
		
		context = {"error_list": error_list}

		return Response(context)
