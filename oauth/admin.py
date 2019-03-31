from django.contrib import admin
from oauth import models


class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'username', 'email')


class AppModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')


class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('app', 'student')


class AccessTokenModelAdmin(admin.ModelAdmin):
    list_display = ('app', 'student')


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class AppServiceRelModel(admin.ModelAdmin):
    list_display = ('app', 'service')


admin.site.register(models.StudentModel, StudentModelAdmin)
admin.site.register(models.AppModel, AppModelAdmin)
admin.site.register(models.RefreshTokenModel, RefreshTokenAdmin)
admin.site.register(models.AccessTokenModel, AccessTokenModelAdmin)
admin.site.register(models.ServiceModel, ServiceModelAdmin)
admin.site.register(models.AppServiceRelModel, AppServiceRelModel)
