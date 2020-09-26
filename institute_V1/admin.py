from django.contrib import admin
from . import models

admin.site.register(models.Institute)
admin.site.register(models.Department)
admin.site.register(models.Branch)
admin.site.register(models.Shift)
admin.site.register(models.Slots)
admin.site.register(models.Semester)
admin.site.register(models.Division)
admin.site.register(models.Batch)