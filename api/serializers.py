from rest_framework import serializers
from .models import Person, Camera


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "tec_id", "created_at")


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "camera_id",
            "camera_url",
            "password",
            "camera_name",
            "camera_location",
        )
