import json, jwt

from django.http.response import JsonResponse

from users.models     import User, UserLevel

from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
from my_settings import SECRET_KEY

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
        headers = {"Authorization": "가짜 토큰"}
        response = client.post('/users/kakao', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        token = response.json()['token']
        user  = jwt.decode(token, SECRET_KEY, algorithms='HS256')['id']
        kakao_id = User.objects.get(id=user).kakao_id

        self.assertEqual(kakao_id, '1234567')
