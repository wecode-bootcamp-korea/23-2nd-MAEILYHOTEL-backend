import jwt

from django.test import TestCase, Client

from stays.models import Category, Staytype, Room, RoomOption, StaytypeImage
from users.models import User, UserLevel
from books.models import Book

from my_settings import SECRET_KEY
from datetime    import date, time

class BookListsTest(TestCase):
    def setUp(self):
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
        staytype_image = StaytypeImage.objects.create(image_url='url',staytype=staytype)
        room        = Room.objects.create(id = 1, name="Aroom", quantity=10, image_url="url", people=2, staytype=staytype)
        room_option = RoomOption.objects.create(id = 1, name="숙박", price=10000, check_in=time(15,00) ,check_out=time(11,00), room=room)

        userlevel = UserLevel.objects.create(name='silver', discount=0)
        user      = User.objects.create(
                    id        = 1,
                    kakao_id  = 12341234,
                    email     = 'email',
                    nickname  = 'nickname',
                    point     = 1000000,
                    userlevel = userlevel)
        check_in  = date(2021,8,1)
        check_out = date(2021,8,3)
        Book.objects.create(
            check_in    = check_in,
            check_out   = check_out,
            room        = room,
            room_option = room_option,
            user        = user
        )
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = 'HS256')
        
    def tearDown(self):
        RoomOption.objects.all().delete()
        Room.objects.all().delete()
        StaytypeImage.objects.all().delete()
        Staytype.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        UserLevel.objects.all().delete()

    def test_book_lists_view_get_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization": self.token}
        response = client.get('/books/list', **headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [{
                        "stay_id"  : 1,
                        "stay_name": "Ahotel",
                        "stay_img" : "url",
                        "room_id"  : 1,
                        "room_name": "Aroom",
                        "check_in" : "2021-08-01",
                        "check_out": "2021-08-03"}])
