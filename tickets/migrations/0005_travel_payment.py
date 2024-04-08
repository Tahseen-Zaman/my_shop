# Generated by Django 4.2 on 2023-05-22 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("tickets", "0004_alter_travel_arrival_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="travel",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="payment_ticket",
                to="users.payment",
            ),
        ),
    ]
