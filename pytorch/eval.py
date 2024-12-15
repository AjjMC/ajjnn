import argparse
import os

import torch
from torch.utils.data import DataLoader
import torchvision as tv


@torch.inference_mode()
def calc_accuracy(
    model: torch.nn.Module, data_loader: torch.utils.data.DataLoader
) -> float:
    device = next(model.parameters()).device

    training = True if model.training else False
    model.eval()

    correct = 0
    total = 0

    for images, labels in data_loader:
        images = images.to(device)
        images = images.view(-1, images.shape[1] * images.shape[2] * images.shape[3])
        images = torch.where(
            images >= 0.5, torch.ones_like(images), torch.zeros_like(images)
        )

        labels = labels.to(device)

        outputs = model(images)

        output_indexes = torch.argmax(outputs, dim=1)

        total += labels.size(0)
        correct += (output_indexes == labels).sum().item()

    if training:
        model.train()

    accuracy = 100 * correct / total

    return accuracy


@torch.inference_mode()
def test_classifier(model, data_loader):
    device = next(model.parameters()).device

    classes = data_loader.dataset.classes

    images, labels = next(iter(data_loader))

    image = images[0]
    image = image.to(device)
    image = image.unsqueeze(0)
    image = image.view(-1, image.shape[1] * image.shape[2] * image.shape[3])
    image = torch.where(image >= 0.5, torch.ones_like(image), torch.zeros_like(image))

    label = labels[0]

    output = model(image)
    output_index = torch.argmax(output).item()
    output_class = classes[output_index]
    target_class = classes[label]

    image = images[0]
    image = torch.where(image >= 0.5, torch.ones_like(image), torch.zeros_like(image))

    return image, classes, output, output_class, output_index, target_class, label


def main(
    batch_size: int,
    data_dir: str,
    checkpoint_dir: str,
    checkpoint_num: str,
    dataset: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if "emnist" in dataset:
        emnist_split = dataset.split("_")[1]

        test_dataset = tv.datasets.EMNIST(
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

    elif dataset == "cifar10":
        test_dataset = tv.datasets.CIFAR10(
            root=data_dir,
            train=False,
            transform=tv.transforms.ToTensor(),
            download=True,
        )

    elif dataset == "cifar100":
        test_dataset = tv.datasets.CIFAR100(
            root=data_dir,
            train=False,
            transform=tv.transforms.ToTensor(),
            download=True,
        )

    classes = test_dataset.classes
    num_classes = len(classes)

    if not os.path.exists(checkpoint_dir):
        raise FileNotFoundError(f"Checkpoint directory {checkpoint_dir} not found")

    checkpoint_list = os.listdir(checkpoint_dir)
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        raise ValueError(f"Checkpoint directory {checkpoint_dir} is empty")

    if checkpoint_num not in range(-1, len(checkpoint_list)):
        raise ValueError(
            f"Checkpoint number {checkpoint_num} not in range [-1, {len(checkpoint_list)})"
        )

    checkpoint_file = checkpoint_list[checkpoint_num]
    checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)

    if not os.path.exists(checkpoint_path):
        raise ValueError(f"Checkpoint file {checkpoint_path} not found")

    model, _ = torch.load(checkpoint_path)
    model = model.to(device)

    num_classes_model = model[-1].out_features

    if num_classes_model != num_classes:
        raise ValueError(
            "Number of model classes ({num_classes_model}) does not match number of dataset classes ({num_classes})"
        )

    num_params = sum(p.numel() for p in model.parameters())

    data_loader = DataLoader(dataset=test_dataset, batch_size=batch_size)

    print(f"{dataset}, {num_classes} Classes: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)

    accuracy = calc_accuracy(model, data_loader)

    print(f"Accuracy: {accuracy:.2f}%", flush=True)

    image, classes, output, output_class, output_index, target_class, label = (
        test_classifier(model, data_loader)
    )

    tv.utils.save_image(image, f"./{dataset}_{target_class}.png")

    print(f"Output: {output}", flush=True)
    print(f"Output Class: {output_class} ({output_index})", flush=True)
    print(f"Target Class: {target_class} ({label})", flush=True)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--data_dir", type=str, default="./data")
    args.add_argument("--checkpoint_dir", type=str, default="./checkpoints")
    args.add_argument("--checkpoint_num", type=int, default=-1)
    args.add_argument(
        "--dataset",
        type=str,
        choices=[
            "emnist_balanced",
            "emnist_letters",
            "emnist_digits",
            "cifar10",
            "cifar100",
        ],
        default="emnist_digits",
    )

    args = args.parse_args()

    main(
        batch_size=args.batch_size,
        data_dir=args.data_dir,
        checkpoint_dir=args.checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        dataset=args.dataset,
    )
