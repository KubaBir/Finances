from django.contrib import admin
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            username=username,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    nordigen_user_id = models.CharField(max_length=255, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    booking_date = models.DateField()
    value_date = models.DateField()
    transaction_amount = models.FloatField()
    debtor_name = models.TextField()
    info = models.TextField(default="")

    def __str__(self):
        return f"{self.debtor_name}, {self.transaction_amount}"
