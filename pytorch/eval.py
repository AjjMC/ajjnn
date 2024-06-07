import argparse
import os

import torch
import torchvision as tv
from torch.utils.data import DataLoader


def main(batch_size: int, data_path: str, model_path: str) -> None:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_path} not found")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = torch.load(model_path)
    model.eval()

    dataset = tv.datasets.MNIST(
        root=data_path,
        train=False,
        transform=tv.transforms.ToTensor(),
        download=True,
    )

    # dataset = tv.datasets.EMNIST(
    #     root=data_path,
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

    with torch.inference_mode():
        for images, labels in data_loader:
            images = images.to(device)
            images = images.view(-1, 784)
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
        test_label = labels[-1]

        tv.utils.save_image(test_image.view(1, 28, 28), "test_image.png")

        classes = dataset.classes
        model_no_softmax = torch.nn.Sequential(*(list(model.children())[:-1]))
        predicted_array = model_no_softmax(test_image.to(device))
        predicted_index = torch.argmax(predicted_array).item()
        predicted_output = classes[predicted_index]

    print("Predicted Classes", classes)
    print("Predicted Array", predicted_array)
    print("Predicted Index", predicted_index)
    print("Predicted Output", predicted_output)
    print("Expected Output", classes[test_label.item()])
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--batch_size", type=int, default=16)
    args.add_argument("--data_path", type=str, default="./data")
    args.add_argument("--model_path", type=str, default="./model.pt")

    args = args.parse_args()

    main(
        batch_size=args.batch_size,
        data_path=args.data_path,
        model_path=args.model_path,
    )
