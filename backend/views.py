from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import cv2
from PIL import Image
import numpy as np


def sketchProcess(request):
    file_list = request.FILES.getlist('file')
    fileData = file_list[0].read()
    img = Image.open(BytesIO(fileData))
    print(img)
    return HttpResponse("Hello, world!")