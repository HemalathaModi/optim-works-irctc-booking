from django.contrib import admin
from .models import Station, Train, Booking, Passenger, UserProfile, Payment

admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(UserProfile)
admin.site.register(Payment)

# Register your models here.
