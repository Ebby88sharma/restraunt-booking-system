from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Table

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Table)