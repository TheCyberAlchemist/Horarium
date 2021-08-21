from django.contrib import admin
from .models import *
from login_V2.admin import Show_unique_users
# Register your models here.

admin.site.register(Student_details)
admin.site.register(User_notes)

@admin.register(Student_logs)
class AuditEntryAdmin(admin.ModelAdmin):
	search_fields=('user_id__first_name','user_id__last_name')
	list_display = ['user_id','Division_id','ip']
	list_filter = ["timestamp",Show_unique_users]
	readonly_fields = ('timestamp',)
