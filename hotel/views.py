import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from hotel.forms import SearchForm, CheckOutForm
from hotel.models import User, Hotel, Booking, Room


def index(request):
    # Default route for the Hotel website.
    if "location" in request.session:
        form = SearchForm({"arrival": request.session["arrival"],
                           "departure": request.session["departure"],
                           "location": request.session["location"]})
        print(request.session["location"])
    else:
        form = SearchForm()
    hotels = Hotel.objects.all()
    return render(request, "hotel/index.html",
                  {"home_page": "active", "form": form, "hotels": hotels})


def search(request):
    """
    Handles Hotel search queries from the Home and Search pages.
    :param request: POST containging arrival and departure dates, location.
    :return: List of Hotels.
    """
    # Validate the search input.
    form = SearchForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        messages.add_message(request, messages.WARNING,
                             "There was an error.")
        return render(request, "hotel/search.html",
                      {"home_page": "active", "form": form})

    # Add search data to session.
    request.session['arrival'] = str(form.cleaned_data["arrival"])
    request.session['departure'] = str(form.cleaned_data["departure"])
    request.session['location'] = str(form.cleaned_data["location"].id)

    # Get hotels for the location specified.
    hotels = Hotel.objects.filter(location=form.cleaned_data['location']).all()
    if not hotels:
        print("NO HOTELS")
        messages.add_message(request, messages.WARNING,
                             "No hotels found.")

    return render(request, "hotel/search.html",
                  {"hotels": hotels, "form": form})


def get_room_available(request, room_id, arrival, departure):
    """
    API for looking up room availability.
    :param request:
    :param room_id:
    :param arrival:
    :param departure:
    :return: True or False room-availability in json format.
    """
    if _room_available(request, room_id, arrival, departure):
        return JsonResponse({"room-availability": "True"}, status=201)
    return JsonResponse({"room-availability": "False"}, status=403)


def _room_available(request, room_id, arrival, departure):
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
        return False

    # Otherwise, the room is available.
    return True


def hotel(request, hotel_id):
    # Default route for the Hotel page displaying Rooms, requires login.
    if not request.user.is_authenticated:
        # Provide a return URL for the User, after they have logged in.
        return_url = f'hotel/{hotel_id}'
        return render(request, "hotel/login.html",
                      {"login_page": "active", "return_url": return_url})
    hotel = Hotel.objects.get(pk=hotel_id)
    return render(request, "hotel/rooms.html", {"hotel": hotel})


def hotel_rooms(request, hotel_id, arrival, departure):
    """
    API method returning available rooms for specified hotel.
    :param request:
    :param hotel_id:
    :param arrival:
    :param departure:
    :return: List of rooms in json format with availability flags set.
    """
    try:
        # Lookup the hotel.
        hotel = Hotel.objects.get(pk=hotel_id)
        room_list = Room.objects.filter(hotel=hotel).all()

        # Create date objects from the string parameters.
        new_arrival = datetime.datetime.strptime(
            arrival, "%Y-%m-%d").date()
        new_departure = datetime.datetime.strptime(
            departure, "%Y-%m-%d").date()

        # Build a ist of rooms with availability flags set.
        final_list = []
        for room in room_list:
            # Make sure rooms are available.
            available = _room_available(request, room.id, new_arrival,
                                        new_departure)
            if not available:
                room.available = False
            final_list.append(room)

    except Hotel.DoesNotExist:
        return JsonResponse({"error": "Hotel does not exist."}, status=404)

    if request.method == 'GET':
        json_data = {
            "rooms": [room.serialize() for room in final_list]
        }
        return JsonResponse(json_data, safe=False)


@login_required
def history(request):
    """
    Retrieves a users booking history.
    :param request:
    :return:
    """
    try:
        user = User.objects.get(pk=request.user.id)
        history = Booking.objects.filter(user=user).all().order_by(
            "-create_date")
        if not history:
            messages.add_message(request, messages.WARNING,
                                 "No booking history found.")
    except User.DoesNotExist:
        print('User does not exist.')
        messages.add_message(request, messages.WARNING,
                             "No User found, please login.")
    return render(request, "hotel/history.html",
                  {"history": history, "history_page": "active"})


