# Generated by Django 4.2.6 on 2023-11-08 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_seaadventure_alter_car_available_till_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='ac',
        ),
        migrations.RemoveField(
            model_name='car',
            name='bags',
        ),
    ]
