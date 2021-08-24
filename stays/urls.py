from django.urls import path

from stays.views import StaytypeListView, StayView, StayCalendarView, StayRoomsView

urlpatterns = [
    path('', StaytypeListView.as_view()),
    path('/<int:stay_id>', StayView.as_view()),
    path('/<int:stay_id>/calendar', StayCalendarView.as_view()),
    path('/<int:stay_id>/rooms', StayRoomsView.as_view())
]
