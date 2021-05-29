from django.apps import AppConfig
import sys

# print("feasd")
class AdminV1Config(AppConfig):
	name = 'admin_V1'
	def ready(self):
		if "runserver" in sys.argv:
			######## for scheduling the task of updating WEFs ########
			from apscheduler.schedulers.background import BackgroundScheduler
			from institute_V1.models import WEF
			from faculty_V1.models import Feedback_type
			import datetime

			WEF.update_all_WEF()
			Feedback_type.update_all_feedback_types()
			scheduler = BackgroundScheduler()
			scheduler.add_job(WEF.update_all_WEF, 'cron', hour=1, minute=0, second=0)
			scheduler.add_job(Feedback_type.update_all_feedback_types, 'cron', hour=1, minute=0, second=0)
			scheduler.start()
			###########################################################
