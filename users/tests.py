import json, jwt

from users.models     import User, UserLevel

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock
from my_settings   import SECRET_KEY

class KaKaoSignInTest(TestCase):
    def setUp(self):
        UserLevel.objects.create(name='silver', discount=0)

    def tearDown(self):
        User.objects.all().delete()
        UserLevel.objects.all().delete()
    
    @patch("users.views.requests")
    def test_kakao_signin_new_user_success(self, mocked_requests):
        class KaKaoResponse:
            def json(self):
                return {
					"id"           : 1234567,
					"kakao_account": { 
					        "profile" : {"nickname": "가나다"},
					        "email"   : "sample@sample.com"
                            }
                }
            status_code = 200

        client = Client()
        mocked_requests.get = MagicMock(return_value = KaKaoResponse())
        headers = {"HTTP_Authorization": "가짜 토큰"}
        response = client.post('/users/kakao', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        token = response.json()['token']
        user  = jwt.decode(token, SECRET_KEY, algorithms='HS256')['id']
        kakao_id = User.objects.get(id=user).kakao_id

        self.assertEqual(kakao_id, '1234567')

class ProfileGETTest(TestCase):
    def setUp(self):
        userlevel = UserLevel.objects.create(name='silver', discount=0)
        self.user = User.objects.create(
                    kakao_id  = 12341234,
                    email     = 'email',
                    nickname  = 'nickname',
                    point     = 1000000,
                    userlevel = userlevel)
        self.token = jwt.encode({"id" : self.user.id}, SECRET_KEY, algorithm = 'HS256')

    def tearDown(self):
        User.objects.all().delete()
        UserLevel.objects.all().delete()
    
    def test_user_profile_get_success(self):
        client = Client()
        headers = {"HTTP_Authorization": self.token}
        response = client.get('/users/profile', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                        "name"      : self.user.nickname,
                        "userlevel:": self.user.userlevel.name,
                        "discount"  : self.user.userlevel.discount,
                        "point"     : "{:.2f}".format(self.user.point,2),
                        "email"     : self.user.email,
                        "agreement" : self.user.agreement,
                        })

class UserLevelTest(TestCase):
    def setUp(self):
        self.userlevel1 = UserLevel.objects.create(
            id = 1, name = "silver", discount = 0.1
        )
        self.userlevel2 = UserLevel.objects.create(
            id = 2, name = "gold", discount = 0.2
        )
        self.user = User.objects.create(
            id           = 1,
            nickname     = "nickname",
            email        = "email@email.com",
            point        = 100000,
            kakao_id     = "1234567",
            userlevel_id = 1
        ) 
        self.token = jwt.encode({"id" : self.user.id}, SECRET_KEY, algorithm='HS256')

    def tearDown(self):
        UserLevel.objects.all().delete()
        User.objects.all().delete()

    def test_userlevelview_patch_success(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        request  = {"userlevel" : 2, "agreement" : "True"}
        response = client.patch('/users/level', json.dumps(request), **header, content_type='application/json')
        
        self.user.refresh_from_db()
        self.assertEqual(response.json(), 
            {
                "id"        : self.user.userlevel.id,
                "agreement" : self.user.agreement
            }
        )
        self.assertEqual(response.status_code, 200)   

    def test_userlevelview_patch_invalid_request_failed(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        request  = {"userlevel" : 1, "agreement" : "True"}
        response = client.patch('/users/level', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.json(), {"message" : "INVALID_REQUEST"})
        self.assertEqual(response.status_code, 400)

    def test_userlevelview_patch_key_error_failed(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        request  = {"userlevellll" : 2, "agreement" : "True"}
        response = client.patch('/users/level', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

