# Generated by Django 5.0.1 on 2024-01-11 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bus_reserve", "0007_alter_busschedule_bus_id_alter_busschedule_route_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="busschedule",
            old_name="datetime",
            new_name="depart_date",
        ),
    ]