def cart(request, room_id, price):
    """
    Removes a Room if it exists or Stores the Room in the users session
    along with price arrival and departure dates.
    :param request:
    :param room_id:
    :param price:
    :return:
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated."},
                            status=401)
    # Create the room to added to cart.
    room = {"id": room_id, "arrival": request.session['arrival'],
            "departure": request.session['departure'], "price": price}

    # Check for an existing cart.
    if "cart" not in request.session:
        # Add the room dict.
        cart = {room_id: room}
        request.session["cart"] = cart
        return JsonResponse({"message": "Room added to cart."}, status=200)

    # Remove room if it exists in the cart.
    cart = request.session['cart']
    if str(room_id) in cart:
        cart.pop(str(room_id))
        request.session['cart'] = cart
        return JsonResponse({"message": "Room deleted from cart."}, status=200)

    # Add room to cart.
    cart[room_id] = room
    request.session['cart'] = cart
    return JsonResponse({"message": "Room added to cart."}, status=200)


def checkout(request):
    """
    Render the checkout page for GET requests or create the Booking
    with POST.
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    try:
        # User info is needed for the checkout process.
        user = User.objects.get(pk=request.user.id)

        # Cart is needed to checkout.
        if "cart" not in request.session:
            messages.add_message(request, messages.WARNING,
                                 "There is nothing in the shopping cart. ")
            return render(request, "hotel/checkout.html")

        # Get the cart from the session.
        cart = request.session["cart"]

        # Build a list of rooms to book.
        total_price = 0
        room_list = []
        for room_id in cart:
            room = Room.objects.get(pk=room_id)
            total_price += int(room.price)
            # Add dates to the room from the users cart.
            room.arrival = cart[room_id].get('arrival')
            room.departure = cart[room_id].get('departure')
            room_list.append(room)

        # Render the checkout form.
        if request.method == "GET":
            # Pre-populate the Checkout form.
            form = CheckOutForm(
                initial={'first_name': user.first_name,
                         'last_name': user.last_name,
                         'username': user.username,
                         'email': user.email})
            return render(request, "hotel/checkout.html",
                          {"form": form, "room_list": room_list,
                           "total_price": total_price})

        # Validate the checkout form and store the booking.
        else:
            form = CheckOutForm(request.POST)
            if not form.is_valid():
                messages.add_message(request, messages.WARNING,
                                     "Form is invalid. ")
                return render(request, "hotel/checkout.html",
                              {"form": form, "room_list": room_list})

            # Generate a confirmation number.
            conf = random.randrange(10000, 99999)

            # Create a booking record per room with common confirmation.
            for room in room_list:
                hotel = Hotel.objects.get(pk=room.hotel.id)
                booking = Booking(user=user, full_name=form.full_name(),
                                  room=room,
                                  hotel=hotel, confirmation=conf,
                                  arrival_date=cart[room_id].get("arrival"),
                                  departure_date=cart[room_id].get("arrival"),
                                  phone_number=form.cleaned_data["phone"],
                                  price_booked=cart[room_id].get("price"))
                booking.save()

                # Reset the cart, booking was successful.
                request.session['cart'] = {}
                messages.add_message(request, messages.SUCCESS,
                                     "Booking Successful. ")
            return HttpResponseRedirect(
                reverse("booking", args=(conf,)))
    except Room.DoesNotExist:
        print('Room does not exist.')
        messages.add_message(request, messages.WARNING,
                             "Room does not exist.")
        return render(request, "hotel/checkout.html")
    except User.DoesNotExist:
        print('User does not exist.')
        messages.add_message(request, messages.WARNING,
                             "User does not exist.")
        return render(request, "hotel/checkout.html")
    except IntegrityError as error:
        print('Error creating a Booking.')
        print(error)
        messages.add_message(request, messages.WARNING,
                             "Error creating a Booking.")
        return render(request, "hotel/checkout.html")


def booking(request, confirmation):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Include all Room details.
    booking_list = Booking.objects.filter(confirmation=confirmation).all()
    total_price = 0
    for booking in booking_list:
        print(booking.price_booked)
        total_price += int(booking.price_booked)
    if not booking_list:
        messages.add_message(request, messages.WARNING,
                             "Bookings Not Found.")
    return render(request, "hotel/booking.html",
                  {"booking_list": booking_list, "total_price": total_price})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Set default dates for looking at rooms.
            request.session['arrival'] = str(timezone.now())
            request.session['departure'] = str(
                timezone.now() + timedelta(days=1))

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
