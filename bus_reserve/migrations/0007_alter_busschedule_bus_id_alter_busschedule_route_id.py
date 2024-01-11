# Generated by Django 5.0.1 on 2024-01-11 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus_reserve", "0006_alter_route_arrive_loc_alter_route_depart_loc"),
    ]

    operations = [
        migrations.AlterField(
            model_name="busschedule",
            name="bus_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="bus_reserve.bus"
            ),
        ),
        migrations.AlterField(
            model_name="busschedule",
            name="route_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="bus_reserve.route"
            ),
        ),
    ]
