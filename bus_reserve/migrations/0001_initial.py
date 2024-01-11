# Generated by Django 5.0.1 on 2024-01-11 05:04

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bus",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("d031d9dc-d0dc-4f13-befb-8d72b1f72bbb"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("model", models.CharField(max_length=15)),
                ("capacity", models.IntegerField(default=20)),
                ("number_plate", models.CharField(max_length=20)),
                ("image", models.ImageField(upload_to="bus_images/")),
            ],
        ),
        migrations.CreateModel(
            name="DepartInfo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("0dfee11f-32ac-4a19-a379-20704eef67fd"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("user_arrived", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("3de3a9e7-541b-49f4-a68d-37a8a600dbd3"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "depart_loc",
                    models.CharField(
                        choices=[
                            (1, "Kathmandu"),
                            (2, "Hetuada"),
                            (3, "Tandi"),
                            (4, "Inarwa"),
                            (5, "Bharatpur"),
                            (6, "Ithari"),
                            (7, "Polkhara"),
                        ],
                        max_length=20,
                    ),
                ),
                ("distance", models.IntegerField(default=1)),
                ("price", models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name="BusSchedule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("e5b28c1b-e1a5-46bb-9264-30113f89112f"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime", models.DateTimeField()),
                (
                    "bus_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.bus",
                    ),
                ),
                (
                    "route_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.route",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("4e815dcf-d205-41af-a15f-a930bd3a596b"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("number", models.CharField(max_length=3)),
                ("is_free", models.BooleanField(blank=True, default=True)),
                (
                    "bus_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.bus",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicektHistory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("37475699-b29b-4f31-928b-2456334b1afc"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("cancelled", models.BooleanField(blank=True, default=False)),
                ("refunded", models.BooleanField(blank=True, default=False)),
                (
                    "depart_info_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.departinfo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicektOrder",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("60840821-fe02-4e83-80f6-868a70e37381"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("bought_date", models.DateTimeField(auto_now_add=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="departinfo",
            name="ticket_order_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bus_reserve.ticektorder",
            ),
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.UUID("24a71ec7-81a0-4ae9-8f1f-1162ef32cfd7"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("ticket_num", models.CharField(max_length=10)),
                ("is_bought", models.BooleanField(blank=True, default=False)),
                (
                    "schedule_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.busschedule",
                    ),
                ),
                (
                    "seat_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_reserve.seat",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ticektorder",
            name="ticket_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="bus_reserve.ticket"
            ),
        ),
    ]
