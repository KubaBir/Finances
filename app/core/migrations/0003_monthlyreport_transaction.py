# Generated by Django 4.1.7 on 2023-02-24 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_user_id_user_nordigen_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_year', models.CharField(max_length=8)),
                ('total_spendings', models.FloatField(blank=True, default=0, null=True)),
                ('total_income', models.FloatField(blank=True, default=0, null=True)),
                ('number_of_transactions', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateField()),
                ('value_date', models.DateField()),
                ('transaction_amount', models.FloatField()),
                ('debtor_name', models.TextField()),
                ('info', models.TextField(default='')),
                ('category', models.CharField(choices=[('Groceries', 'Groceries'), ('Food', 'Food'), ('Travel', 'Travel'), ('Clothing', 'Clothing'), ('Other', 'Other')], default='Other', max_length=20)),
                ('value', models.CharField(choices=[('SP', 'Spendings'), ('IN', 'Income'), ('RE', 'Returned')], default='SP', max_length=2)),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.monthlyreport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
