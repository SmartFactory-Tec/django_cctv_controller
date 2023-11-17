from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    tec_id = models.CharField(max_length=50, unique=True)
    major = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Camera(models.Model):
    camera_id = models.IntegerField(unique=True)
    camera_url = models.CharField(max_length=500, blank=True)
    password = models.CharField(null=True, max_length=500)
    camera_name = models.CharField(null=True, max_length=500, unique=True)
    camera_location = models.CharField(null=True, max_length=500)
    camera_status = models.CharField(null=True, max_length=500)

    def __str__(self):
        return f"{self.camera_id} - {self.camera_name} - {self.camera_url}"
