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
    params_dir: str,
    split: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_dataset = tv.datasets.EMNIST(
        root=data_dir,
        split=split,
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

    test_dataset = tv.datasets.EMNIST(
        root=data_dir,
        split=split,
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

    classes = train_dataset.classes
    num_classes = len(classes)

    os.makedirs(params_dir, exist_ok=True)

    params_list = os.listdir(params_dir)
    params_list = sorted(params_list, key=lambda x: int(x.split("_")[-1].split(".")[0]))

    if len(params_list) == 0:
        model = create_model(num_classes, split)
        model = model.to(device)

        checkpoint = 0
    else:
        params = params_list[-1]
        params_path = os.path.join(params_dir, params)

        model = torch.load(params_path)

        checkpoint = int(params.split("_")[-1].split(".")[0]) + 1

    optim = torch.optim.Adam(model.parameters(), lr=learning_rate)
    num_params = sum(p.numel() for p in model.parameters())

    train_data_loader = DataLoader(
        dataset=train_dataset, batch_size=batch_size, shuffle=True
    )

    test_data_loader = DataLoader(dataset=test_dataset, batch_size=batch_size)

    print(f"{split}, {num_classes} Classes: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)
    print("Training on", device, flush=True)

    accuracies = []

    for epoch in range(checkpoint, checkpoint + num_epochs):
        avg_loss = 0.0
        len_data_loader = len(train_data_loader)

        start = time.perf_counter()

        for images, labels in train_data_loader:
            images = images.to(device)
            images = images.view(-1, 28**2)
            images = torch.where(
                images >= 0.5, torch.ones_like(images), torch.zeros_like(images)
            )

            labels = labels.to(device)

            optim.zero_grad()

            outputs = model(images)

            loss = torch.nn.functional.cross_entropy(outputs, labels)

            loss.backward()

            optim.step()

            avg_loss += loss.item()

        avg_loss /= len_data_loader

        accuracy = calc_accuracy(model, test_data_loader)

        accuracies.append(accuracy)

        duration = round(time.perf_counter() - start)

        print(
            f"Epoch: {epoch}, Train Loss: {avg_loss:.4f}, Test Accuracy: {accuracy:.2f}%, Duration: {duration} s",
            flush=True,
        )

        torch.save(model, os.path.join(params_dir, f"epoch_{epoch}.pt"))

    best_epoch, best_accuracy = max(enumerate(accuracies), key=lambda x: x[1])
    best_epoch += checkpoint

    print(f"Best Epoch: {best_epoch}, Test Accuracy: {best_accuracy:.2f}%", flush=True)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--learning_rate", type=float, default=1e-3)
    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--num_epochs", type=int, default=10)
    args.add_argument("--data_dir", type=str, default="./data")
    args.add_argument("--params_dir", type=str, default="./params")
    args.add_argument(
        "--split",
        type=str,
        choices=["balanced", "letters", "digits"],
        default="digits",
    )

    args = args.parse_args()

    main(
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        data_dir=args.data_dir,
        params_dir=args.params_dir,
        split=args.split,
    )
