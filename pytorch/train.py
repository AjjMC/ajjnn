import argparse
import os
import time

from model import create_model
from eval import calc_accuracy

import torch
from torch.utils.data import DataLoader
import torchvision as tv


def main(
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    data_dir: str,
    checkpoint_dir: str,
    data: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if "emnist" in data:
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

    elif data == "cifar10":
        train_data = tv.datasets.CIFAR10(
            root=data_dir, train=True, transform=tv.transforms.ToTensor(), download=True
        )

        test_data = tv.datasets.CIFAR10(
            root=data_dir,
            train=False,
            transform=tv.transforms.ToTensor(),
            download=True,
        )

    elif data == "cifar100":
        train_data = tv.datasets.CIFAR100(
            root=data_dir, train=True, transform=tv.transforms.ToTensor(), download=True
        )

        test_data = tv.datasets.CIFAR100(
            root=data_dir,
            train=False,
            transform=tv.transforms.ToTensor(),
            download=True,
        )

    num_features = (
        train_data[0][0].shape[0]
        * train_data[0][0].shape[1]
        * train_data[0][0].shape[2]
    )

    classes = train_data.classes
    num_classes = len(classes)

    os.makedirs(checkpoint_dir, exist_ok=True)

    checkpoint_list = os.listdir(checkpoint_dir)
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        model = create_model(num_features, num_classes, data)
        model = model.to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        checkpoint_num = 0
    else:
        checkpoint_file = checkpoint_list[-1]
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)

        model, optimizer = torch.load(checkpoint_path, weights_only=False)

        checkpoint_num = int(checkpoint_file.split("_")[-1].split(".")[0]) + 1

    num_params = sum(p.numel() for p in model.parameters())

    train_data_loader = DataLoader(
        dataset=train_data, batch_size=batch_size, shuffle=True
    )

    test_data_loader = DataLoader(dataset=test_data, batch_size=batch_size)

    print(f"{data}, {num_classes} Classes: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)
    print("Training on", device, flush=True)

    accuracies = []

    for epoch in range(checkpoint_num, checkpoint_num + num_epochs):
        avg_loss = 0.0
        len_data_loader = len(train_data_loader)

        start = time.perf_counter()

        for images, labels in train_data_loader:
            images = images.to(device)
            images = images.view(-1, num_features)
            images = torch.where(
                images >= 0.5, torch.ones_like(images), torch.zeros_like(images)
            )

            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = torch.nn.functional.cross_entropy(outputs, labels)

            loss.backward()

            optimizer.step()

            avg_loss += loss.item()

        avg_loss /= len_data_loader

        accuracy = calc_accuracy(model, test_data_loader)

        accuracies.append(accuracy)

        duration = round(time.perf_counter() - start)

        print(
            f"Epoch: {epoch}, Train Loss: {avg_loss:.4f}, Test Accuracy: {accuracy:.2f}%, Duration: {duration} s",
            flush=True,
        )

        torch.save(
            (model, optimizer), os.path.join(checkpoint_dir, f"epoch_{epoch}.pt")
        )

    best_epoch, best_accuracy = max(enumerate(accuracies), key=lambda x: x[1])
    best_epoch += checkpoint_num

    print(f"Best Epoch: {best_epoch}, Test Accuracy: {best_accuracy:.2f}%", flush=True)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--learning_rate", type=float, default=1e-3)
    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--num_epochs", type=int, default=10)
    args.add_argument("--data_dir", type=str, default="data")
    args.add_argument("--checkpoint_dir", type=str, default="checkpoints")
    args.add_argument(
        "--data",
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
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        data_dir=args.data_dir,
        checkpoint_dir=args.checkpoint_dir,
        data=args.data,
    )
