from django.contrib import admin
from wl import models
from django.contrib.auth import get_user_model

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('userId', 'deviceId', 'sex', 'birthday', 'pk')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'user')

admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(models.Location)
admin.site.register(models.Booeonglee)
admin.site.register(models.HouseOfBooeonglee)
