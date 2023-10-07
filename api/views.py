from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

from rest_framework import generics
from .serializers import PersonSerializer
from .models import Person

from datetime import datetime

import cv2
import threading


@gzip.gzip_page
def main(request):
    #    try:
    #        cam = VideoCamera(urls[1])
    #        return StreamingHttpResponse(
    #            gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
    #        )
    #    except:
    #        pass

    return render(request, "main.html")


class PersonView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
