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
        images = images.view(-1, 28**2)
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
    image = image.unsqueeze(0)

    image = image.to(device)
    image = image.view(-1, 28**2)
    image = torch.where(image >= 0.5, torch.ones_like(image), torch.zeros_like(image))

    label = labels[0]

    output = model(image)
    output_index = torch.argmax(output).item()
    output_class = classes[output_index]
    target_class = classes[label]

    image = image.view(1, 1, 28, 28)
    image = image.to("cpu")

    return image, classes, output, output_class, output_index, target_class, label


def main(
    batch_size: int, data_dir: str, params_dir: str, params_file: str, split: str
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

    classes = test_dataset.classes
    num_classes = len(classes)

    if not os.path.exists(params_dir):
        raise FileNotFoundError(f"Parameter directory {params_dir} not found")

    params_list = os.listdir(params_dir)
    params_list = sorted(params_list, key=lambda x: int(x.split("_")[-1].split(".")[0]))

    if len(params_list) == 0:
        raise ValueError(f"Parameter directory {params_dir} is empty")

    params = params_list[-1] if params_file is None else params_file
    params_path = os.path.join(params_dir, params)

    if not os.path.exists(params_path):
        raise ValueError(f"Parameter file {params_file} does not exist")

    model = torch.load(params_path)
    model = model.to(device)

    num_classes_model = model[-1].out_features

    if num_classes_model != num_classes:
        raise ValueError(
            "Number of model classes ({num_classes_model}) does not match number of EMNIST split classes ({num_classes})"
        )

    num_params = sum(p.numel() for p in model.parameters())

    data_loader = DataLoader(dataset=test_dataset, batch_size=batch_size)

    print(f"{split}, {num_classes} Classes: {classes}", flush=True)
    print("Number of Parameters:", num_params, flush=True)

    accuracy = calc_accuracy(model, data_loader)

    print(f"Accuracy: {accuracy:.2f}%", flush=True)

    image, classes, output, output_class, output_index, target_class, label = (
        test_classifier(model, data_loader)
    )

    tv.utils.save_image(image, "sample.png")

    print(f"Output: {output}", flush=True)
    print(f"Output Class: {output_class} ({output_index})", flush=True)
    print(f"Target Class: {target_class} ({label})", flush=True)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--batch_size", type=int, default=64)
    args.add_argument("--data_dir", type=str, default="./data")
    args.add_argument("--params_dir", type=str, default="./params")
    args.add_argument("--params_file", type=str, default=None)
    args.add_argument(
        "--split",
        type=str,
        choices=["balanced", "letters", "digits"],
        default="digits",
    )

    args = args.parse_args()

    main(
        batch_size=args.batch_size,
        data_dir=args.data_dir,
        params_dir=args.params_dir,
        params_file=args.params_file,
        split=args.split,
    )
