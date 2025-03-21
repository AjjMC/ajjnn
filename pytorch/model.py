import torch


def create_model(num_features: int, num_classes: int, data: str) -> torch.nn.Module:
    if data == "emnist_balanced":
        # 80% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(num_features, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, num_classes),
        )

    elif data == "emnist_letters":
        # 86% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(num_features, 48),
            torch.nn.ReLU(),
            torch.nn.Linear(48, 24),
            torch.nn.ReLU(),
            torch.nn.Linear(24, num_classes),
        )

    elif data == "emnist_digits":
        # 96% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(num_features, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, num_classes),
        )

    elif data == "cifar10":
        model = torch.nn.Sequential(
            torch.nn.Linear(num_features, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, num_classes),
        )

    elif data == "cifar100":
        model = torch.nn.Sequential(
            torch.nn.Linear(num_features, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, num_classes),
        )

    return model
