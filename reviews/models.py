import random

from django.db        import models
from django.db.models import Max

from core.models      import TimeStampModel

class Review(TimeStampModel):
    user    = models.ForeignKey('users.User', on_delete = models.SET_NULL, null = True)
    room    = models.ForeignKey('stays.Room', on_delete = models.CASCADE)
    rating  = models.FloatField()
    comment = models.TextField(null = True)

    @classmethod
    def get_random(cls, reviews):
        if not reviews:
            return None
            
        return reviews[random.randrange(reviews.count())]

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review    = models.ForeignKey('Review', on_delete = models.CASCADE)
    image_url = models.CharField(max_length = 2000)

    class Meta:
        db_table = 'reviewimages'
