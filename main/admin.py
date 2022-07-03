from django.contrib import admin
from .models import Ways, Profile, Bookings, Parcels, Clients, Stores

from .models import User


# Register your models here.
admin.site.register(Ways)
admin.site.register(Clients)
admin.site.register(Profile)
admin.site.register(Bookings)
admin.site.register(Parcels)
admin.site.register(Stores)
