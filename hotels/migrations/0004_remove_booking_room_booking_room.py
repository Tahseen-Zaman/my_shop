# Generated by Django 4.2 on 2023-05-07 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hotels", "0003_booking_room_alter_booking_hotel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="room",
        ),
        migrations.AddField(
            model_name="booking",
            name="room",
            field=models.ManyToManyField(
                related_name="bookings_room", to="hotels.room"
            ),
        ),
    ]