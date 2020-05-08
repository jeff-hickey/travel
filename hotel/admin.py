from django.contrib import admin

from hotel.models import User, Room, Amenity, Hotel, Category, Location, \
    Booking


class UserAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class HotelAdmin(admin.ModelAdmin):
    list_display = ("label", "create_date")
    filter_horizontal = ("amenity_list",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "icon_name")


class AmenityAdmin(admin.ModelAdmin):
    list_display = ("label", "create_date")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("label", "create_date", "num_beds", "number_on_door")


class BookingAdmin(admin.ModelAdmin):
    list_display = ("create_date", "user", "full_name", "confirmation")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Booking, BookingAdmin)
