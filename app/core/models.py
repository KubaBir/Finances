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
        'MonthlyReport', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.debtor_name}, {self.transaction_amount}"

    @property
    def month_year(self):
        return f"{self.value_date.month:02d}" + '-' + str(self.value_date.year)

    def save(self, *args, **kwargs):
        date = datetime.date(self.value_date.year, self.value_date.month, 1)
        report, created = MonthlyReport.objects.get_or_create(
            user=self.user,
            date=date,
        )
        self.report = report

        self.set_category()

        if self.transaction_amount > 0 and not self.value:
            self.value = 'IN'
        super().save(*args, **kwargs)

    def set_category(self):
        if self.transaction_amount > 0:
            return
        category_list = {
            'Groceries': [
                'ZABKA', 'ZAPPKA', 'CARREFOUR', 'LIDL', 'VEMAT', 'ORLEN', 'CHATA', 'KIOSK'
            ],
            'Food': [
                'MC DON', 'KFC', 'MCDONALDS', 'BAR', 'EATS', 'PYSZNE', 'GLODNY', 'PIZZA', 'SALAD', 'KIM CHI',
                'MAKARONSKI', 'STODOLA',
            ],
            'Travel': [
                'JAKDOJADE', 'BILKOM', 'LIM', 'DOTT', 'TRIP', 'BOLT', 'INTERCITY', 'URBANCARD'
            ],
            'Clothing': [
                'ZARA', 'ASOS', 'ZALANDO'
            ]}
        for category, names in category_list.items():
            for name in names:
                if name in self.debtor_name:
                    self.category = category
                    return


class MonthlyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Day set to always be 01
    date = models.DateField()

    total_spendings = models.FloatField(default=0, null=True, blank=True)
    total_income = models.FloatField(default=0, null=True, blank=True)
    number_of_transactions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date.strftime('%B %Y')}"

    @property
    def previous(self):
        previous = MonthlyReport.objects.filter(
            date__lt=self.date).order_by('date').first()
        return previous
