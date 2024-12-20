# Generated by Django 4.2 on 2023-05-22 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hotels", "0005_booking_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings_hotel",
                to="hotels.hotel",
            ),
        ),
    ]
