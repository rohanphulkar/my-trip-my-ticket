# Generated by Django 4.2.6 on 2023-10-27 06:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_citytour_citytourimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='fuel_type',
        ),
        migrations.RemoveField(
            model_name='car',
            name='transmission_type',
        ),
        migrations.AlterField(
            model_name='car',
            name='available_till',
            field=models.DateField(default=datetime.date(2023, 10, 27)),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='available_from',
            field=models.DateField(default=datetime.date(2023, 10, 27)),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='available_to',
            field=models.DateField(default=datetime.date(2023, 10, 27)),
        ),
        migrations.AlterField(
            model_name='package',
            name='departure',
            field=models.DateField(default=datetime.date(2023, 10, 27)),
        ),
    ]