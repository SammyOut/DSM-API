from django.contrib import admin

from . import models


class AppModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')


admin.site.register(models.AppModel, AppModelAdmin)
