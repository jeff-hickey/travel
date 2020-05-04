from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("hotel/<int:hotel_id>", views.hotel, name="hotel"),
    path("checkout", views.checkout, name="checkout"),
    path("booking/<int:confirmation>", views.booking, name="booking"),
    path("history", views.history, name="history"),
    # API urls
    path("hotel-rooms/<int:hotel_id>/<slug:arrival>/<slug:departure>",
         views.hotel_rooms, name="hotel"),
    path("get_room_available/<int:room_id>/<slug:arrival>/<slug:departure>",
         views.get_room_available, name="room_available"),
    path("cart/<int:room_id>/<slug:arrival>/<slug:departure>/<slug:price>",
         views.cart, name="cart"),
    # Account creation and login.
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
