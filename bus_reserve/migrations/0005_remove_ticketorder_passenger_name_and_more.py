# Generated by Django 5.0.1 on 2024-01-17 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bus_reserve", "0004_delete_departinfo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticketorder",
            name="passenger_name",
        ),
        migrations.RemoveField(
            model_name="ticketorder",
            name="passenger_phone",
        ),
    ]
