import datetime
from django.test import Client, TestCase

from .models import Booking, Room, User, Location, Hotel, Amenity, Category


#  Set testing year to next year.
def test_year():
    return datetime.date.today().year + 1


class BookingTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user("test", "test@home.com", "crossfit")

        location1 = Location.objects.create(label="Test Locations")

        category1 = Category.objects.create(label="Swimming Pool",
                                            icon_name="pool.jpg")
        category2 = Category.objects.create(label="Wifi", icon_name="wifi.jpg")
        amenity1 = Amenity.objects.create(label="Free and Paid Wifi",
                                          category=category2)
        amenity2 = Amenity.objects.create(label="6 Pools with Hot Tub",
                                          category=category1)

        room1 = Room.objects.create(label="room one", price=100, max_guests=2,
                                    number_on_door=101, floor=2)

        # Create the Hotel adding room plus amenitues.
        hotel1 = Hotel.objects.create(label="Test Hotel", location=location1,
                                      about_hotel="Wonderful hotel.")
        hotel1.room_list.add(room1)
        hotel1.amenity_list.add(amenity1)
        hotel1.amenity_list.add(amenity2)

        # Book the room.
        Booking.objects.create(arrival_date=datetime.date(test_year(), 6, 1),
                               departure_date=datetime.date(test_year(), 6, 5),
                               confirmation=12345,
                               user_id=user.id, room=room1, hotel=hotel1)

    def test_room_availability(self):
        c = Client()
        # No availability, same dates
        response = c.get(
            f"/room_available/1/{datetime.date(test_year(), 6, 1)}/"
            + f"{datetime.date(test_year(), 6, 5)}")
        self.assertEquals(response.json()['room-availability'], "False")
        self.assertEqual(response.status_code, 403)

        # No availability, arrival before booked arrival
        response = c.get(
            f"/room_available/1/{datetime.date(test_year(), 5, 29)}/"
            + f"{datetime.date(test_year(), 6, 5)}")
        self.assertEquals(response.json()['room-availability'], "False")
        self.assertEqual(response.status_code, 403)

        # No availability, arrival after booked arrival, departure before
        # booked departure
        response = c.get(
            f"/room_available/1/{datetime.date(test_year(), 6, 2)}/"
            + f"{datetime.date(test_year(), 6, 4)}")
        self.assertEquals(response.json()['room-availability'], "False")
        self.assertEqual(response.status_code, 403)

        # Rooms available, arrival and departure before booked arrival
        response = c.get(
            f"/room_available/1/{datetime.date(test_year(), 5, 10)}/"
            + f"{datetime.date(test_year(), 5, 11)}")
        self.assertEquals(response.json()['room-availability'], "True")
        self.assertEqual(response.status_code, 201)
