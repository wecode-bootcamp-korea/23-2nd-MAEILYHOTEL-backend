from django.urls import path

from stays.views import StayView

urlpatterns = [
    path('/<int:stay_id>', StayView.as_view()),
]