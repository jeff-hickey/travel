from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("hotel/<int:hotel_id>", views.hotel, name="hotel"),
    path("history", views.history, name="history"),
    # API urls
    path("hotel-info/<int:hotel_id>", views.hotel_info, name="hotel"),
    path("booking", views.booking, name="booking"),
    path("room_available/<int:room_id>/<str:arrival>/<str:departure>",
         views.room_available, name="room_available"),
    # Account creation and login.
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
