import datetime
import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from hotel.models import User, Hotel, Booking, Room, Location


def index(request):
    # Default route for the Hotel website.
    locations = Location.objects.all()
    return render(request, "hotel/index.html",
                  {"locations": locations, "home_page": "active"})


def search(request):
    # Get hotels for the location specified.
    hotels = Hotel.objects.filter(location=request.POST["location"]).all()
    if not hotels:
        messages.add_message(request, messages.WARNING,
                             "No hotels found.")
        return HttpResponseRedirect(reverse("index"))
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
    # Default route for the Hotel page with rooms, requires login.
    if not request.user.is_authenticated:
        # Provide a return URL for the User, after they have logged in.
        return_url = f'hotel/{hotel_id}'
        return render(request, "hotel/login.html",
                      {"login_page": "active", "return_url": return_url})
    return render(request, "hotel/hotel.html", {"hotel_id": hotel_id})


def hotel_info(request, hotel_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
    except Hotel.DoesNotExist:
        return JsonResponse({"error": "Hotel does not exist."}, status=404)

    if request.method == 'GET':
        return JsonResponse(hotel.serialize())


@login_required
def history(request):
    try:
        user = User.objects.get(pk=request.user.id);
        history = Booking.objects.filter(user=user).all()

    except User.DoesNotExist:
        print('User does not exist.')
        messages.add_message(request, messages.WARNING,
                             "No User found, please login.")
    return render(request, "hotel/history.html",
                  {"history": history, "history_page": "active"})


@require_http_methods(["POST"])
def booking(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must log in to book."}, status=401)
    data = json.loads(request.body)

    try:
        user = User.objects.get(pk=request.user.id)
        room = Room.objects.get(pk=data.get("room"))
        hotel = Hotel.objects.get(room_list__in=room)
        booking = Booking.objects.create(user=user,
                                         full_name=data.get("full_name"),
                                         room=room,
                                         hotel=hotel,
                                         confirmation=
                                         random.randrange(10000, 99999),
                                         arrival_date=data.get("arrival"),
                                         departure_date=data.get("departure"),
                                         phone_number=data.get("phone"),
                                         price_booked=data.get("price"))

        return JsonResponse({"confirmation": booking.confirmation},
                            status=201)
    except Room.DoesNotExist:
        print('Room does not exist.')
        return JsonResponse({"error": "Booking was not created."}, status=404)
    except User.DoesNotExist:
        print('User does not exist.')
        return JsonResponse({"error": "Booking was not created."}, status=404)
    except IntegrityError as error:
        print('Error creating a Booking.')
        print(error)
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
            # Return User to the Booking process, if they have a return url.
            if request.POST['return_url']:
                return HttpResponseRedirect(request.POST['return_url'])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hotel/login.html", {
                "message": "Invalid username and/or password.",
                "login_page": "active"
            })
    else:
        return render(request, "hotel/login.html", {"login_page": "active"})


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
            # Add first and last name if available.
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
        except IntegrityError:
            return render(request, "hotel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hotel/register.html",
                      {"register_page": "active"})
