from rest_framework import serializers
from .models import Person, Camera


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "email",
            "tec_id",
            "major",
            "phone_number",
            "created_at",
        )


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
