# Generated by Django 4.2.11 on 2024-06-27 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cliente", "0002_alter_member_status"),
        ("custom", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Status",),
    ]
