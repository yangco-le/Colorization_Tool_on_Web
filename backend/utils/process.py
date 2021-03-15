import torch
import numpy as np
import cv2

def NumpyToTensor(array):
    # handle numpy array
    img = torch.from_numpy(array.transpose((2, 0, 1)))
    # backward compatibility
    if isinstance(img, torch.ByteTensor) or img.dtype==torch.uint8:
        return img.float().div(255)
    else:
        return img

def TensorToNumpy(tensor):
    array = np.transpose(tensor.detach().cpu().numpy(), (1,2,0))
    
    return array

def QPixmapToNumpy(pixmap):
    ## Get the size of the current pixmap
    size = pixmap.size()
    h = size.width()
    w = size.height()
    channels_count = 4

    ## Get the QImage Item and convert it to a byte string
    qimg = pixmap.toImage().convertToFormat(13)
    ptr = qimg.bits()
    ptr.setsize(h * w * 3)
    array = np.frombuffer(ptr, np.uint8).reshape((h, w, 3)).copy()
    
    return array

# def NumpyToPixmap(array):
#     array = array.copy()
#     if len(array.shape) == 2: # It has single channel (grayscaled)
#         array = np.broadcast_to(array.shape[0], array.shape[1], 3)
#     height, width, channel = array.shape
#     bytesPerLine = 3 * width
#     qimg = QImage(array.data, width, height, bytesPerLine, QImage.Format_RGB888)
#     pixmap = QPixmap.fromImage(qimg)
#
#     return pixmap

def ForwardNet(input_array, net, device):
    with torch.no_grad():
        input_tensor = NumpyToTensor(input_array).unsqueeze(0).to(device)
        output_tensor = net(input_tensor)
        output_tensor = output_tensor.squeeze(0).cpu()
    output_array = TensorToNumpy(output_tensor)
    
    return output_array

def XDoG(img, sigma = 0.8, k = 3.0, t = 0.998, e = -0.1, p = 30):
    img = img.astype(np.float32)/255

    Ig1 = cv2.GaussianBlur(img, (3, 3), sigma, sigma)
    Ig2 = cv2.GaussianBlur(img, (3, 3), sigma * k, sigma * k)

    Dg = (Ig1 - t * Ig2)

    Dg[Dg<e] = 1
    Dg[Dg>=e]= 1 + np.tanh(p * Dg[Dg>=e])

    Dg[Dg>1.0] = 1.0
    Dg = Dg * 255
    Dg = Dg.astype(np.uint8)
    
    return Dg


