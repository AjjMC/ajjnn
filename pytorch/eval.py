import logging
from argparse import ArgumentParser
from pathlib import Path

import torch
import torchvision as tv

from utils import (
    calc_accuracy,
    get_data,
    get_data_loaders,
    get_num_features,
    test_model,
)


def main(
    batch_size: int,
    data_dir: Path,
    checkpoint_dir: Path,
    checkpoint_num: int,
    data: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, test_data = get_data(data, data_dir)

    _, test_data_loader = get_data_loaders(None, test_data, batch_size)

    num_features = get_num_features(test_data)

    classes = test_data.classes
    num_classes = len(classes)

    model = load_epoch(checkpoint_dir, checkpoint_num, device)

    num_params = sum(p.numel() for p in model.parameters())

    logger.info("%s, Classes (%d): %s", data, num_classes, classes)
    logger.info("Number of Parameters: %d", num_params)

    accuracy = calc_accuracy(model, test_data_loader, device, num_features)

    logger.info("Accuracy: %.2f%%", accuracy)

    image, output, output_class, output_index, target_class, label = test_model(
        model, test_data_loader, device, num_features, classes
    )

    tv.utils.save_image(image, f"{data}_{target_class}.png")

    logger.info("Output: %s", output)
    logger.info("Output Class: %s (%d)", output_class, output_index)
    logger.info("Target Class: %s (%d)", target_class, label)


def load_epoch(
    checkpoint_dir: Path, checkpoint_num: int, device: torch.device
) -> torch.nn.Module:
    if not checkpoint_dir.exists() or not checkpoint_dir.is_dir():
        raise RuntimeError(
            f"Checkpoint directory {checkpoint_dir} is missing or invalid"
        )

    checkpoint_list = list(checkpoint_dir.glob("epoch_*.pt"))
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.name.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        raise RuntimeError(f"Checkpoint directory {checkpoint_dir} is empty")

    if checkpoint_num not in range(-1, len(checkpoint_list)):
        raise RuntimeError(
            f"Checkpoint number {checkpoint_num} is not in range [-1, {len(checkpoint_list)})"
        )

    checkpoint_path = checkpoint_list[checkpoint_num]

    if not checkpoint_path.exists() or not checkpoint_path.is_file():
        raise RuntimeError(f"Checkpoint file {checkpoint_path} is missing or invalid")

    model, _ = torch.load(checkpoint_path, weights_only=False)
    model = model.to(device)

    return model


if __name__ == "__main__":
    args = ArgumentParser()

    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--data_dir", type=Path, default="data")
    args.add_argument("--checkpoint_dir", type=Path, default="checkpoints")
    args.add_argument("--checkpoint_num", type=int, default=-1)
    args.add_argument(
        "--data",
        type=str,
        choices=["emnist_balanced", "emnist_letters", "emnist_digits"],
        default="emnist_digits",
    )

    args = args.parse_args()

    logger = logging.getLogger(__name__)

    main(
        batch_size=args.batch_size,
        data_dir=args.data_dir,
        checkpoint_dir=args.checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        data=args.data,
    )
