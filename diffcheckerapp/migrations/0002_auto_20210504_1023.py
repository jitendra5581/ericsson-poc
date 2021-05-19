# Generated by Django 3.1.7 on 2021-05-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diffcheckerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='primaryinterface',
            options={'verbose_name_plural': 'Primary Devices'},
        ),
        migrations.AlterModelOptions(
            name='secondaryinterface',
            options={'verbose_name_plural': 'Secondary Devices'},
        ),
        migrations.AlterField(
            model_name='primaryinterface',
            name='enable_monitoring',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='primaryinterface',
            name='ip_address',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.AlterField(
            model_name='secondaryinterface',
            name='enable_monitoring',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='secondaryinterface',
            name='ip_address',
            field=models.GenericIPAddressField(unique=True),
        ),
    ]