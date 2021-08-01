from django.contrib import admin
from .models import Student_details,Student_logs
from login_V2.admin import Show_unique_users
# Register your models here.

admin.site.register(Student_details)


@admin.register(Student_logs)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['user_id','Division_id','ip']
    list_filter = ["timestamp",Show_unique_users]
    readonly_fields = ('timestamp',)
