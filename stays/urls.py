from django.urls import path

from stays.views import RoomView

urlpatterns = [
    path('/room/<int:room_id>', RoomView.as_view()),
]