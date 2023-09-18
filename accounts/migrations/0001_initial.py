# Generated by Django 4.2.5 on 2023-09-18 04:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('merital_status', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married')], max_length=20, null=True)),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='birthday')),
                ('address', models.TextField(blank=True, null=True)),
                ('pin', models.CharField(blank=True, max_length=6, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('provider', models.CharField(blank=True, choices=[('email', 'Email'), ('google', 'Google'), ('phone', 'Phone')], max_length=100)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
                ('pwd_reset_token', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]