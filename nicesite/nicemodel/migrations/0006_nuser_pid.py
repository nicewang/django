# Generated by Django 2.0 on 2017-12-21 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nicemodel', '0005_auto_20171219_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuser',
            name='pid',
            field=models.IntegerField(default=0),
        ),
    ]
