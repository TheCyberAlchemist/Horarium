from django.contrib import admin
from .models import Event

################################################

@admin.register(Event)
class Event_table(admin.ModelAdmin):
	search_fields=('Slot_id__Timing_id__start_time','Slot_id__day__Days_id__name')
	# list_display = ['user_id','Division_id','ip']
	list_filter = ["Slot_id__Timing_id__Shift_id"]
	# readonly_fields = ('timestamp',)

################################################
