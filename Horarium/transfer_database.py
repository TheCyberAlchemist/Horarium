import django.apps
from django.db import IntegrityError
# al = django.apps.apps.get_models(include_auto_created=True)
# temp = al.copy()
from institute_V1.models import *
from subject_V1.models import *
from faculty_V1.models import *
from Table_V2.models import *
from student_V1.models import *
from admin_V1.models import *
from login_V2.models import *
from django.contrib.auth.models import *
import django.contrib as dj
al = [
	dj.contenttypes.models.ContentType,dj.auth.models.Group,dj.auth.models.Permission,Group,Permission,CustomUser,dj.admin.models.LogEntry,dj.sessions.models.Session,Institute,Department,Resource,Branch,WEF,Semester,Shift,Days,Working_days,Timings,Division,Slots,Subject_details,Batch,Faculty_designation,Faculty_details,Feedback_type,Faculty_load,Can_teach,Not_available,Subject_event,Admin_details,Student_details,Student_logs,AuditEntry,Feedback,Event,User_notes
]
temp = al.copy()
def batch_migrate(model):
	# remove data from destination db before copying
	# to avoid primary key conflicts or mismatches
	if model.objects.using('horarium').exists():
		model.objects.using('horarium').all().delete()

	# get data form the source database
	items = model.objects.all()

	# process in chunks, to handle models with lots of data
	start = 0
	count = items.count()
	for i in range(start, count, 1000):
		chunk_items = items[i:i+1000]
		model.objects.using('horarium').bulk_create(chunk_items)

	# many-to-many fields are NOT handled by bulk create; check for
	# them and use the existing implicit through models to copy them
	for m2mfield in model._meta.many_to_many:
		m2m_model = getattr(model, m2mfield.name).through
		batch_migrate(m2m_model)

from time import sleep
from rich.console import Console
console = Console()
def migrate_models(models):
	all_models = models.copy()
	with console.status("[bold green]Working on tasks...") as status:
		last_size = -1
		dict1 = {}
		while all_models:
			model = all_models.pop(0)
			try:
				batch_migrate(model)
				# print(".",end="")
				console.log(f"{model.__name__}"+" [bold green]complete ✅")
			except IntegrityError as e:
				console.log(f"{model.__name__} "+"[bold red]failed ❌")
				all_models.append(model)
				if last_size == len(all_models):
					print(dict1)
					if not dict1.get(model.__name__):
						dict1[model.__name__] = len(all_models)
					else:
						if dict1.get(model.__name__) == len(all_models):
							console.log(f"[bold blue]Infinite Condition reached at :: {model.__name__}❌❌")
							console.log(all_models)
							break
				last_size = len(all_models)

def empty_all_tables(models):
	all_models = models.copy()
	with console.status("[bold red]Deleting Models ...") as status:
		while all_models:
			model = all_models.pop(0)
			try:
				model.objects.using('horarium').all().delete()
				console.log(f"{model.__name__}"+" [bold red]Deleted ✅")
			except Exception as e:
				all_models.append(model)
				console.log(f"{model.__name__}"+" [bold green]Failed ❌")