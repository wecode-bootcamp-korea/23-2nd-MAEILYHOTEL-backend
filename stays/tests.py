import json

from django.test import TestCase, Client
from datetime    import time

from stays.models import *

class StaysViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="호텔")
        staytype = Staytype.objects.create(
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
        response = client.get('/stays/1')
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

