# Generated by Django 3.1.7 on 2021-03-22 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryInterface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('secret', models.CharField(max_length=50)),
                ('enable_monitoring', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Primary Interface Inventory',
            },
        ),
        migrations.CreateModel(
            name='SecondaryInterface',
            fields=[
                ('primary_interface', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='diffcheckerapp.primaryinterface')),
                ('ip_address', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('secret', models.CharField(max_length=50)),
                ('enable_monitoring', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Primary Interface Inventory',
            },
        ),
    ]
