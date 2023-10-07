from django.urls import path, include
from .views import PersonView, main

urlpatterns = [
    path('', PersonView.as_view()),
    path('video/', main)
]
