# Generated by Django 2.0 on 2017-12-19 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nicemodel', '0004_auto_20171219_0841'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user',
            new_name='nuser',
        ),
    ]
