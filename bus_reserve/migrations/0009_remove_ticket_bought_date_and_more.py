# Generated by Django 5.0.1 on 2024-01-22 14:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_reserve', '0008_ticket'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='bought_date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='busschedule',
            name='bus_id',
            field=models.OneToOneField(default='deleted', on_delete=django.db.models.deletion.SET_DEFAULT, to='bus_reserve.bus'),
        ),
        migrations.CreateModel(
            name='TicketOrder',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('bought_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(blank=True, default=1)),
                ('ticket_id', models.ManyToManyField(to='bus_reserve.ticket')),
                ('transaction_id', models.ForeignKey(default='Refunded', on_delete=django.db.models.deletion.SET_DEFAULT, to='bus_reserve.transactiontable')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
