# Generated by Django 4.2.11 on 2024-06-24 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("custom", "0004_delete_academiclevel"),
        ("cliente", "0013_member_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="custom.status",
            ),
        ),
    ]
