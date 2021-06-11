from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import numpy as np

from login_V2.models import CustomUser
from institute_V1.models import *
from django.db.models import Q
# from . import student_details.csv
#region //////////////////// view_functions //////////////////
from django.shortcuts import render,redirect

table_classes = [""] # add classes for table tag here

# if to_json for rows doesn't work make it to_dict with changing NAN to ""
# clean functions
def clear_empty_rows(df):
	df = df.dropna(how='all')
	return df

def clear_duplicate_rows(df):
	df = df.drop_duplicates()
	return df

# check functions
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
		error_json['error_name'] = "Headers not properly formated"
		error_json['error_body'] = '''The header of the file need to follow the format of 'E-mail','Password','First name','Last name','Roll_no','Department','Semester','Branch','Division','Practical Batch','Lecture Batch' '''

	return error_json


def check_user_details(df):
	error_json = {}
	user_info_headers = ["Password","E-mail","First name","Last name"]
	a = df.loc[pd.isna(df["Password"]) | pd.isna(df["E-mail"]) | pd.isna(df["First name"]) | pd.isna(df["Last name"]) , :]
	if not a.empty:
		error_json["error_name"] = "User info is missing (Password,E-mail,First name,Last name)"
		error_json["error_body"] = ''' The mentioned fields must be filled in order to save the user '''
		error_json["table"] = a.to_html(classes = table_classes)
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

def check_student_details(df):
	error_json = {}
	user_info_headers = ["Roll_no","Department","Semester","Branch","Division"]
	a = df.loc[pd.isna(df["Roll_no"]) | pd.isna(df["Department"]) | pd.isna(df["Semester"]) | pd.isna(df["Branch"]) | pd.isna(df["Division"]) , :]
	if not a.empty:
		error_json["error_name"] = "Student details missing (Roll_no,Department,Semester,Division)"
		error_json["error_body"] = ''' The mentioned fields must be filled in order to save the student '''
		error_json["table"] = a.to_html()
		# print(a)
		return error_json
	return False
	# print(bool(arr.any()))
	# arr = np.where(df[user_info_headers].isna())[0]
	# if arr.any():
	# 	error_json["error_name"] = "Student details missing (Roll_no,Department,Semester,Division)"
	# 	error_json["error_body"] = ''' The mentioned fields must be filled in order to save the student '''
	# 	error_json["table"] = []
	# 	# if any rows have empty Password,E-mail,....
	# 	for i in arr:
	# 		error_json["table"].append(df.loc[i].to_frame().to_json(orient="columns"))
	# return error_json

def check_email_for_duplication_internal(df):
	error_json = {}
	error_json["error_name"] = "Email duplication found in the file. "
	error_json["error_body"] = ''' Emails of the following rows have been found to be same in the file. '''
	df = df.sort_values("E-mail")
	# print(df[df.duplicated(['E-mail'],keep=False)])
	arr = df[df.duplicated(['E-mail'],keep=False)]
	if not arr.empty:
		error_json["table"] = arr.to_html(classes= table_classes)
		return error_json
	return False

def check_email_for_duplication_external(df):
	error_json = {}
	same_email_users = CustomUser.objects.all().filter(email__in=df['E-mail'].tolist())	
	duplicate_list = list(same_email_users.values_list("email",flat=True))
	error_json["error_name"] = "Email duplication found in the database. "
	error_json["error_body"] = ''' Emails of the following rows have been found to be same in the database '''
	arr = df[df['E-mail'].isin(duplicate_list)]
	# print(df[df['E-mail'].isin(duplicate_list)].to_json(orient="index"))
	if not arr.empty:
		error_json["table"] = arr.to_html(classes=table_classes)
		return error_json
	return False

def validate_and_make_student_details(df):
	error_json = {}
	error_json["error_name"] = "Student Detials invalid "
	error_json["error_body"] = []
	cache = {
	"departments":{},
	"branches":{},
	"Divisions":{},
	"Batches":{}
	}
	# COLUMN_NAMES=["index","roll_no","Institute_id","Division_id","prac_batch","lect_batch"]
	error_row_list = []
	row_list = []
	prac_is_null = pd.isna(df['Practical Batch'])
	lect_is_null = pd.isna(df['Lecture Batch'])
	error_df = pd.DataFrame()
	for i,row in df.iterrows():
		# need institute division batches
		my_department = Department.objects.all().filter(Q(short = row['Department']) |Q(name = row['Department'])).first()
		my_institute = my_department.Institute_id if my_department else None
		my_branch = my_department.branch_set.filter(Q(short = row['Branch']) | Q(name = row['Branch'])).first() if my_department else None
		my_semester = my_branch.semester_set.filter(short = row['Semester']).first() if my_branch else None
		my_division = my_semester.division_set.filter(name= row['Division']).first() if my_semester else None
		my_prac_batch = my_division.batch_set.filter(name = row['Practical Batch'],batch_for="prac").first() if my_division else None
		my_lect_batch = my_division.batch_set.filter(name = row['Lecture Batch'],batch_for="lect").first() if my_division else None

		dict1 = {}
		dict1.update({
			"index" : i,
			"roll_no" : row['Roll_no'],
			"Institute_id" : my_institute,
			"Division_id" : my_division,
		})
		# check if none
		# print(dict1,my_division)
		if not all(dict1.values()):
			# if any of the dict1 is empty
			# print("inside")
			if not my_institute:
				# if institute is empty meaning department is None
				error_json["error_body"].append("No Department named %s" % (row("Department")))
				error_df = error_df.append(row)
				# error_row_list.append(row.to_frame().to_json(orient="columns"))
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
			dict1.update({
				"prac_batch" : my_prac_batch,
				"lect_batch": my_lect_batch
			})
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
		error_json["table"] = error_df.to_html(classes= table_classes)
		return student_details,error_json
	return student_details,False


def csv_view_func(request):
	return render(request,"try/upload_csv.html")

class csv_check_api(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request):
		# csv_file = request.FILES['file']
		# if not csv_file.name.endswith('.csv'):
		# 	messages.error(request, 'THIS IS NOT A CSV FILE')
		error_list = []
		df = pd.read_csv("admin_V1\student_details.csv", na_filter= True)
		
		# clear empty rows
		df = clear_empty_rows(df)
		df = clear_duplicate_rows(df)

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
			print("Something went wrong in internal email duplication function ")
			print(e)

		# check if the Student details for valid department,branch,class,batch
		try:
			details,json = validate_and_make_student_details(df)
			app(json)
		except Exception as e:
			print("Something went wrong in  function ")
			print(e)

		print(details)
		context = {"error_list": error_list}

		return Response(context)
#endregion

