# Generated by Django 4.2.7 on 2024-09-30 21:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_applicant_specialization_specializationapplicant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 30, 21, 15, 43, 677748, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
