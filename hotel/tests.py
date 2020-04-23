import datetime
from django.test import Client, TestCase

from .models import Booking, Room, User


#  Set testing year to next year.
def test_year():
    return datetime.date.today().year + 1


class BookingTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user("test", "test@home.com", "crossfit")

        # Create room.
        room1 = Room.objects.create(label="room one", price=100, max_guests=2,
                                    number_on_door=101, floor=2)

        # Dates
        # Book the room.
        Booking.objects.create(arrival_date=datetime.date(test_year(), 6, 1),
                               departure_date=datetime.date(test_year(), 6, 5),
                               confirmation=12345,
                               user_id=user.id, room=room1)

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
