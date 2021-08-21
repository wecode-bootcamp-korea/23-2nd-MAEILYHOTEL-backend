from django.urls import path, include

urlpatterns = [
    path('stays', include('stays.urls')),
]