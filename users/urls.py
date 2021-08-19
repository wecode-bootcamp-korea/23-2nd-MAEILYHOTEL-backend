from django.urls import path

from users.views import KaKaoSignInView

urlpatterns = [
    path('/kakao', KaKaoSignInView.as_view()),
]
