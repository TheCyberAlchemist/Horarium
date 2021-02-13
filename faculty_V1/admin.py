from django.contrib import admin
from .models import Faculty_designation,Faculty_details,Faculty_load,Can_teach,Not_available,Chart
# Register your models here.

admin.site.register(Faculty_designation)
admin.site.register(Faculty_details)
admin.site.register(Faculty_load)
admin.site.register(Can_teach)
admin.site.register(Not_available)
admin.site.register(Chart)
