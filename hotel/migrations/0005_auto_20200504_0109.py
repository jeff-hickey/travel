# Generated by Django 3.0.3 on 2020-05-04 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_auto_20200501_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='room_list',
        ),
        migrations.AddField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hotel', to='hotel.Hotel'),
            preserve_default=False,
        ),
    ]
