from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Location(models.Model):
    label = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.label}"


class Category(models.Model):
    label = models.CharField(max_length=64)
    icon_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.label}"


class Amenity(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='amenity_category')

    def __str__(self):
        return f"{self.label}"


class Hotel(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=64)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='hotel_location')
    about_hotel = models.TextField(max_length=10000)
    amenity_list = models.ManyToManyField(Amenity,
                                          related_name='amenity_list')
    image_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.label}"

    def serialize(self):
        return {
            "id": self.id,
            "create-date": self.create_date.strftime(
                "%b %-d %Y, %-I:%M %p"),
            "label": self.label,
            "about": self.about_hotel,
            "amenities": [amenity.label for amenity in
                          self.amenity_list.all()],
            "image_url": self.image_url,
        }


class Room(models.Model):
    # Attributes used by view for displaying Rooms.
    available = True
    arrival = timezone.now()
    departure = timezone.now()

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
                              related_name='hotel')
    create_date = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=64)
    about_room = models.TextField(max_length=5000)
    number_on_door = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    num_beds = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    image_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.label}, Room # {self.number_on_door}"

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "about": self.about_room,
            "hotel": self.hotel.serialize(),
            "number_on_door": self.number_on_door,
            "floor": self.floor,
            "num_beds": self.num_beds,
            "max_guests": self.max_guests,
            "price": self.price,
            "image_url": self.image_url,
            "available": self.available
        }


class Booking(models.Model):
    """
    Repressents a one or many of Rooms plus Hotel combinations, booked with
    the same arrival and departure, grouped by a common confirmation value.
    """
    create_date = models.DateTimeField(auto_now=True)
    confirmation = models.PositiveIntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='guest')
    full_name = models.CharField(max_length=64)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    phone_number = models.CharField(max_length=64)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             related_name='room_booked')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE,
                              related_name='hotel_booked')
    price_booked = models.DecimalField(max_digits=6, decimal_places=0,
                                       default=0)
