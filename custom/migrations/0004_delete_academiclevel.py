# Generated by Django 4.2.11 on 2024-06-24 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("custom", "0003_status_name"),
    ]

    operations = [
        migrations.DeleteModel(name="AcademicLevel",),
    ]