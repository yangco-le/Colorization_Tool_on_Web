import torch
import torch.nn as nn
import os, sys
from torchvision import models
from torch.nn.utils import spectral_norm

# Conv. block
class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, bias=False, 
                 norm=None, SN=False, activation='relu', residual=False):
        super().__init__()
        # Convolution
        if SN:
            self.conv = spectral_norm(nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=bias))
        else:
            self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=bias)

        # Normalization
        self.norm = norm
        if norm=='BN':
            self.norm = nn.BatchNorm2d(out_channels)
        elif norm=='GN':
            self.norm = nn.GroupNorm(32, out_channels)
        elif norm=='IN':
            self.norm = nn.InstanceNorm2d(out_channels)  
        elif norm is None:
            self.norm= nn.Identity()
            
        # Activation
        if activation=='relu':
            self.activation = nn.ReLU(inplace=True)
        elif activation=='lrelu':
            self.activation = nn.LeakyReLU(0.2, inplace=True)
        elif activation=='tanh':
            self.activation = nn.Tanh()
        elif activation=='sigmoid':
            self.activation = nn.Sigmoid()
        elif activation is None:
            self.activation = nn.Identity() 
            
        # Residual
        self.residual = residual
    
    def forward(self, inputs):
        # Get input
        x = inputs
        
        # Convolution
        x = self.conv(x)
        
        # Normalization
        x = self.norm(x)
        
        # Residual Connection
        if self.residual:
            x = inputs + x
            
        # Activation
        x = self.activation(x)

        return x
    
class Encoder(nn.Module):
    def __init__(self, input_nc, norm, SN, activation):
        super(Encoder, self).__init__()
        # Build ResNet and change first conv layer to accept single-channel input
        self.layer1 = ConvBlock(in_channels=input_nc, 
                                out_channels=64,
                                kernel_size=3,
                                stride=2,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual= False)
        
        self.layer2 = ConvBlock(in_channels=64, 
                                out_channels=128,
                                kernel_size=3,
                                stride=2,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual= False)
        
        self.layer3 = ConvBlock(in_channels=128, 
                                out_channels=256,
                                kernel_size=3,
                                stride=2,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual= False)
        
        self.layer4 = ConvBlock(in_channels=256, 
                                out_channels=512,
                                kernel_size=3,
                                stride=2,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual= False)

    def forward(self, input_image):
        # Pass input through ResNet-gray to extract features
        x0 = input_image # nc * 256 * 256 
        x1 = self.layer1(x0) # 64 * 128 * 128 
        x2 = self.layer2(x1) # 128 * 64 * 64
        x3 = self.layer3(x2) # 256 * 32 * 32 
        x4 = self.layer4(x3) # 512 * 16 * 16 

        return (x1, x2, x3), x4
    
class Middle(nn.Module):
    def __init__(self, input_nc, norm, SN, activation, residual):
        super(Middle, self).__init__()
        # Build ResNet and change first conv layer to accept single-channel input
        self.layer1 = ConvBlock(in_channels=input_nc, 
                                out_channels=input_nc,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=residual)
        
        self.layer2 = ConvBlock(in_channels=input_nc, 
                                out_channels=input_nc,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=residual)
        
        self.layer3 = ConvBlock(in_channels=input_nc, 
                                out_channels=input_nc,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=residual)
        
        self.layer4 = ConvBlock(in_channels=input_nc, 
                                out_channels=input_nc,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=residual)

    def forward(self, input_image):
        # Pass input through ResNet-gray to extract features
        x = input_image 
        x = self.layer1(x) 
        x = self.layer2(x) 
        x = self.layer3(x) 
        x = self.layer4(x) 

        return x   

class Decoder(nn.Module):
    def __init__(self, output_nc, norm, SN, activation):
        super(Decoder, self).__init__()
        # Convolutional layers and upsampling     
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)

        self.layer4 = ConvBlock(in_channels=512, 
                                out_channels=256,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=False)

        self.layer3 = ConvBlock(in_channels=512, 
                                out_channels=128,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=False)

        self.layer2 = ConvBlock(in_channels=256, 
                                out_channels=64,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=False)

        self.layer1 = ConvBlock(in_channels=128, 
                                out_channels=64,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=norm,
                                SN=SN,
                                activation=activation,
                                residual=False)

        self.layer0 = ConvBlock(in_channels=64, 
                                out_channels=output_nc,
                                kernel_size=3,
                                stride=1,
                                padding=1,
                                norm=None,
                                SN=SN,
                                activation='sigmoid',
                                residual=False)

    def forward(self, skip_connection, inputs): 
        x1, x2, x3 = skip_connection
        x4 = inputs

        x = x4
        x = self.upsample(x) # 512 * 32 * 32 
        x = self.layer4(x) # 256 * 32 * 32

        x = torch.cat([x, x3], dim=1) # 512 * 64 * 64
        x = self.upsample(x) # 512 * 64 * 64
        x = self.layer3(x) # 128 * 64 * 64 

        x = torch.cat([x, x2], dim=1) # 256 * 64 * 64
        x = self.upsample(x) # 256 * 128 * 128
        x = self.layer2(x) # 64 * 128 * 128 

        x =  torch.cat([x, x1], dim=1)  # 128 * 128 * 128
        x = self.upsample(x) # 128 * 256 * 256
        x = self.layer1(x) # 64 * 256 * 256                 

        x = self.layer0(x) # 3 * 256 * 256

        return x

    
