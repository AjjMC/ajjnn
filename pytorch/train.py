import logging
import time
from argparse import ArgumentParser
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from model import get_model
from utils import calc_accuracy, get_data


def main(
    batch_size: int,
    checkpoint_dir: Path,
    data: str,
    data_dir: Path,
    learning_rate: float,
    num_epochs: int,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_data, test_data = get_data(data=data, data_dir=data_dir)

    train_data_loader = DataLoader(
        dataset=train_data, batch_size=batch_size, shuffle=True
    )

    test_data_loader = DataLoader(dataset=test_data, batch_size=batch_size)

    num_features = (
        test_data[0][0].shape[0] * test_data[0][0].shape[1] * test_data[0][0].shape[2]
    )

    classes = test_data.classes
    num_classes = len(classes)

    model, optimizer, scheduler, checkpoint_num = load_checkpoint(
        data=data,
        num_features=num_features,
        num_classes=num_classes,
        num_epochs=num_epochs,
        learning_rate=learning_rate,
        checkpoint_dir=checkpoint_dir,
        device=device,
    )

    num_params = sum(p.numel() for p in model.parameters())

    logger.info("%s, Classes (%d): %s", data, num_classes, classes)
    logger.info("Number of Parameters: %d", num_params)
    logger.info("Training on %s", device)

    train_model(
        model=model,
        optimizer=optimizer,
        scheduler=scheduler,
        train_data_loader=train_data_loader,
        test_data_loader=test_data_loader,
        num_features=num_features,
        num_epochs=num_epochs,
        checkpoint_num=checkpoint_num,
        checkpoint_dir=checkpoint_dir,
        device=device,
    )


def load_checkpoint(
    data: str,
    num_features: int,
    num_classes: int,
    num_epochs: int,
    learning_rate: float,
    checkpoint_dir: Path,
    device: torch.device,
) -> tuple[
    torch.nn.Module, torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler, int
]:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_list = list(checkpoint_dir.glob("epoch_*.pt"))
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.name.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        model = get_model(data, num_features, num_classes)
        model = model.to(device)

        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=num_epochs
        )

        checkpoint_num = 0
    else:
        checkpoint_path = checkpoint_list[-1]

        checkpoint = torch.load(checkpoint_path, weights_only=False)

        model = checkpoint["model"]
        optimizer = checkpoint["optimizer"]
        scheduler = checkpoint["scheduler"]

        checkpoint_num = int(checkpoint_path.name.split("_")[-1].split(".")[0]) + 1

    return model, optimizer, scheduler, checkpoint_num


def train_model(
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
    train_data_loader: DataLoader,
    test_data_loader: DataLoader,
    num_features: int,
    num_epochs: int,
    checkpoint_num: int,
    checkpoint_dir: Path,
    device: torch.device,
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

        scheduler.step()

        avg_loss /= len_data_loader

        accuracy = calc_accuracy(model, test_data_loader, num_features, device)

        accuracies.append(accuracy)

        duration = round(time.perf_counter() - start)

        logger.info(
            "Epoch: %d, Train Loss: %.4f, Test Accuracy: %.2f%%, Duration: %d s",
            epoch,
            avg_loss,
            accuracy,
            duration,
        )

        torch.save(
            {"model": model, "optimizer": optimizer, "scheduler": scheduler},
            checkpoint_dir / f"epoch_{epoch}.pt",
        )

    best_epoch, best_accuracy = max(enumerate(accuracies), key=lambda x: x[1])
    best_epoch += checkpoint_num

    logger.info("Best Epoch: %d, Test Accuracy: %.2f%%", best_epoch, best_accuracy)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--checkpoint_dir", type=Path, default="checkpoints")
    parser.add_argument(
        "--data",
        type=str,
        choices=["emnist_balanced", "emnist_digits", "emnist_letters"],
        default="emnist_digits",
    )
    parser.add_argument("--data_dir", type=Path, default="data")
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--num_epochs", type=int, default=10)

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    logger = logging.getLogger(__name__)

    main(
        batch_size=args.batch_size,
        checkpoint_dir=args.checkpoint_dir,
        data=args.data,
        data_dir=args.data_dir,
        learning_rate=args.learning_rate,
        num_epochs=args.num_epochs,
    )
