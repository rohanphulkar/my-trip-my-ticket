# Generated by Django 4.2.4 on 2023-08-18 04:20

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_rename_rent_hotel_price_car_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='0123456789', length=22, max_length=22, prefix='', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
