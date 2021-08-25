import json, jwt

from datetime      import datetime, time

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock  import patch, MagicMock
from reviews.models import *
from stays.models   import *
from users.models   import *
from my_settings    import SECRET_KEY

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

    def test_reviewsavailable_get_success(self):
        client   = Client()
        headers = {"HTTP_Authorization": self.token}
        response = client.get('/stays/1/reviewsavailable', **headers, content_type='application/json')
        self.assertEqual(response.json(),{"is_available":False})
        self.assertEqual(response.status_code, 200)

class ReviewspostTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="호텔")
        staytype = Staytype.objects.create(
                id          = 1,
                name        = "강릉호텔",
                address     = "강원도 강릉시 강릉동 1-1",
                longitude   = 12.345,
                latitude    = 12.345,
                description = "강릉강릉",
                category    = category
            )
        facility = Facility.objects.create(name="facility")
        StaytypeFacility.objects.create(facility=facility,staytype=staytype)        
        StaytypeImage.objects.create(image_url="url",staytype=staytype)
        
        room =  Room.objects.create(
                id        = 1,
                name      = "스위트룸",
                quantity  = 4,
                image_url = "url",
                people    = 2,
                staytype  = staytype
            )
        
        RoomOption.objects.create(
                name      = "숙박",
                price     = 100000,
                check_in  = time(15,00),
                check_out = time(12,00),
                room      = room
            )

        userlevel = UserLevel.objects.create(
            name = "silver", discount = 0.1
        )

        self.user = User.objects.create(
            nickname  = "nickname",
            email     = "email@email.com",
            point     = 100000,
            kakao_id  = "1234567",
            userlevel = userlevel
        ) 
        self.token = jwt.encode({"id" : self.user.id}, SECRET_KEY, algorithm='HS256')

    def tearDown(self):
        User.objects.all().delete()
        RoomOption.objects.all().delete()
        Room.objects.all().delete()
        StaytypeImage.objects.all().delete()
        Facility.objects.all().delete()
        StaytypeFacility.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()

    @patch("reviews.views.boto3.client")
    def test_reviews_post_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        header = {"HTTP_Authorization" : self.token}

        review = {
            "room_id" : 1,
            "rating"  : 4,
            "comment" : "test_comment",
            "image"   : test_image
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/stays/1/reviews", review, **header)
        self.assertEqual(response.json(), {"message" : "CREATED"})
        self.assertEqual(response.status_code, 201)

    @patch("reviews.views.boto3.client")
    def test_reviews_post_invalid_room_failed(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        header = {"HTTP_Authorization" : self.token}

        review = {
            "room_id" : 10000,
            "rating"  : 4,
            "comment" : "test_comment",
            "image"   : test_image
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/stays/1/reviews", review, **header)
        self.assertEqual(response.json(), {"message" : "INVALID_ROOM"})
        self.assertEqual(response.status_code, 400)
    
    @patch("reviews.views.boto3.client")
    def test_reviews_post_invalid_rate_number_failed(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        header = {"HTTP_Authorization" : self.token}

        review = {
            "room_id" : 1,
            "rating"  : 10,
            "comment" : "test_comment",
            "image"   : test_image
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/stays/1/reviews", review, **header)
        self.assertEqual(response.json(), {"message" : "INVALID_RATE_NUMBER"})
        self.assertEqual(response.status_code, 400)

    @patch("reviews.views.boto3.client")
    def test_reviews_post_image_does_not_exist_failed(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        header = {"HTTP_Authorization" : self.token}

        review = {
            "room_id" : 1,
            "rating"  : 4,
            "comment" : "test_comment"
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/stays/1/reviews", review, **header)
        self.assertEqual(response.json(), {"message" : "IMAGE_DOES_NOT_EXIST"})
        self.assertEqual(response.status_code, 400)
