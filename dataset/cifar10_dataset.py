import torchvision
from torchvision.transforms import transforms


class CIFAR10Dataset(torchvision.datasets.CIFAR10):
    def __init__(self, root: str, is_train: bool = True, transform=None):
        if transform is None:
            self.transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], inplace=True),
                transforms.Resize(32),
                transforms.CenterCrop(32),
            ])
        else:
            self.transform = transform
        super(CIFAR10Dataset, self).__init__(root, train=is_train, transform=self.transform, download=True)

    @property
    def num_class(self):
        return 10
