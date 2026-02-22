import argparse
import time
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset

from model import get_model
from utils import calc_accuracy, get_data, get_data_loaders, get_num_features


def main(
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    data_dir: Path,
    checkpoint_dir: Path,
    data: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_data, test_data = get_data(data, data_dir)

    train_data_loader, test_data_loader = get_data_loaders(
        train_data, test_data, batch_size
    )

    num_features = get_num_features(test_data)

    classes = test_data.classes
    num_classes = len(classes)

    model, optimizer, checkpoint_num = laod_epoch(
        checkpoint_dir, data, num_features, num_classes, device, learning_rate
    )

    num_params = sum(p.numel() for p in model.parameters())

    print(f"{data}, Classes {num_classes}: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)
    print("Training on", device, flush=True)

    train_model(
        checkpoint_num,
        num_epochs,
        train_data_loader,
        device,
        num_features,
        optimizer,
        model,
        test_data_loader,
        checkpoint_dir,
    )


def laod_epoch(
    checkpoint_dir: Path,
    data: str,
    num_features: int,
    num_classes: int,
    device: torch.device,
    learning_rate: float,
) -> tuple[torch.nn.Module, torch.optim.Optimizer, int]:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_list = list(checkpoint_dir.glob("epoch_*.pt"))
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.name.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        model = get_model(data, num_features, num_classes)
        model = model.to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        checkpoint_num = 0
    else:
        checkpoint_path = checkpoint_list[-1]

        model, optimizer = torch.load(checkpoint_path, weights_only=False)

        checkpoint_num = int(checkpoint_path.name.split("_")[-1].split(".")[0]) + 1

    return model, optimizer, checkpoint_num


def train_model(
    checkpoint_num: int,
    num_epochs: int,
    train_data_loader: DataLoader,
    device: torch.device,
    num_features: int,
    optimizer: torch.optim.Optimizer,
    model: torch.nn.Module,
    test_data_loader: DataLoader,
    checkpoint_dir: Path,
) -> list[float]:
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

        accuracy = calc_accuracy(model, test_data_loader, device, num_features)

        accuracies.append(accuracy)

        duration = round(time.perf_counter() - start)

        print(
            f"Epoch: {epoch}, Train Loss: {avg_loss:.4f}, Test Accuracy: {accuracy:.2f}%, Duration: {duration} s",
            flush=True,
        )

        torch.save((model, optimizer), checkpoint_dir / f"epoch_{epoch}.pt")

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
        choices=["emnist_balanced", "emnist_letters", "emnist_digits"],
        default="emnist_digits",
    )

    args = args.parse_args()

    data_dir = Path(args.data_dir)
    checkpoint_dir = Path(args.checkpoint_dir)

    main(
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        data_dir=data_dir,
        checkpoint_dir=checkpoint_dir,
        data=args.data,
    )
