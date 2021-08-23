import json

from django.test import TestCase, Client
from datetime    import time, date

from stays.models import *
from users.models import User, UserLevel
from books.models import Book

class StaytypeListTest(TestCase):
    def setUp(self):
        category = Category.objects.create(id = 1, name="호텔")
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
                name      = "스위트룸",
                quantity  = 4,
                image_url = "url",
                people    = 2,
                staytype  = staytype
            )
        
        room_option = RoomOption.objects.create(
                name      = "숙박",
                price     = 100000,
                check_in  = time(15,00),
                check_out = time(12,00),
                room      = room
            )

        userlevel = UserLevel.objects.create(name="name",discount=0.2)

        user = User.objects.create(
            nickname  = "nickname",
            email     = "email@email.com",
            kakao_id  = "kakao_id",
            userlevel = userlevel
        )

        Book.objects.create(
            user        = user,
            room        = room,
            room_option = room_option,
            check_in    = date(2021,7,31),
            check_out   = date(2021,8,5)
        )

        Book.objects.create(
            user        = user,
            room        = room,
            room_option = room_option,
            check_in    = date(2021,8,2),
            check_out   = date(2021,8,5)
        )

        Book.objects.create(
            user        = user,
            room        = room,
            room_option = room_option,
            check_in    = date(2021,8,1),
            check_out   = date(2021,8,3)
        )

        Book.objects.create(
            user        = user,
            room        = room,
            room_option = room_option,
            check_in    = date(2021,7,30),
            check_out   = date(2021,7,31)
        )

    def tearDown(self):
        Book.objects.all().delete()
        UserLevel.objects.all().delete()
        User.objects.all().delete()
        RoomOption.objects.all().delete()
        Room.objects.all().delete()
        StaytypeImage.objects.all().delete()
        Facility.objects.all().delete()
        StaytypeFacility.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()

    def test_staytypelist_get_success(self):
        client   = Client()
        response = client.get(f"/stays?category=1&location=강릉시&CheckIn=2021-08-01&CheckOut=2021-08-04")
        self.assertEqual(response.json(),
            {
                "staylist" : [{
                    "id"        : 1,
                    "name"      : "강릉호텔",
                    "image_url" : "url",
                    "price"     : 100000        
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_staytypelist_not_input_date_failed(self):
        client   = Client()
        response = client.get('/stays')
        self.assertEqual(response.json(),
        {"message":"INVALID_DATE"}
        )
        self.assertEqual(response.status_code, 400)

class StaysViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="호텔")
        staytype = Staytype.objects.create(
            id          = 1,
            name        = "Ahotel",
            address     = "testaddress",
            longitude   = 111.111,
            latitude    = 111.111,
            description = "설명입니다",
            category    = category
            )
        facility = Facility.objects.create(name="Facility")
        StaytypeFacility.objects.create(facility=facility,staytype=staytype)        
        StaytypeImage.objects.create(image_url="url",staytype=staytype)
        room = Room.objects.create(name="Aroom",quantity=10,image_url="url",people=2,staytype=staytype)
        RoomOption.objects.create(name="숙박", price=10000, check_in=time(15,00) ,check_out=time(11,00), room=room)
        
    def tearDown(self):
        RoomOption.objects.all().delete()
        Room.objects.all().delete()
        StaytypeImage.objects.all().delete()
        StaytypeFacility.objects.all().delete()
        Facility.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()

    def test_staydetailview_get_success(self):
        client   = Client()
        response = client.get(f'/stays/1')
        self.assertEqual(response.json(),
        {
            "category": "호텔",
            "name": "Ahotel",
            "images": [
                "url"
            ],
            "total_rooms": 10,
            "facilities": [
                "Facility"
            ],
            "address": "testaddress",
            "long": "111.1110000",
            "lat": "111.1110000",
            "description": "설명입니다",
            "check_in": "15:00:00",
            "check_out": "11:00:00"
        }
                )
        self.assertEqual(response.status_code, 200)
    
    def test_staydetailview_invalid_id_failed(self):
        client   = Client()
        response = client.get('/stays/50')
        self.assertEqual(response.status_code, 404)

class StayCalendarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="호텔")
        staytype = Staytype.objects.create(
            id          = 1,
            name        = "Ahotel",
            address     = "testaddress",
            longitude   = 111.111,
            latitude    = 111.111,
            description = "설명입니다",
            category    = category
            )
        room = Room.objects.create(name="Aroom",quantity=10,image_url="url",people=2,staytype=staytype)
        RoomOption.objects.create(name="숙박", price=10000, check_in=time(15,00) ,check_out=time(11,00), room=room)
        cls.stay_id = staytype.id
        
    def tearDown(self):
        RoomOption.objects.all().delete()
        Room.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()

    def test_stay_calendar_view_get_success(self):
        client   = Client()
        response = client.get(f'/stays/1/calendar?Date=2021-08-23')
        self.assertEqual(response.json(),
        {
            "result": {
                "2021-08-23": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-08-24": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-08-25": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-08-26": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-08-27": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-08-28": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-08-29": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-08-30": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-08-31": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-01": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-02": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-03": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-04": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-05": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-06": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-07": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-08": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-09": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-10": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-11": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-12": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-13": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-14": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-15": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-16": {
                    "price": 10000.0,
                    "quantity": 10
                },
                "2021-09-17": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-18": {
                    "price": 13000.0,
                    "quantity": 10
                },
                "2021-09-19": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-20": {
                    "price": 7000.0,
                    "quantity": 10
                },
                "2021-09-21": {
                    "price": 10000.0,
                    "quantity": 10
                }
            }
        }
                )
        self.assertEqual(response.status_code, 200)
    
    def test_stay_calendar_view_invalid_id_failed(self):
        client   = Client()
        response = client.get('/stays/100/calendar?Date=2021-08-23')
        self.assertEqual(response.status_code, 404)

    def test_stay_calendar_view_invalid_date_failed(self):
        client   = Client()
        response = client.get('/stays/1/calendar')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message":"INVALID_DATE"})

