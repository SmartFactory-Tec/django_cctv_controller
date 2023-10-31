from django.urls import path, include
from .views import PersonView, CameraView, main, camera_request_handler, people_request_handler

urlpatterns = [
    path("", PersonView.as_view()),
    path("video/", main),
    path("cameras_overview/", CameraView.as_view()),

    path("cameras/", camera_request_handler, name="camera_handler"),
    path(
        "cameras/<int:record_id>/",
        camera_request_handler,
        name="camera_handler_with_id",
    ),

    path("people/", people_request_handler, name="people_handler"),
    path(
        "people/<int:record_id>/",
        people_request_handler,
        name="people_handler_with_id",
    ),
]
