import torch
from torch import nn
from torchsummary import summary


class DepthWiseConv(nn.Module):
    def __init__(self, num_channels, kernel_size=3, stride=1):
        super().__init__()
        padding = (kernel_size - 1) // 2
        self.conv = nn.Conv2d(num_channels, num_channels, kernel_size=kernel_size, padding=padding, stride=stride,
                              groups=num_channels, bias=False)

    def forward(self, x):
        # (B, C, H, W) -> (B, C, H//stride, W//stride)
        x = self.conv(x)
        return x


class PointWiseConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)

    def forward(self, x):
        # (B, Cin, H, W) -> (B, Cout, H, W)
        x = self.conv(x)
        return x


class SeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, downscale=1):
        super().__init__()
        self.dw_conv = DepthWiseConv(in_channels, stride=downscale)
        self.bn1 = nn.BatchNorm2d(in_channels)
        self.relu1 = nn.ReLU6()
        self.pw_conv = PointWiseConv(in_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu2 = nn.ReLU6()

    def forward(self, x):
        # (B, Cin, H, W) -> (B, Cout, H/downscale, W/downscale)
        x = self.relu1(self.bn1(self.dw_conv(x)))
        x = self.relu2(self.bn2(self.pw_conv(x)))
        return x


class MobileNet(nn.Module):
    def __init__(self, num_class, alpha=1.0, input_resolution=224, **kwargs):
        super().__init__()
        if alpha <= 0:
            raise ValueError("width multiplier must be positive")
        if input_resolution < 1:
            raise ValueError("input resolution must larger than 1")
        self.num_class, self.alpha, self.input_resolution = num_class, alpha, input_resolution

        num_channels = [int(c * alpha) for c in (32, 64, 128, 128, 256, 256, 512, 512, 512, 512, 512, 512, 1024, 1024)]
        resolutions = [int(r * input_resolution / 224) for r in
                       (112, 112, 56, 56, 28, 28, 14, 14, 14, 14, 14, 14, 7, 7)]
        assert len(num_channels) == len(resolutions)

        # expand number of channels
        self.initial = nn.Sequential(
            nn.AdaptiveAvgPool2d(input_resolution),
            nn.Conv2d(3, num_channels[0], kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(num_channels[0]),
            nn.ReLU6(),
        )

        # break down conv into depth-wise separable conv
        separable_convs = []
        for in_channels, out_channels, in_dim, out_dim in zip(num_channels[:-1], num_channels[1:], resolutions[:-1],
                                                              resolutions[1:]):
            assert (in_dim % out_dim) == 0
            separable_convs.append(SeparableConv(in_channels, out_channels, downscale=in_dim // out_dim))
        self.separable_convs = nn.Sequential(*separable_convs)

        # classifier
        self.final = nn.Sequential(
            nn.AvgPool2d(resolutions[-1]),
            nn.Dropout(p=0.001),
            nn.Conv2d(num_channels[-1], num_class, kernel_size=1),  # 1x1 conv as linear layer
            nn.Flatten(),
            # no softmax
        )

    def forward(self, x):
        # (B, 3, H, W) -> (B, num_class)
        # no softmax implemented
        x = self.initial(x)
        x = self.separable_convs(x)
        x = self.final(x)
        return x

    def __repr__(self):
        return f"MobileNet({self.num_class}, alpha={self.alpha}, input_resolution={self.input_resolution})"


def test():
    net = MobileNet(1000)
    summary(net, (3, 224, 224))


if __name__ == '__main__':
    test()