class Color2Sketch(nn.Module):
    def __init__(self, input_nc=3, output_nc=1, norm='BN', SN=False, activation='relu', residual=False, ckpt_path=None):
        super(Color2Sketch, self).__init__()
        self.encoder = Encoder(input_nc=input_nc, norm=norm, SN=SN, activation='lrelu')
        self.middle = Middle(512, norm=norm, SN=SN, activation=activation, residual=residual)
        self.decoder = Decoder(output_nc=output_nc, norm=norm, SN=SN, activation='lrelu')

        if ckpt_path:
            # checkpoint = torch.load(ckpt_path)
            checkpoint = torch.load(ckpt_path, map_location=torch.device('cpu'))
            self.load_state_dict(checkpoint['netG'], strict=True)
        else:
            self.apply(weights_init)
            
    def forward(self, inputs):
        skip_connection, encode = self.encoder(inputs)
        encode = self.middle(encode)
        output = self.decoder(skip_connection, encode)
        
        return output

class Colorizenet(nn.Module):
    def __init__(self, input_nc=3, output_nc=1, norm='BN', SN=False, activation='relu', residual=False, ckpt_path=None):
        super(Colorizenet, self).__init__()
        self.encoder = Encoder(input_nc=input_nc, norm=norm, SN=SN, activation='lrelu')
        self.middle = Middle(512, norm=norm, SN=SN, activation=activation, residual=residual)
        self.decoder = Decoder(output_nc=output_nc, norm=norm, SN=SN, activation='lrelu')

        if ckpt_path:
            # checkpoint = torch.load(ckpt_path)
            checkpoint = torch.load(ckpt_path, map_location=torch.device('cpu'))
            self.load_state_dict(checkpoint['netG'], strict=True)
        else:
            self.apply(weights_init)
            
    def forward(self, inputs):
        skip_connection, encode = self.encoder(inputs)
        encode = self.middle(encode)
        output = self.decoder(skip_connection, encode)
        
        return output
    
class Discriminator(nn.Module):
    def __init__(self, nc=6, pretrained=False):
        super(Discriminator, self).__init__()
        self.conv1 = nn.Conv2d(nc, 64, kernel_size=4, stride=2, padding=1)
        self.norm1 = nn.InstanceNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1)
        self.norm2 = nn.InstanceNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1)
        self.norm3 = nn.InstanceNorm2d(256)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=4, stride=1, padding=1)
        self.norm4 = nn.InstanceNorm2d(512)
        self.conv5 = nn.Conv2d(512, 1, kernel_size=4, stride=1, padding=1)           
        self.activation = nn.LeakyReLU(0.2, inplace=True)
        
        if pretrained:
            pass
        else:
            self.apply(weights_init)
            print('Weights of {0} model are initialized'.format('Discriminator'))

    def forward(self, inputs, condition):
        x = torch.cat([inputs, condition], dim=1)
        x = self.activation(self.conv1(x))
        x = self.activation(self.norm2(self.conv2(x)))
        x = self.activation(self.norm3(self.conv3(x)))
        x = self.activation(self.norm4(self.conv4(x)))
        x = self.conv5(x)
        x = x.mean((2,3))

        return x
    
    def weight_init(self, mean, std):
        for m in self._modules:
            normal_init(self._modules[m], mean, std)
            
class VGG16FeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        vgg16 = models.vgg16(pretrained=True)
        self.enc_1 = nn.Sequential(*vgg16.features[:5])
        self.enc_2 = nn.Sequential(*vgg16.features[5:10])
        self.enc_3 = nn.Sequential(*vgg16.features[10:17])

        # fix the encoder
        for i in range(3):
            for param in getattr(self, 'enc_{:d}'.format(i + 1)).parameters():
                param.requires_grad = False

    def forward(self, image):
        results = [image]
        for i in range(3):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

# To initialize model weights
def weights_init(model):
    classname = model.__class__.__name__
    if classname.find('Conv2d') != -1:
        nn.init.normal_(model.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(model.weight.data, 1.0, 0.02)
        nn.init.constant_(model.bias.data, 0)
    elif classname.find('GroupNorm') != -1:
        nn.init.normal_(model.weight.data, 1.0, 0.02)
        nn.init.constant_(model.bias.data, 0)
    else:
        pass