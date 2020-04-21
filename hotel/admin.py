from django.contrib import admin

from hotel.models import User, Room, Amenity, Hotel


class UserAdmin(admin.ModelAdmin):
    pass

class HotelAdmin(admin.ModelAdmin):
    list_display = ("create_date", "label")


class AmenityAdmin(admin.ModelAdmin):
    list_display = ("create_date", "label")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("create_date", "label", "num_beds", "number_on_door")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Amenity, AmenityAdmin)
