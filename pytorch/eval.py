import argparse
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
    data_dir: str,
    checkpoint_dir: Path,
    checkpoint_num: str,
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

    print(f"{data}, {num_classes} Classes: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)

    accuracy = calc_accuracy(model, test_data_loader, device, num_features)

    print(f"Accuracy: {accuracy:.2f}%", flush=True)

    image, output, output_class, output_index, target_class, label = test_model(
        model, test_data_loader, device, num_features, classes
    )

    tv.utils.save_image(image, f"{data}_{target_class}.png")

    print(f"Output: {output}", flush=True)
    print(f"Output Class: {output_class} ({output_index})", flush=True)
    print(f"Target Class: {target_class} ({label})", flush=True)


def load_epoch(
    checkpoint_dir: Path, checkpoint_num: int, device: torch.device
) -> torch.nn.Module:
    if not checkpoint_dir.exists() or not checkpoint_dir.is_dir():
        raise FileNotFoundError(f"Checkpoint directory {checkpoint_dir} not found")

    checkpoint_list = list(checkpoint_dir.glob("epoch_*.pt"))
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.name.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        raise ValueError(f"Checkpoint directory {checkpoint_dir} is empty")

    if checkpoint_num not in range(-1, len(checkpoint_list)):
        raise ValueError(
            f"Checkpoint number {checkpoint_num} not in range [-1, {len(checkpoint_list)})"
        )

    checkpoint_path = checkpoint_list[checkpoint_num]

    if not checkpoint_path.exists() or not checkpoint_path.is_file():
        raise ValueError(f"Checkpoint file {checkpoint_path} not found")

    model, _ = torch.load(checkpoint_path, weights_only=False)
    model = model.to(device)

    return model


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--data_dir", type=str, default="data")
    args.add_argument("--checkpoint_dir", type=str, default="checkpoints")
    args.add_argument("--checkpoint_num", type=int, default=-1)
    args.add_argument(
        "--data",
        type=str,
        choices=["emnist_balanced", "emnist_letters", "emnist_digits"],
        default="emnist_digits",
    )

    args = args.parse_args()

    checkpoint_dir = Path(args.checkpoint_dir)

    main(
        batch_size=args.batch_size,
        data_dir=args.data_dir,
        checkpoint_dir=checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        data=args.data,
    )
