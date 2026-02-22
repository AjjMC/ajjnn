import torch


def get_model(data: str, num_features: int, num_classes: int) -> torch.nn.Module:
    if data == "emnist_balanced":
        # 80% accuracy
        return torch.nn.Sequential(
            torch.nn.Linear(num_features, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, num_classes),
        )

    if data == "emnist_letters":
        # 86% accuracy
        return torch.nn.Sequential(
            torch.nn.Linear(num_features, 48),
            torch.nn.ReLU(),
            torch.nn.Linear(48, 24),
            torch.nn.ReLU(),
            torch.nn.Linear(24, num_classes),
        )

    if data == "emnist_digits":
        # 96% accuracy
        return torch.nn.Sequential(
            torch.nn.Linear(num_features, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, num_classes),
        )
