from django.db   import models
from core.models import TimeStampModel

class Book(TimeStampModel):
    user        = models.ForeignKey('users.User', on_delete = models.CASCADE)
    room        = models.ForeignKey('stays.Room', on_delete = models.CASCADE)
    room_option = models.ForeignKey('stays.RoomOption', on_delete = models.CASCADE)
    check_in    = models.DateField()
    check_out   = models.DateField()
    status      = models.BooleanField(default = False)

    class Meta:
        db_table = 'books'

class Payment(TimeStampModel):
    book      = models.ForeignKey('Book', on_delete = models.CASCADE)
    amount    = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        db_table = 'payments'