from django.shortcuts import render
from django.http import HttpResponse
import cv2
from .utils import process
from .utils import models
import numpy as np
import torch
from PIL import Image
from io import BytesIO
import base64

def sketchProcess(request):
    '''
    Get the uploaded image and convert it to sketch, then return the sketch.
    :param request: include the uploaded image
    :return: the sketch generated according to the original image
    '''
    if request.method == 'POST':
        # Read the image and save it to lacal
        file_list = request.FILES.getlist('file')
        file = file_list[0]
        path = "./backend/utils/imgDir/"
        img_name = "origin.png"
        img_dir = path + img_name
        data = file.file.read()
        with open(img_dir, 'wb') as f:
            f.write(data)

        # Initialize config
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        with torch.no_grad():
            netC2S = models.Color2Sketch(input_nc=3,
                                         output_nc=1,
                                         norm='IN',
                                         SN=True,
                                         activation='relu',
                                         residual=False,
                                         ckpt_path='./backend/utils/checkpoint/color2sketch.pth').to(device)
            netS2C = models.Colorizenet(input_nc=4,
                                        output_nc=3,
                                        norm='IN',
                                        SN=True,
                                        activation='relu',
                                        residual=True,
                                        ckpt_path='./backend/utils/checkpoint/sketch2color.pth').to(device)

            netC2S.eval()
            netS2C.eval()

        # Iamge process
        img = cv2.imread(img_dir, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_AREA)
        with torch.no_grad():
            img_ = process.ForwardNet(img, netC2S, device)
        img_ = img_ * 255
        img_ = img_.astype(np.uint8)
        img_ = np.broadcast_to(img_, img.shape)

        # Save sketch
        img_name_ = "sketch.png"
        img_dir_ = path + img_name_
        img_ = Image.fromarray(img_)
        img_.save(img_dir_)

        # Generate stream
        stream = BytesIO()
        img_.save(stream, "png")
        data = stream.getvalue()
        data = base64.b64encode(data).decode()

    return HttpResponse(data, content_type='image/png')


def colorization(request):
    '''
    Get the sketch and convert it to colored image, then return.
    :param request: include the sketch
    :return: the image generated according to the original sketch
    '''
    if request.method == 'POST':
        # Read the hint and save it to lacal
        file = request.POST.get('hint')
        data = file.split(",")[-1]
        data = base64.b64decode(data)
        path = "./backend/utils/imgDir/"
        img_name = "hint.png"
        img_dir = path + img_name
        with open(img_dir, 'wb') as f:
            f.write(data)

        # Initialize config
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        with torch.no_grad():
            netS2C = models.Colorizenet(input_nc=4,
                                        output_nc=3,
                                        norm='IN',
                                        SN=True,
                                        activation='relu',
                                        residual=True,
                                        ckpt_path='./backend/utils/checkpoint/sketch2color.pth').to(device)
            netS2C.eval()

        # Iamge process
        hint = cv2.imread(path + 'hint.png', cv2.IMREAD_COLOR)
        hint = cv2.cvtColor(hint, cv2.COLOR_BGR2RGB)
        sketch = cv2.imread(path + 'sketch.png', cv2.IMREAD_GRAYSCALE).reshape(512, 512, 1)
        input_array = np.concatenate([sketch, hint], axis=2)
        with torch.no_grad():
            result = process.ForwardNet(input_array, netS2C, device)
        result = result * 255
        result = result.astype(np.uint8)

        # Save result
        result_dir = path + "result.png"
        result = Image.fromarray(result)
        result.save(result_dir)

        # Generate stream
        stream = BytesIO()
        result.save(stream, "png")
        data = stream.getvalue()
        data = base64.b64encode(data).decode()

    return HttpResponse(data, content_type='image/png')