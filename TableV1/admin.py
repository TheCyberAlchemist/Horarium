from django.contrib import admin
from .models import event_class,timings,event
# Register your models here.

admin.site.register(event_class)
admin.site.register(event)
admin.site.register(timings)
