import logging
from argparse import ArgumentParser
from pathlib import Path

import torch
import torchvision as tv
from torch.utils.data import DataLoader

from utils import calc_accuracy, get_data


def main(
    batch_size: int,
    checkpoint_dir: Path,
    checkpoint_num: int,
    data: str,
    data_dir: Path,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, test_data = get_data(data=data, data_dir=data_dir)

    test_data_loader = DataLoader(dataset=test_data, batch_size=batch_size)

    num_features = (
        test_data[0][0].shape[0] * test_data[0][0].shape[1] * test_data[0][0].shape[2]
    )

    classes = test_data.classes
    num_classes = len(classes)

    model = load_checkpoint(
        checkpoint_num=checkpoint_num, checkpoint_dir=checkpoint_dir, device=device
    )

    num_params = sum(p.numel() for p in model.parameters())

    logger.info("%s, Classes (%d): %s", data, num_classes, classes)
    logger.info("Number of Parameters: %d", num_params)

    accuracy = calc_accuracy(
        model=model,
        test_data_loader=test_data_loader,
        num_features=num_features,
        device=device,
    )

    logger.info("Accuracy: %.2f%%", accuracy)

    image, output, output_class, output_index, target_class, label = test_model(
        model=model,
        test_data_loader=test_data_loader,
        num_features=num_features,
        classes=classes,
        device=device,
    )

    tv.utils.save_image(image, f"{data}_{target_class}.png")

    logger.info("Output: %s", output)
    logger.info("Output Class: %s (%d)", output_class, output_index)
    logger.info("Target Class: %s (%d)", target_class, label)


def load_checkpoint(
    checkpoint_num: int, checkpoint_dir: Path, device: torch.device
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

    checkpoint = torch.load(checkpoint_path, weights_only=False)

    model = checkpoint["model"]
    model = model.to(device)

    return model


@torch.inference_mode()
def test_model(
    model: torch.nn.Module,
    test_data_loader: DataLoader,
    num_features: int,
    classes: list[str],
    device: torch.device,
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


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--checkpoint_dir", type=Path, default="checkpoints")
    parser.add_argument("--checkpoint_num", type=int, default=-1)
    parser.add_argument(
        "--data",
        type=str,
        choices=["emnist_balanced", "emnist_digits", "emnist_letters"],
        default="emnist_digits",
    )
    parser.add_argument("--data_dir", type=Path, default="data")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    logger = logging.getLogger(__name__)

    main(
        batch_size=args.batch_size,
        checkpoint_dir=args.checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        data=args.data,
        data_dir=args.data_dir,
    )
