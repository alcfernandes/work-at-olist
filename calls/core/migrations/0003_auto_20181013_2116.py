# Generated by Django 2.1.2 on 2018-10-13 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181013_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingrule',
            name='end_time',
            field=models.TimeField(verbose_name='end time (excluding)'),
        ),
    ]