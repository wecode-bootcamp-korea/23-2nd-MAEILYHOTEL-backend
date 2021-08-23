import json, jwt

from django.http.response import JsonResponse

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
