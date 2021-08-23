from django.urls import path
from users.views import KaKaoSignInView, ProfileView, UserLevelView

urlpatterns = [
    path('/kakao', KaKaoSignInView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/level', UserLevelView.as_view()),
]
