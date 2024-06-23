import argparse

import torch
from torch.utils.data import DataLoader
import torchvision as tv


def main(
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    data_dir: str,
    model_path: str,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = torch.nn.Sequential(
        torch.nn.Linear(28**2, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 10),
        torch.nn.Softmax(dim=1),
    )

    # model = torch.nn.Sequential(
    #     torch.nn.Linear(28**2, 64),
    #     torch.nn.ReLU(),
    #     torch.nn.Linear(64, 64),
    #     torch.nn.ReLU(),
    #     torch.nn.Linear(64, 27),
    #     torch.nn.Softmax(dim=1),
    # )

    model = model.to(device)
    num_classes = model[-2].out_features
    optim = torch.optim.Adam(model.parameters(), lr=learning_rate)

    dataset = tv.datasets.MNIST(
        root=data_dir,
        train=True,
        transform=tv.transforms.ToTensor(),
        download=True,
    )

    # dataset = tv.datasets.EMNIST(
    #     root=data_dir,
    #     split="letters",
    #     train=True,
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

    print("Number of Parameters:", sum(p.numel() for p in model.parameters()))
    print("Training on", device)

    for epoch in range(num_epochs):
        avg_loss = 0.0
        len_data_loader = len(data_loader)

        for images, labels in data_loader:
            images = images.to(device)
            images = images.view(-1, 28**2)
            images = torch.where(
                images > 0.1, torch.ones_like(images), torch.zeros_like(images)
            )

            labels = labels.to(device)
            labels = torch.nn.functional.one_hot(
                labels, num_classes=num_classes
            ).float()

            optim.zero_grad()

            loss = torch.nn.functional.binary_cross_entropy(model(images), labels)

            loss.backward()

            optim.step()

            avg_loss += loss.item() / len_data_loader

        print(f"Epoch {epoch} Loss: {avg_loss}")

    torch.save(model, model_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--learning_rate", type=float, default=1e-3)
    args.add_argument("--batch_size", type=int, default=16)
    args.add_argument("--num_epochs", type=int, default=10)
    args.add_argument("--data_dir", type=str, default="./data")
    args.add_argument("--model_path", type=str, default="./model.pt")

    args = args.parse_args()

    main(
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        data_dir=args.data_dir,
        model_path=args.model_path,
    )
