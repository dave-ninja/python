from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from datetime import datetime
import random

# Create your models here.

STATUS = (
    ('ordered','Ordered'),
    ('packed', 'Packed'),
    ('transit','In Transit'),
    ('delivered','Delivered')
)




class Ways(models.Model):
    city_from = models.CharField(max_length=30, verbose_name='From', default=" ")
    city_to = models.CharField(max_length=30, verbose_name='To', default=" ")
    dep_date = models.DateTimeField(verbose_name='Departure Date', null=True)
    arr_date = models.DateTimeField(verbose_name='Date of Arrival', null=True)
    some_currency = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=5,
        verbose_name='Price per Kilogram'
    )
    min_kg = models.DecimalField(verbose_name='Minimal kg', decimal_places=1, default=0.1, max_digits=50)

    status = models.CharField(max_length=30, choices=STATUS, default='ordered')

    class Meta:
        verbose_name = 'Ways'
        verbose_name_plural = 'Ways'

    def __str__(self):
        return str(f"{self.city_from} - {self.city_to}, {str(self.dep_date)[:16]}")



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed



class Bookings(models.Model):
    user_id = models.IntegerField(verbose_name='Client ID')
    name = models.CharField(max_length=30, verbose_name='Name', default=" ")
    username = models.CharField(max_length=30, verbose_name='Username', default=" ")
    phone = models.EmailField(max_length=30, verbose_name='Phone', default=" ")
    city_from = models.CharField(max_length=30,verbose_name='From', null=True)
    city_to = models.CharField(max_length=30,verbose_name='To', null=True, )

    kg = models.DecimalField(verbose_name='Kg', decimal_places=1, default=0.1, max_digits=50)


    class Meta:
        verbose_name = 'Bookings'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return str(f"{self.name}")



class Parcels(models.Model):
    city_from = models.CharField(max_length=30, verbose_name='From', default=" ")
    city_to = models.CharField(max_length=30, verbose_name='To', default=" ")
    kg = models.DecimalField(verbose_name='Kg', decimal_places=1, default=0.1, max_digits=50)

    track_number = models.CharField(max_length=30, verbose_name='Track number', default=' ')


    class Meta:
        verbose_name = 'Parcels'
        verbose_name_plural = 'Parcels'

    def __str__(self):
        return str(f"{self.city_from} - {self.city_to}")


class Clients(models.Model):
    client_id = models.IntegerField(verbose_name='Client ID')
    client_code = models.CharField(max_length=250, verbose_name='Client Code', default=" ")
    client_surname = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_name = models.CharField(max_length=250, verbose_name='Name', default=" ")
    client_name2 = models.CharField(max_length=250, verbose_name='Name2', default=" ")
    client_phone = models.CharField(max_length=250, verbose_name='Phone', default=" ")
    client_email = models.CharField(max_length=250, verbose_name='Email', default=" ")
    client_country = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_surname = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_country = models.IntegerField(verbose_name='Client Country')
    client_city = models.IntegerField(verbose_name='Client City')
    client_state = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_postcode = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_address = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_company = models.CharField(max_length=250, verbose_name='Surname', default=" ")
    client_info = models.CharField(max_length=250, verbose_name='Surname', default=" ")

    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return str(f"{self.client_id} - {self.client_name} {self.client_surname}")


class Stores(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Store ID')
    country = models.CharField(max_length=30, verbose_name='Country', default=" ")
    address = models.CharField(max_length=30, verbose_name='Address', default=" ")
    phone = models.CharField(max_length=30, verbose_name='Phone', default=" ")


    class Meta:
        verbose_name = 'Stores'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return str(f"{self.country}")