from django.db import models
from datetime import datetime, timedelta

WEEK = ['월','화','수','목','금','토','일']
W1   = ['금','토']
W2   = ['일','월']

class Category(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'categories'

class Staytype(models.Model):
    category    = models.ForeignKey('Category', on_delete = models.PROTECT)
    name        = models.CharField(max_length = 45)
    address     = models.CharField(max_length = 2000)
    longitude   = models.DecimalField(max_digits = 10, decimal_places = 7)
    latitude    = models.DecimalField(max_digits = 10, decimal_places = 7)
    description = models.TextField()
    facility    = models.ManyToManyField('Facility', through = 'StaytypeFacility', related_name = 'staytypes')

    @classmethod
    def get_discount_one_price(cls, price, date):
        price = float(price)
        if WEEK[date.weekday()] in W1:
            price = price * 1.3
        if WEEK[date.weekday()] in W2:
            price = price * 0.7
        return price

    class Meta:
        db_table = 'staytypes'

class StaytypeFacility(models.Model):
    staytype  = models.ForeignKey('Staytype', on_delete = models.CASCADE)
    facility  = models.ForeignKey('Facility', on_delete = models.CASCADE)

    class Meta:
        db_table = 'staytypes_facilities'

class Facility(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'facilities'

class StaytypeImage(models.Model):
    image_url = models.CharField(max_length = 2000)
    staytype  = models.ForeignKey('Staytype', on_delete = models.CASCADE)

    class Meta:
        db_table = 'staytypeimages'


class Room(models.Model):
    staytype  = models.ForeignKey('Staytype', on_delete = models.PROTECT)
    name      = models.CharField(max_length = 45)
    quantity  = models.IntegerField()
    image_url = models.CharField(max_length = 2000)
    people    = models.PositiveIntegerField()

    @classmethod
    def get_discount_prices(cls, price,check_in,check_out):
        option_price = float(price)
        total = 0
        date_list = [check_in + timedelta(i) for i in range((check_out - check_in).days)]
        for date in date_list:
            price = option_price
            if WEEK[date.weekday()] in W1:
                price = price * 1.3
            if WEEK[date.weekday()] in W2:
                price = price * 0.7
            total += price
        avg = total/len(date_list)
        return {
            "total": total,
            "avg"  : round(avg,-2)
            }

    class Meta:
        db_table = 'rooms'

class RoomOption(models.Model):
    room      = models.ForeignKey('Room', on_delete = models.PROTECT)
    name      = models.CharField(max_length = 45)
    price     = models.DecimalField(max_digits = 10, decimal_places = 2)
    check_in  = models.TimeField()
    check_out = models.TimeField()

    class Meta:
        db_table = 'roomoptions'

