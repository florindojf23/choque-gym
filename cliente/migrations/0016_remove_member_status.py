# Generated by Django 4.2.11 on 2024-06-24 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cliente", "0015_alter_member_status"),
    ]

    operations = [
        migrations.RemoveField(model_name="member", name="status",),
    ]
