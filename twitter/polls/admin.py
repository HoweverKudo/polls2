from django.contrib import admin

from .models import Poll, Choice, CustumUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(CustumUser, UserAdmin)