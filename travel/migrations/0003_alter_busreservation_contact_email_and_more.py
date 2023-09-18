# Generated by Django 4.2.5 on 2023-09-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_dubaiactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busreservation',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='busreservation',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='carreservation',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='carreservation',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='flightreservation',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='flightreservation',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='hotelreservation',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='hotelreservation',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='packagereservation',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='packagereservation',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
