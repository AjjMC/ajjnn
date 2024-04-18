import argparse
import os

import torch


def main(model_path: str, model_name: str) -> None:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_path} was not found")

    model = torch.load(model_path)

    if not isinstance(model, torch.nn.Sequential):
        raise ValueError("Model must be an instance of torch.nn.Sequential")

    parent = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(parent)
    converted_model_path = os.path.join(
        root, "data", "ajjnn", "functions", "models", f"{model_name}.mcfunction"
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

        for i, layer in enumerate(model):
            if isinstance(layer, torch.nn.Linear):
                weights = layer.weight.data
                biases = layer.bias.data

                weights_formatted_inside = ",".join(
                    f"[{','.join(f'{value:.3f}' for value in row)}]" for row in weights
                )

                weights_formatted = f"[{weights_formatted_inside}]"

                biases_formatted_inside = ",".join(f"{value:.3f}" for value in biases)

                biases_formatted = f"[{biases_formatted_inside}]"

                set_linear_layer_weights = f"data modify storage ajjnn:data sequence[{i}].weights set value {weights_formatted}\n\n"

                set_linear_layer_biases = f"data modify storage ajjnn:data sequence[{i}].biases set value {biases_formatted}\n\n"

                f.write(add_linear_layer)
                f.write(set_linear_layer_weights)
                f.write(set_linear_layer_biases)

            elif isinstance(layer, torch.nn.ReLU):
                f.write(add_relu_layer)

            elif isinstance(layer, torch.nn.Hardsigmoid) or isinstance(
                layer, torch.nn.Sigmoid
            ):
                f.write(add_hard_sigmoid_layer)

            elif isinstance(layer, torch.nn.Softmax):
                f.write(add_argmax_layer)
            else:
                raise ValueError(f"Layer {layer} is not supported")

    print(f"Model {model_name} has been converted for use in Minecraft")
    print(
        f'If ajjnn is installed, reload the datapack and run /function ajjnn:__load {{model:"{model_name}"}} to load the model into the game'
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--model_path", type=str, default="./model.pt")
    parser.add_argument("--model_name", type=str, default="model")

    args = parser.parse_args()

    main(model_path=args.model_path, model_name=args.model_name)
