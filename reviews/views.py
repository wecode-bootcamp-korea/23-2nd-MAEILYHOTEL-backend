from users.utils import login_decorator

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg

from reviews.models import Review
from stays.models   import Staytype
from books.models   import Book
from datetime       import date

class ReviewsView(View):
    def get(self, request, stay_id):
        if not Staytype.objects.filter(id=stay_id).exists():
            return JsonResponse({"message":"INVALID_ID"}, status=404)

        reviews   = Review.objects.filter(room__staytype_id=stay_id).select_related('room','user').prefetch_related('reviewimage_set').order_by('-created_at')[:5]
        avg_score = round(Review.objects.filter(room__staytype_id=stay_id).aggregate(avg_score=Avg('rating'))['avg_score'],2) if reviews else 0
        
        data = [{
            "id"          : review.id,
            "userId"      : review.user.nickname,
            "score"       : review.rating,
            "description" : review.comment,
            "image"       : [image.image_url for image in review.reviewimage_set.all()],
            "created_date": review.created_at.date(),
            "room"        : review.room.name
        } for review in reviews]

        return JsonResponse({"AvgScore":avg_score,"data":data}, status=200)

class ReviewAvailableView(View):
    @login_decorator
    def get(self, request, stay_id):
        if not Staytype.objects.filter(id=stay_id).exists():
            return JsonResponse({"message":"INVALID_ID"}, status=404)

        is_available = Book.objects.filter(room__staytype_id=stay_id, user=request.user, status=True).exists()
        
        return JsonResponse({"is_available":is_available}, status=200)   


