from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Faculty_designation)
admin.site.register(Faculty_details)
admin.site.register(Faculty_load)
admin.site.register(Can_teach)
admin.site.register(Not_available)
admin.site.register(Chart)
admin.site.register(Feedback_type)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ['Given_by','Faculty_id','average']
	list_filter = ["timestamp"]
	readonly_fields = ('timestamp',)
# admin.site.register(Feedback)