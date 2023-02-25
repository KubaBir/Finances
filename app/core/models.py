import datetime

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    booking_date = models.DateField()
    value_date = models.DateField()
    transaction_amount = models.FloatField()
    debtor_name = models.TextField()
    info = models.TextField(default="")

    CATEGORY_CHOICES = [
        ('Groceries', 'Groceries'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Clothing', 'Clothing'),
        ('Other', 'Other'),
    ]
    category = models.CharField(
        choices=CATEGORY_CHOICES, default='Other', max_length=20)
    VALUE_CHOICES = [
        ('SP', 'Spendings'),
        ('IN', 'Income'),
        ('RE', 'Returned'),
    ]
    value = models.CharField(choices=VALUE_CHOICES, default='SP', max_length=2)

    report = models.ForeignKey(
        'MonthlyReport', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.debtor_name}, {self.transaction_amount}"

    @property
    def month_year(self):
        return f"{self.value_date.month:02d}" + '-' + str(self.value_date.year)

    def save(self, *args, **kwargs):
        report, created = MonthlyReport.objects.get_or_create(
            month_year=self.month_year, user=self.user, year=self.value_date.year)
        self.report = report
        if self.transaction_amount > 0:
            self.value = 'IN'
        super().save(*args, **kwargs)


class MonthlyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Format "MM-YYYY"
    month_year = models.CharField(max_length=8)
    year = models.IntegerField()

    total_spendings = models.FloatField(default=0, null=True, blank=True)
    total_income = models.FloatField(default=0, null=True, blank=True)
    number_of_transactions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.month_year}"
