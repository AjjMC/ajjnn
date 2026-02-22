from pathlib import Path

import torch
import torchvision as tv
from torch.utils.data import DataLoader, Dataset


@torch.inference_mode()
def calc_accuracy(
    model: torch.nn.Module,
    test_data_loader: DataLoader,
    device: torch.device,
    num_features: int,
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


def get_data_loaders(
    train_data: Dataset | None, test_data: Dataset, batch_size: int
) -> tuple[DataLoader | None, DataLoader]:
    if train_data is not None:
        train_data_loader = DataLoader(
            dataset=train_data, batch_size=batch_size, shuffle=True
        )
    else:
        train_data_loader = None

    test_data_loader = DataLoader(dataset=test_data, batch_size=batch_size)

    return train_data_loader, test_data_loader


def get_num_features(test_data: Dataset) -> int:
    return (
        test_data[0][0].shape[0] * test_data[0][0].shape[1] * test_data[0][0].shape[2]
    )


@torch.inference_mode()
def test_model(
    model: torch.nn.Module,
    test_data_loader: DataLoader,
    device: torch.device,
    num_features: int,
    classes: list[str],
) -> tuple[torch.Tensor, torch.Tensor, str, int, str, int]:
    images, labels = next(iter(test_data_loader))

    image = images[0]
    image = image.to(device)
    image = image.unsqueeze(0)
    image = image.view(-1, num_features)
    image = torch.where(image >= 0.5, torch.ones_like(image), torch.zeros_like(image))

    label = labels[0]

    output = model(image)
    output_index = torch.argmax(output).item()
    output_class = classes[output_index]
    target_class = classes[label]

    image = images[0]
    image = torch.where(image >= 0.5, torch.ones_like(image), torch.zeros_like(image))

    return image, output, output_class, output_index, target_class, label
