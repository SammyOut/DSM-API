from django.contrib import admin

from . import models


class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'username', 'email')


admin.site.register(models.StudentModel, StudentModelAdmin)
