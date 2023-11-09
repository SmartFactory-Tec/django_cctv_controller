from django.shortcuts import render
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.http import JsonResponse

from rest_framework import generics

from api.scripts.people_utils import (
    serialize_person_record,
    serialize_person_records,
    create_person_record,
    update_person_record,
    delete_person_record,
)
from api.scripts.camera_utils import (
    serialize_camera_record,
    serialize_camera_records,
    create_camera_record,
    update_camera_record,
    delete_camera_record,
)
from api.serializers import PersonSerializer
from api.serializers import CameraSerializer
from api.models import Person, Camera

import json


@gzip.gzip_page
def main(request):
    return render(request, "main.html")


@csrf_exempt
def camera_request_handler(request, record_id=None):
    if request.method == "GET":
        if record_id is not None:
            try:
                record = Camera.objects.get(camera_id=record_id)
                serialized_record = serialize_camera_record(record)
                return JsonResponse({"data": serialized_record}, status=200)
            except Camera.DoesNotExist:
                return JsonResponse(
                    {"error": f"Record with id {record_id} does not exist"}, status=404
                )
        else:
            all_records = Camera.objects.all()
            serialized_records = serialize_camera_records(all_records)
            return JsonResponse({"data": serialized_records}, status=200)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            new_record = create_camera_record(data)
            new_record.save()
            return JsonResponse({"message": "Record created successfully."}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            update_camera_record(record_id, data)
            return JsonResponse({"message": "Record updated successfully."}, status=200)
        except Camera.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "DELETE":
        try:
            delete_camera_record(record_id)
            return JsonResponse({"message": "Record deleted successfully."}, status=200)
        except Camera.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )

    else:
        return JsonResponse({"message": "Method not allowed."}, status=405)


@csrf_exempt
def people_request_handler(request, record_id=None):
    if request.method == "GET":
        if record_id is not None:
            try:
                record = Person.objects.get(id=record_id)
                return JsonResponse(
                    {"data": serialize_person_record(record)}, status=200
                )
            except Person.DoesNotExist:
                return JsonResponse(
                    {"error": f"Record with id {record_id} does not exist"}, status=404
                )
        else:
            return JsonResponse(
                {"data": serialize_person_records(Person.objects.all())}, status=200
            )

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            new_record = create_person_record(data)
            return JsonResponse({"message": "Record created successfully."}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            update_person_record(record_id, data)
            return JsonResponse({"message": "Record updated successfully."}, status=200)
        except Person.DoesNotExist:
            return JsonResponse(
                {"error": f"Record with id {record_id} does not exist"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided"}, status=400)

    elif request.method == "DELETE":
        try:
            delete_person_record(record_id)
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
