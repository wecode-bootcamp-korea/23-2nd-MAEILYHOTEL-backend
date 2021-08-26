import json, jwt, requests

from django.views import View
from django.http  import JsonResponse

from users.models import User, UserLevel
from my_settings  import SECRET_KEY
from users.utils  import login_decorator

class KaKaoSignInView(View):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization')    
            profile_response = requests.get(    
                "https://kapi.kakao.com/v2/user/me",
                headers = {"Authorization" : f"Bearer {access_token}"},
                timeout = 3
            )
            
            if not profile_response.status_code == 200:
                return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

            profile_json  = profile_response.json()
            kakao_id      = profile_json.get("id")
            kakao_account = profile_json.get("kakao_account")

            kakao_profile = kakao_account.get("profile")
            email         = kakao_account.get("email")
            nickname      = kakao_profile.get("nickname")           

            user, created = User.objects.get_or_create(
                    kakao_id  = kakao_id,
                    defaults = {
                        'email'    : 'email',
                        'nickname' : 'nickname',
                        'point'    : 1000000,
                        'userlevel': UserLevel.objects.get(name='silver')
                    }
                )
            user.email    = email
            user.nickname = nickname
            user.save()
            token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({"token" : token}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

class ProfileView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        return JsonResponse({
            "name"      : user.nickname,
            "userlevel" : user.userlevel.name,
            "discount"  : user.userlevel.discount,
            "point"     : user.point,
            "email"     : user.email,
            "agreement" : user.agreement,
            }, status = 200)


class UserLevelView(View):
    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            if (data["agreement"] == True and data["userlevel"] == "silver") or \
                (data["agreement"] == False and data["userlevel"] == "gold"):
                return JsonResponse({"message" : "INVALID_REQUEST"}, status = 400)

            if not UserLevel.objects.filter(name = data["userlevel"]).exists():
                return JsonResponse({"message" : "INVALID_LEVEL_NAME"}, status = 400)

            request.user.agreement = data["agreement"]
            request.user.userlevel = UserLevel.objects.get(name=data["userlevel"])
            request.user.save()

            data = {
                "userlevel" : request.user.userlevel.name,
                "agreement" : request.user.agreement
            }
            
            return JsonResponse(data, status = 200)
            
        except:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
