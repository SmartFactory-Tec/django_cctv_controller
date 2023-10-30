from django.shortcuts import render
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.http import JsonResponse

from rest_framework import generics
from api.serializers import PersonSerializer
from api.serializers import CameraSerializer
from api.models import Person, Camera

from datetime import datetime

import cv2
import threading
import json


@gzip.gzip_page
def main(request):
    return render(request, "main.html")


@csrf_exempt
def camera_request_handler(request, record_id=None):
    print(f"Handling request: {str(request)} at {datetime.now()}")
    print(record_id)

    if request.method == "GET":
        if record_id is not None:
            try:
                record = Camera.objects.get(camera_id=record_id)

                serialized_record = {
                    "camera_id": record.camera_id,
                    "camera_location": record.camera_location,
                    "camera_name": record.camera_name,
                    "camera_url": record.camera_url,
                }

                return JsonResponse({"data": serialized_record}, status=200)
            except Camera.DoesNotExist:
                return JsonResponse(
                    {"error": f"Record with id {record_id} does not exist"}, status=404
                )

        else:
            all_records = Camera.objects.all()

            serialized_records = [
                {
                    "camera_id": record.camera_id,
                    "camera_location": record.camera_location,
                    "camera_name": record.camera_name,
                    "camera_url": record.camera_url,
                }
                for record in all_records
            ]

            return JsonResponse({"data": serialized_records}, status=200)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            new_record = Camera.objects.create(
                camera_id=data["camera_id"],
                camera_location=data["camera_location"],
                camera_name=data["camera_name"],
                camera_url=data["camera_url"],
            )

            new_record.save()

            return JsonResponse({"message": "Record created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)

            record = Camera.objects.get(camera_id=record_id)
            record.camera_location = data["camera_location"]
            record.camera_name = data["camera_name"]
            record.camera_url = data["camera_url"]

            record.save()

            return JsonResponse({"message": "Record updated successfully."}, status=200)

        except Camera.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "DELETE":
        try:
            record = Camera.objects.get(camera_id=record_id)
            record.delete()

            return JsonResponse({"message": "Record deleted successfully."}, status=200)

        except Camera.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )

    else:
        return JsonResponse({"message": "Method not allowed."}, status=405)


class PersonView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CameraView(generics.ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
