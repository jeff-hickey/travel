import datetime
import json
import random

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from hotel.models import User, Hotel, Booking, Room


def index(request):
    # Default route for the Hotel website.
    locations = Hotel.objects.order_by('location_city').values(
        'location_city').distinct()
    print(locations)
    return render(request, "hotel/index.html", {"locations": locations})


def search(request):
    hotels = Hotel.objects.filter(location_city=request.POST["location"]).all()
    print(hotels)
    return render(request, "hotel/search.html", {"hotels": hotels})


def room_available(request, room_id, arrival, departure):
    room = Room.objects.get(pk=room_id)

    # A booked arrival date is less than the requested arrival date and booked
    # departure date greater than the requested arrival date.
    booking_1 = Booking.objects.filter(room=room, arrival_date__lte=arrival,
                                       departure_date__gte=departure).exists()

    # A booked arrival is greater than the requested arrival date and booked
    # departure is less than the requested departure.
    booking_2 = Booking.objects.filter(room=room, arrival_date__gte=arrival,
                                       departure_date__lte=departure).exists()

    # A booked arrival date is less than the requested departure date and
    # booked departure is greater than requested departure
    booking_3 = Booking.objects.filter(room=room, arrival_date__lte=departure,
                                       departure_date__gte=departure).exists()

    # if any of these bookings exist, there is no availability
    if booking_1 or booking_2 or booking_3:
        return JsonResponse({"room-availability": "False"}, status=403)

    # Otherwise, the room is available.
    return JsonResponse({"room-availability": "True"}, status=201)


def hotel(request, hotel_id):
    # Default route for the Hotel website.
    return render(request, "hotel/hotel.html", {"hotel_id": hotel_id})


def hotel_info(request, hotel_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
    except Hotel.DoesNotExist:
        return JsonResponse({"error": "Hotel does not exist."}, status=404)

    if request.method == 'GET':
        return JsonResponse(hotel.serialize())


@require_http_methods(["POST"])
def booking(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse({"error": "User must log in to book."},
    #     status=401)
    data = json.loads(request.body)
    print(data)
    try:
        user = User.objects.get(pk=request.user.id)
        booking = Booking.objects.create(user=user,
                                         confirmation=
                                         random.randrange(10000, 99999),
                                         arrival_date=data.get("arrival"),
                                         departure_date=data.get("departure"),
                                         phone_number=data.get("phone"),
                                         price_booked=data.get(
                                             "price"))

        print(booking)
        return JsonResponse({"confirmation": booking.confirmation},
                            status=201)
    except User.DoesNotExist:
        return JsonResponse({"error": "Booking was not created."}, status=404)
    except IntegrityError:
        return JsonResponse({"error": "Booking was not created."}, status=500)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hotel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hotel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "hotel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hotel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hotel/register.html")
