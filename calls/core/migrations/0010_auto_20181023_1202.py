# Generated by Django 2.1.2 on 2018-10-23 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_call_duration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calldetail',
            unique_together={('type', 'call_id')},
        ),
    ]
