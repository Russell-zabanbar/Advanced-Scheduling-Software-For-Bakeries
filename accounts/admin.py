from django.contrib import admin
from accounts.models import CustomUser, OtpCode
from django.contrib.auth.models import Group

admin.site.register(CustomUser)
admin.site.unregister(Group)
admin.site.register(OtpCode)
