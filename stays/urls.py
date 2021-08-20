from django.urls import path
from stays.views import StaytypeListView, StayView

urlpatterns = [
    path('', StaytypeListView.as_view()),
    path('/<int:stay_id>', StayView.as_view()),
]
