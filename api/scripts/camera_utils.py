from django.http import JsonResponse
from api.models import Camera
import json


def serialize_camera_record(record):
    return {
        "camera_id": record.camera_id,
        "camera_location": record.camera_location,
        "camera_name": record.camera_name,
        "camera_url": record.camera_url,
        "camera_status": record.camera_status,
    }


def serialize_camera_records(records):
    return [serialize_camera_record(record) for record in records]


def create_camera_record(data):
    return Camera.objects.create(
        camera_id=data["camera_id"],
        camera_location=data["camera_location"],
        camera_name=data["camera_name"],
        camera_url=data["camera_url"],
    )


def update_camera_record(record_id, data):
    record = Camera.objects.get(camera_id=record_id)
    if "camera_location" in data:
        record.camera_location = data["camera_location"]
    if "camera_name" in data:
        record.camera_name = data["camera_name"]
    if "camera_url" in data:
        record.camera_url = data["camera_url"]
    if "camera_status" in data:
        record.camera_status = data["camera_status"]
    record.save()


def delete_camera_record(record_id):
    record = Camera.objects.get(camera_id=record_id)
    record.delete()
