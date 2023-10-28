from django.urls import path, include
from .views import PersonView, CameraView, main

urlpatterns = [
    path("", PersonView.as_view()),
    path("video/", main),
    path("cameras_overview/", CameraView.as_view()),
]
