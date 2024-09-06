import argparse
import os

import torch


def main(params_dir: str, params_file: str, model_name: str, add_argmax: bool) -> None:
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

    if not isinstance(model, torch.nn.Sequential):
        raise ValueError("Model must be an instance of torch.nn.Sequential")

    parent = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(parent)
    converted_model_path = os.path.join(
        root, "data", "ajjnn", "function", "models", f"{model_name}.mcfunction"
    )

    with open(converted_model_path, "w") as f:
        set_model_name = (
            f'data modify storage ajjnn:data name set value "{model_name}"\n\n'
        )

        set_num_params = f"data modify storage ajjnn:data parameters set value {sum(p.numel() for p in model.parameters())}\n\n"

        add_linear_layer = (
            'data modify storage ajjnn:data sequence append value {layer:"linear"}\n\n'
        )

        add_relu_layer = (
            'data modify storage ajjnn:data sequence append value {layer:"relu"}\n\n'
        )

        add_hard_sigmoid_layer = 'data modify storage ajjnn:data sequence append value {layer:"hard_sigmoid"}\n\n'

        add_argmax_layer = (
            'data modify storage ajjnn:data sequence append value {layer:"argmax"}\n\n'
        )

        f.write(set_model_name)
        f.write(set_num_params)

        for layer in model:
            if isinstance(layer, torch.nn.Linear):
                if layer.in_features > 784:
                    raise ValueError("Number of input features cannot exceed 784")

                if layer.out_features > 784:
                    raise ValueError("Network width cannot exceed 784")

                weights = layer.weight.data
                biases = layer.bias.data

                weights_formatted_inside = ",".join(
                    f"[{','.join(f'{value:.3f}' for value in row)}]" for row in weights
                )

                weights_formatted = f"[{weights_formatted_inside}]"

                biases_formatted_inside = ",".join(f"{value:.3f}" for value in biases)

                biases_formatted = f"[{biases_formatted_inside}]"

                set_linear_layer_weights = f"data modify storage ajjnn:data sequence[-1].weights set value {weights_formatted}\n\n"

                set_linear_layer_biases = f"data modify storage ajjnn:data sequence[-1].biases set value {biases_formatted}\n\n"

                f.write(add_linear_layer)
                f.write(set_linear_layer_weights)
                f.write(set_linear_layer_biases)

            elif isinstance(layer, torch.nn.ReLU):
                f.write(add_relu_layer)

            elif isinstance(layer, torch.nn.Hardsigmoid):
                f.write(add_hard_sigmoid_layer)

            elif isinstance(layer, torch.nn.Dropout):
                continue

            else:
                raise ValueError(f"Layer {layer} is not supported")

        if add_argmax:
            f.write(add_argmax_layer)

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

    parser.add_argument("--params_dir", type=str, default="./params")
    parser.add_argument("--params_file", type=str, default=None)
    parser.add_argument("--model_name", type=str, default="model")
    parser.add_argument("--add_argmax", type=str2bool, default=False)

    args = parser.parse_args()

    main(
        params_dir=args.params_dir,
        params_file=args.params_file,
        model_name=args.model_name,
        add_argmax=args.add_argmax,
    )
