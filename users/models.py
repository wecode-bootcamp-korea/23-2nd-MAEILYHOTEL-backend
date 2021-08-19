from django.db   import models
from core.models import TimeStampModel

class User(models.Model):
    nickname   = models.CharField(max_length = 45)
    email      = models.CharField(max_length = 2000)
    password   = models.CharField(max_length = 200, null = True)
    birth_date = models.DateField(null = True)
    agreement  = models.BooleanField(default = False)
    point      = models.DecimalField(max_digits = 10, decimal_places = 2, default=0)
    kakao_id   = models.CharField(max_length = 45)
    userlevel  = models.ForeignKey('UserLevel', on_delete = models.CASCADE)

    class Meta:
        db_table = 'users'

class UserLevel(models.Model): 
    name     = models.CharField(max_length = 45)
    discount = models.FloatField()

    class Meta:
        db_table = 'userlevels'

class Wishlist(TimeStampModel):
    user     = models.ForeignKey('User', on_delete = models.CASCADE)
    staytype = models.ForeignKey('stays.Staytype', on_delete = models.CASCADE)

    class Meta:
        db_table = 'wishlists'