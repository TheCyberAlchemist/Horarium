from django.contrib import admin
from .models import Faculty_designation,Faculty_details,Faculty_load,Can_teach
# Register your models here.

admin.site.register(Faculty_designation)
admin.site.register(Faculty_details)
admin.site.register(Faculty_load)
admin.site.register(Can_teach)