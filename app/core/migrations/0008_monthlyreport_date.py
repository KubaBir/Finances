# Generated by Django 4.1.7 on 2023-02-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_transaction_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyreport',
            name='date',
            field=models.DateField(default='2023-02-01'),
            preserve_default=False,
        ),
    ]