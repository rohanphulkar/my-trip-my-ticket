# Generated by Django 4.2.6 on 2023-11-08 07:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_remove_car_ac_remove_car_bags'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bus_images/'),
        ),
        migrations.AddField(
            model_name='bus',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='BusImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='bus_images/')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.bus')),
            ],
        ),
    ]
