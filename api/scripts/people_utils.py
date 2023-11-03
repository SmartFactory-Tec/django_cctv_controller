from django.http import JsonResponse
import json


def serialize_person_record(record):
    return {
        "id": record.id,
        "first_name": record.first_name,
        "last_name": record.last_name,
        "email": record.email,
        "tec_id": record.tec_id,
        "major": record.major,
        "phone_number": record.phone_number,
        "created_at": record.created_at,
    }


def serialize_person_records(records):
    return [serialize_person_record(record) for record in records]


def create_person_record(data):
    return Person.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        tec_id=data["tec_id"],
        major=data["major"],
        phone_number=data["phone_number"],
    )


def update_person_record(record_id, data):
    record = Person.objects.get(id=record_id)
    record.first_name = data["first_name"]
    record.last_name = data["last_name"]
    record.email = data["email"]
    record.tec_id = data["tec_id"]
    record.major = data["major"]
    record.phone_number = data["phone_number"]
    record.save()


def delete_person_record(record_id):
    record = Person.objects.get(id=record_id)
    record.delete()
