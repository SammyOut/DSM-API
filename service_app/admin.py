from django.contrib import admin

from . import models


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(models.ServiceModel, ServiceModelAdmin)
