from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import UserManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_baker = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "کد اعتبار سنجی "
        verbose_name_plural = "کد های اعتبار سنجی"

#
# class Comment(models.Model):
#     user = models.ManyToOneRel(CustomUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField(max_length=300)
#
#


