import json, jwt, requests, boto3, uuid

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg

from users.models   import *
from reviews.models import Review, ReviewImage
from stays.models   import Staytype, Room
from books.models   import Book
from users.utils    import login_decorator
from my_settings    import AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

from datetime       import date

class CloudStorage:
    def __init__(self, id, password, bucket):
        self.id        = id
        self.password  = password
        self.bucket    = bucket
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id     = self.id,
            aws_secret_access_key = self.password
        )

    def upload_file(self, image):
        upload_key = str(uuid.uuid1()).replace("-","") + image.name
        
        self.s3_client.upload_fileobj(
            image,
            self.bucket,
            upload_key,
            ExtraArgs = {
                "ContentType": image.content_type
            }
        )
        return upload_key

class ReviewsView(View):
    @login_decorator
    def post(self, request, stay_id):
        room_id       = request.POST.get("room_id")
        rating        = request.POST.get("rating")
        comment       = request.POST.get("comment")
        images        = request.FILES.getlist("image")
        cloud_storage = CloudStorage(id = AWS_S3_ACCESS_KEY_ID, password = AWS_S3_SECRET_ACCESS_KEY, bucket = AWS_STORAGE_BUCKET_NAME)
        
        rating_dict = {
            "1"  : 1,
            "1.5": 1.5,
            "2"  : 2,
            "2.5": 2.5,
            "3"  : 3,
            "3.5": 3.5,
            "4"  : 4,
            "4.5": 4.5,
            "5"  : 5
        }

        if not Room.objects.filter(id = room_id).exists(): 
            return JsonResponse({"message" : "INVALID_ROOM"}, status = 400)

        if rating not in rating_dict.keys(): 
            return JsonResponse({"message" : "INVALID_RATE_NUMBER"}, status = 400)

        if not images:
            return JsonResponse({"message" : "IMAGE_DOES_NOT_EXIST"}, status = 400)

        review = Review.objects.create(
            user   = request.user,
            room   = Room.objects.get(id = room_id),
            rating = rating
        )

        if comment:
            review.comment = comment
            review.save()        
            
        for image in images:
            upload_key = cloud_storage.upload_file(image)
            image_url  = f"https://s3.ap-northeast-2.amazonaws.com/maeilyhotel/{upload_key}"
            ReviewImage.objects.create(
                review    = review,
                image_url = cloud_storage.upload_file.image_url
            )
            
        return JsonResponse({"message" : "CREATED"}, status = 201)

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


