from django.contrib import admin
from .models import event_class,timings
# Register your models here.

admin.site.register(event_class)
admin.site.register(timings)
