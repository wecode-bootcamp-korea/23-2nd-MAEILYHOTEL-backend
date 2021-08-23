from django.urls import path
from users.views import KaKaoSignInView, ProfileView

urlpatterns = [
    path('/kakao', KaKaoSignInView.as_view()),
    path('/profile', ProfileView.as_view()),
]