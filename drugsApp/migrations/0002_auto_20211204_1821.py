# Generated by Django 3.2.8 on 2021-12-05 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescriber',
            name='IsOpioidPrescriber',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='TotalPrescriptions',
            field=models.IntegerField(default=0),
        ),
    ]