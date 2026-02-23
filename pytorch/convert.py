import logging
from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path

import torch


def main(
    add_argmax: bool, checkpoint_dir: Path, checkpoint_num: str, model_name: str
) -> None:
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

    if not isinstance(model, torch.nn.Sequential):
        raise RuntimeError("Model must be an instance of torch.nn.Sequential")

    root = Path(__file__).parents[1]
    converted_model_path = (
        root / "data" / "ajjnn" / "function" / "model" / f"{model_name}.mcfunction"
    )

    with open(converted_model_path, "w") as f:
        set_model_name = (
            f'data modify storage ajjnn:data model_name set value "{model_name}"\n\n'
        )

        set_num_params = f"data modify storage ajjnn:data num_params set value {sum(p.numel() for p in model.parameters())}\n\n"

        add_linear_module = (
            'data modify storage ajjnn:data modules append value {type:"linear"}\n\n'
        )

        add_relu_module = (
            'data modify storage ajjnn:data modules append value {type:"relu"}\n\n'
        )

        add_hard_sigmoid_module = 'data modify storage ajjnn:data modules append value {type:"hard_sigmoid"}\n\n'

        add_argmax_module = (
            'data modify storage ajjnn:data modules append value {type:"argmax"}\n\n'
        )

        f.write(set_model_name)
        f.write(set_num_params)

        for module in model:
            if isinstance(module, torch.nn.Linear):
                if module.in_features > 784:
                    raise RuntimeError("Number of input features cannot exceed 784")

                if module.out_features > 784:
                    raise RuntimeError("Network width cannot exceed 784")

                weights = module.weight.data
                biases = module.bias.data

                weights_formatted_inside = ",".join(
                    f"[{','.join(f'{value:.3f}' for value in row)}]" for row in weights
                )

                weights_formatted = f"[{weights_formatted_inside}]"

                biases_formatted_inside = ",".join(f"{value:.3f}" for value in biases)

                biases_formatted = f"[{biases_formatted_inside}]"

                set_linear_module_weights = f"data modify storage ajjnn:data modules[-1].weights set value {weights_formatted}\n\n"

                set_linear_module_biases = f"data modify storage ajjnn:data modules[-1].biases set value {biases_formatted}\n\n"

                f.write(add_linear_module)
                f.write(set_linear_module_weights)
                f.write(set_linear_module_biases)

            elif isinstance(module, torch.nn.ReLU):
                f.write(add_relu_module)

            elif isinstance(module, torch.nn.Hardsigmoid):
                f.write(add_hard_sigmoid_module)

            elif isinstance(module, torch.nn.Dropout):
                continue

            else:
                raise RuntimeError(f"Module {module} is not supported")

        if add_argmax:
            f.write(add_argmax_module)

    logger.info("Model %s has been converted for use in Minecraft", model_name)
    logger.info(
        'If ajjnn is installed, reload the datapack and run /function ajjnn:__load {{model:"%s"}} to load the model into the game',
        model_name,
    )


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--add_argmax", action=BooleanOptionalAction, default=False)
    parser.add_argument("--checkpoint_dir", type=Path, default="checkpoints")
    parser.add_argument("--checkpoint_num", type=int, default=-1)
    parser.add_argument("--model_name", type=str, default="model")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    logger = logging.getLogger(__name__)

    main(
        add_argmax=args.add_argmax,
        checkpoint_dir=args.checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        model_name=args.model_name,
    )
