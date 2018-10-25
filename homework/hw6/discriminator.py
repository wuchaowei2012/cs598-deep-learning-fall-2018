import torch
import torch.nn as nn

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.out_dim = 32
        self.in_channels = 3
        self.out_channels = 196

        # Create every conv layer.
        self.conv1 = self._add_block(1, is_first_block=True)
        self.conv2 = self._add_block(2)
        self.conv3 = self._add_block(1)
        self.conv4 = self._add_block(2)
        self.conv5 = self._add_block(1)
        self.conv6 = self._add_block(1)
        self.conv7 = self._add_block(1)
        self.conv8 = self._add_block(2)

        # Append all conv layers into a list for convenience.
        self.conv_layers = [
            self.conv1, self.conv2, self.conv3, self.conv4, 
            self.conv5, self.conv6, self.conv7, self.conv8
        ]

        self.maxpool = nn.MaxPool2d(4, stride=4)
        self.fc1 = nn.Linear(self.out_channels, 1)
        self.fc10 = nn.Linear(self.out_channels, 10)
    
    def forward(self, x):
        for layer in self.conv_layers:
            x = layer(x)       
        x = x.maxpool(x)

        # Reshape to (batch_size, 1*1*196)
        x = x.view(x.shape[0], -1)

        x_from_fc1 = self.fc1(x)
        x_from_fc10 = self.fc10(x)

        return x_from_fc1, x_from_fc10

    def _add_block(self, stride, is_first_block=False):
        if stride == 2:
            self.out_dim //= 2
        
        if is_first_block:
            in_channels = self.in_channels
        else:
            in_channels = self.out_channels

        # conv2d -> layer norm -> leaky relu
        block = nn.Sequential(
            nn.Conv2d(in_channels, self.out_channels, 3, padding=1, stride=stride),
            nn.LayerNorm((self.out_channels, self.out_dim, self.out_dim)),
            nn.LeakyReLU(inplace=True)
        )
        return block