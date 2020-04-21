from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Amenity(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=2)
    label = models.TextField(max_length=64)


class Hotel(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    label = models.TextField(max_length=64)
    about_info = models.TextField(max_length=10000)
    amenity_list = models.ForeignKey(Amenity, on_delete=models.CASCADE,
                                     related_name='amenity_list')
    room_list = models.ForeignKey(Amenity, on_delete=models.CASCADE,
                                  related_name='room_list')


class Room(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    label = models.TextField(max_length=64)
    about_info = models.TextField(max_length=5000)
    number_on_door = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    num_beds = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=1)
