# Generated by Django 4.1.7 on 2023-02-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_user_id_user_nordigen_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateField()),
                ('value_date', models.DateField()),
                ('transaction_amount', models.FloatField()),
                ('debtor_name', models.TextField()),
                ('info', models.TextField(default='')),
            ],
        ),
    ]