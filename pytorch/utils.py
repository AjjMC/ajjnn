from pathlib import Path

import torch
import torchvision as tv
from torch.utils.data import DataLoader, Dataset


@torch.inference_mode()
def calc_accuracy(
    model: torch.nn.Module,
    test_data_loader: DataLoader,
    num_features: int,
    device: torch.device,
) -> float:
    training = True if model.training else False
    model.eval()

    correct = 0
    total = 0

    for images, labels in test_data_loader:
        images = images.to(device)
        images = images.view(-1, num_features)
        images = torch.where(
            images >= 0.5, torch.ones_like(images), torch.zeros_like(images)
        )

        labels = labels.to(device)

        outputs = model(images)

        output_indexes = torch.argmax(outputs, dim=1)

        correct += (output_indexes == labels).sum().item()
        total += labels.size(0)

    if training:
        model.train()

    accuracy = 100 * correct / total

    return accuracy


def get_data(data: str, data_dir: Path) -> tuple[Dataset, Dataset]:
    emnist_split = data.split("_")[1]

    train_data = tv.datasets.EMNIST(
        root=data_dir,
        split=emnist_split,
        train=True,
        transform=tv.transforms.Compose(
            [
                lambda image: tv.transforms.functional.rotate(image, -90),
                lambda image: tv.transforms.functional.hflip(image),
                tv.transforms.ToTensor(),
            ]
        ),
        download=True,
    )

    test_data = tv.datasets.EMNIST(
        root=data_dir,
        split=emnist_split,
        train=False,
        transform=tv.transforms.Compose(
            [
                lambda image: tv.transforms.functional.rotate(image, -90),
                lambda image: tv.transforms.functional.hflip(image),
                tv.transforms.ToTensor(),
            ]
        ),
        download=True,
    )

    return train_data, test_data
