from django.contrib import admin
from wl import models
from django.contrib.auth import get_user_model

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('deviceId', 'userId', 'sex', 'birthday',)

admin.site.register(get_user_model(), MyUserAdmin)

