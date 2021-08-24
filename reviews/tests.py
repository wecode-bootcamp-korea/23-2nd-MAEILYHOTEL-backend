import json, jwt

from users.models     import User, UserLevel
from stays.models     import Category, Staytype, Room
from reviews.models   import Review, ReviewImage

from django.test   import TestCase, Client
from my_settings   import SECRET_KEY
from datetime      import datetime

# Create your tests here.

class ReviewsgetTest(TestCase):
    def setUp(self):
        userlevel = UserLevel.objects.create(name='silver', discount=0)
        user      = User.objects.create(
                    id        = 1,
                    kakao_id  = 12341234,
                    email     = 'email',
                    nickname  = 'nickname',
                    point     = 1000000,
                    userlevel = userlevel)
        category = Category.objects.create(id = 1, name="호텔")
        staytype = Staytype.objects.bulk_create([
                    Staytype(
                        id          = 1,
                        name        = "강릉호텔",
                        address     = "강원도 강릉시 강릉동 1-1",
                        longitude   = 12.345,
                        latitude    = 12.345,
                        description = "강릉강릉",
                        category    = category),
                    Staytype(
                        id          = 2,
                        name        = "서울호텔",
                        address     = "서울특별시 서울동 1-1",
                        longitude   = 12.345,
                        latitude    = 12.345,
                        description = "서울서울",
                        category    = category)
                        ]
                    )        
        Room.objects.bulk_create([
            Room(
                id          = 1,
                name        = "스위트룸",
                quantity    = 4,
                image_url   = "url",
                people      = 2,
                staytype_id = 1),
            Room(
                id          = 2,
                name        = "스위트룸",
                quantity    = 4,
                image_url   = "url",
                people      = 2,
                staytype_id = 2)
                ]
            )
        review = Review.objects.create(
                id      = 1,
                rating  = 3.5,
                comment = "괜찮았습니다",
                room_id = 1,
                user    = user
            )
        ReviewImage.objects.create(
                image_url = 'url',
                review    = review
            )
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = 'HS256')

    def tearDown(self):
        ReviewImage.objects.all().delete()
        Review.objects.all().delete()
        Room.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()
        UserLevel.objects.all().delete()
        User.objects.all().delete()

    def test_reviewsview_get_success(self):
        client   = Client()
        response = client.get('/stays/1/reviews')
        self.assertEqual(response.json(),
        {
        "AvgScore": 3.5,
        "data": [
            {
                "id": 1,
                "userId": "nickname",
                "score": 3.5,
                "description": "괜찮았습니다",
                "image": ['url'],
                "created_date": f"{datetime.today().date()}",
                "room": "스위트룸"
            }
                ]
        }
                )
        self.assertEqual(response.status_code, 200)
    
    def test_reviewsview_get_no_reviews_success(self):
        client   = Client()
        response = client.get('/stays/2/reviews')
        self.assertEqual(response.json(), {"AvgScore": 0, "data": []})
        self.assertEqual(response.status_code, 200)
    
    def test_reviewsview_invalid_id_failed(self):
        client   = Client()
        response = client.get('/stays/100/reviews')
        self.assertEqual(response.json(),{'message':'INVALID_ID'})
        self.assertEqual(response.status_code, 404)
