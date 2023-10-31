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


@csrf_exempt
def people_request_handler(request, record_id=None):
    print(f"Handling request: {str(request)} at {datetime.now()}")

    if request.method == "GET":
        if record_id is not None:
            try:
                record = Person.objects.get(id=record_id)

                serialized_record = {
                    "id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "email": record.email,
                    "tec_id": record.tec_id,
                    "major": record.major,
                    "phone_number": record.phone_number,
                    "created_at": record.created_at,
                }

                return JsonResponse({"data": serialized_record}, status=200)
            except Person.DoesNotExist:
                return JsonResponse(
                    {"error": f"Record with id {record_id} does not exist"}, status=404
                )

        else:
            all_records = Person.objects.all()

            serialized_records = [
                {
                    "id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "email": record.email,
                    "tec_id": record.tec_id,
                    "major": record.major,
                    "phone_number": record.phone_number,
                    "created_at": record.created_at,
                }
                for record in all_records
            ]

            return JsonResponse({"data": serialized_records}, status=200)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            new_record = Person.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                tec_id=data["tec_id"],
                major=data["major"],
                phone_number=data["phone_number"],
            )

            new_record.save()

            return JsonResponse({"message": "Record created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)

            record = Person.objects.get(id=record_id)
            
            record.first_name = data["first_name"]
            record.last_name = data["last_name"]
            record.email = data["email"]
            record.tec_id = data["tec_id"]
            record.major = data["major"]
            record.phone_number = data["phone_number"]

            record.save()

            return JsonResponse({"message": "Record updated successfully."}, status=200)

        except Person.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "DELETE":
        try:
            record = Person.objects.get(id=record_id)
            record.delete()

            return JsonResponse({"message": "Record deleted successfully."}, status=200)

        except Person.DoesNotExist:
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
