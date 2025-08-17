import argparse
import os

import torch


def main(
    checkpoint_dir: str, checkpoint_num: str, model_name: str, add_argmax: bool
) -> None:
    if not os.path.exists(checkpoint_dir):
        raise FileNotFoundError(f"Checkpoint directory {checkpoint_dir} not found")

    checkpoint_list = os.listdir(checkpoint_dir)
    checkpoint_list = sorted(
        checkpoint_list, key=lambda x: int(x.split("_")[-1].split(".")[0])
    )

    if len(checkpoint_list) == 0:
        raise ValueError(f"Checkpoint directory {checkpoint_dir} is empty")

    if checkpoint_num not in range(-1, len(checkpoint_list)):
        raise ValueError(
            f"Checkpoint number {checkpoint_num} not in range [-1, {len(checkpoint_list)})"
        )

    checkpoint_file = checkpoint_list[checkpoint_num]
    checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)

    if not os.path.exists(checkpoint_path):
        raise ValueError(f"Checkpoint file {checkpoint_path} not found")

    model, _ = torch.load(checkpoint_path, weights_only=False)

    if not isinstance(model, torch.nn.Sequential):
        raise ValueError("Model must be an instance of torch.nn.Sequential")

    parent = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(parent)
    converted_model_path = os.path.join(
        root, "data", "ajjnn", "function", "model", f"{model_name}.mcfunction"
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
                    raise ValueError("Number of input features cannot exceed 784")

                if module.out_features > 784:
                    raise ValueError("Network width cannot exceed 784")

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
                raise ValueError(f"Module {module} is not supported")

        if add_argmax:
            f.write(add_argmax_module)

    print(f"Model {model_name} has been converted for use in Minecraft")
    print(
        f'If ajjnn is installed, reload the datapack and run /function ajjnn:__load {{model:"{model_name}"}} to load the model into the game'
    )


def str2bool(v):
    if isinstance(v, bool):
        return v

    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True

    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False

    else:
        raise argparse.ArgumentTypeError("Expected Boolean")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--checkpoint_dir", type=str, default="checkpoints")
    parser.add_argument("--checkpoint_num", type=int, default=-1)
    parser.add_argument("--model_name", type=str, default="model")
    parser.add_argument("--add_argmax", type=str2bool, default=False)

    args = parser.parse_args()

    main(
        checkpoint_dir=args.checkpoint_dir,
        checkpoint_num=args.checkpoint_num,
        model_name=args.model_name,
        add_argmax=args.add_argmax,
    )
