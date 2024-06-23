import argparse
import os

import torch
from torch.utils.data import DataLoader
import torchvision as tv


def main(batch_size: int, data_dir: str, model_path: str) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_path} not found")

    model = torch.load(model_path)
    model.eval()

    dataset = tv.datasets.MNIST(
        root=data_dir,
        train=False,
        transform=tv.transforms.ToTensor(),
        download=True,
    )

    # dataset = tv.datasets.EMNIST(
    #     root=data_dir,
    #     split="letters",
    #     train=False,
    #     transform=tv.transforms.Compose(
    #         [
    #             lambda image: tv.transforms.functional.rotate(image, -90),
    #             lambda image: tv.transforms.functional.hflip(image),
    #             tv.transforms.ToTensor(),
    #         ]
    #     ),
    #     download=True,
    # )

    data_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

    correct = 0
    total = 0

    print("Number of Parameters:", sum(p.numel() for p in model.parameters()))

    with torch.inference_mode():
        for images, labels in data_loader:
            images = images.to(device)
            images = images.view(-1, 28**2)
            images = torch.where(
                images > 0.1, torch.ones_like(images), torch.zeros_like(images)
            )

            labels = labels.to(device)

            outputs = model(images)

            predicted = torch.argmax(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total

        test_image = images[-1]
        test_image = test_image.unsqueeze(0)

        test_label = labels[-1]
        test_label = test_label.unsqueeze(0)

        tv.utils.save_image(test_image.view(1, 1, 28, 28), "test_image.png")

        classes = dataset.classes
        model_no_softmax = torch.nn.Sequential(*(list(model.children())[:-1]))
        test_image = test_image.to(device)
        predicted_array = model_no_softmax(test_image)
        predicted_index = torch.argmax(predicted_array).item()
        predicted_output = classes[predicted_index]

    print("Predicted Classes:", classes)
    print("Predicted Array:", predicted_array)
    print("Predicted Index:", predicted_index)
    print("Predicted Output:", predicted_output)
    print("Expected Output:", classes[test_label.item()])
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--batch_size", type=int, default=16)
    args.add_argument("--data_dir", type=str, default="./data")
    args.add_argument("--model_path", type=str, default="./model.pt")

    args = args.parse_args()

    main(
        batch_size=args.batch_size,
        data_dir=args.data_dir,
        model_path=args.model_path,
    )
