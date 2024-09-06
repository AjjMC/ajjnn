import torch


def create_model(num_classes: int, split: str) -> torch.nn.Module:
    if split == "balanced":
        # 80% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(28**2, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, num_classes),
        )

    elif split == "letters":
        # 86% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(28**2, 48),
            torch.nn.ReLU(),
            torch.nn.Linear(48, 24),
            torch.nn.ReLU(),
            torch.nn.Linear(24, num_classes),
        )

    elif split == "digits":
        # 96% accuracy
        model = torch.nn.Sequential(
            torch.nn.Linear(28**2, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, num_classes),
        )

    return model
