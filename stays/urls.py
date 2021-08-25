from django.urls import path

from stays.views   import StaytypeListView, StayView, StayCalendarView, StayRoomsView
from reviews.views import ReviewAvailableView, ReviewsView

urlpatterns = [
    path('', StaytypeListView.as_view()),
    path('/<int:stay_id>', StayView.as_view()),
    path('/<int:stay_id>/calendar', StayCalendarView.as_view()),
    path('/<int:stay_id>/rooms', StayRoomsView.as_view()),
    path('/<int:stay_id>/reviews', ReviewsView.as_view()),
    path('/<int:stay_id>/reviewsavailable', ReviewAvailableView.as_view()),
]
