# Generated by Django 4.2.7 on 2024-09-24 13:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_applicant_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 24, 13, 21, 55, 864575, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
