from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Account creation and login.
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
