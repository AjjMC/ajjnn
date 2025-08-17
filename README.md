# A Neural Network Deployment Library for Minecraft Mapmaking

> **AVAILABLE ON 1.21.8**
>
> **Click [here](https://github.com/AjjMC/ajjnn/archive/refs/heads/main.zip) to download.**
>
> **Also available on [Modrinth](https://modrinth.com/datapack/ajjnn).**
>
> **For any queries, please use the issues section.**

<p align = "center">
  <img src="repo/demo_digits.gif" width="250">
  <img src="repo/demo_letters.gif" width="250">
</p>

<p align = "center">
  <i>Handwritten digit and letter classification models.</i>
</p>

## Overview

This datapack allows mapmakers to deploy neural networks of arbitrary widths and depths in Minecraft. It functions as a black box that performs inference dynamically for a given model, without requiring any modifications to be made. A Python script is provided, converting trained PyTorch models to standalone mcfunction files used to load them into the game.

## Installing

After this datapack has been added to the "datapacks" folder of a Minecraft world, ``/reload`` needs to be run in-game. A list of the datapack's commands is available via ``/function ajjnn:__help``. By convention, all functions run directly by the mapmaker start with two underscores. Functions starting with a single underscore are aliases that do not give any feedback messages in the chat. These are meant to be used by the mapmaker as part of their own map's datapack. Any functions not listed here are internal and are not meant to be used.

| Function                                        | Description                                         |
|:------------------------------------------------|:----------------------------------------------------|
| ``/function ajjnn:__crediting``                 | Displays datapack crediting information             |
| ``/function ajjnn:__demo/kit``                  | Gives demo kit                                      |
| ``/function ajjnn:__demo/place_canvas``         | Places or relocates demo canvas                     |
| ``/function ajjnn:__demo/remove_canvas``        | Removes demo canvas                                 |
| ``/function ajjnn:__forward``                   | Performs forward pass                               |
| ``/function ajjnn:__help``                      | Displays datapack command list                      |
| ``/function ajjnn:__load {model:<model_name>}`` | Loads PyTorch model into Minecraft                  |
| ``/function ajjnn:__install``                   | Installs datapack                                   |
| ``/function ajjnn:__manual``                    | Displays datapack manual link                       |
| ``/function ajjnn:__uninstall``                 | Uninstalls datapack                                 |
| ``/function ajjgui:__version``                  | Displays datapack version                           |
| ``/function ajjnn:__view``                      | Displays model architecture                         |
| ``/function ajjnn:_forward``                    | Runs ``/function ajjnn:__forward`` without feedback |
| ``/function ajjnn:_load {model:<model_name>}``  | Runs ``/function ajjnn:__load`` without feedback    |

The datapack can be installed by running ``/function ajjnn:__install``. It can be uninstalled using ``/function ajjnn:__uninstall``, which removes all data associated with it from the world.

## Converting Models

The datapack is limited to neural networks trained in PyTorch using ``torch.nn.Sequential``. At the moment, ``torch.nn.Linear`` is the only supported layer, along with the activation functions ``torch.nn.ReLU`` and ``torch.nn.HardSigmoid``. The provided Python script ``convert.py`` converts a PyTorch model to an mcfunction file, creating an NBT tag structure. Dropout layers ``torch.nn.Dropout``, used during the training process, are skipped, and an argmax function can be optionally applied by the script after the last layer, useful for classification models. The model parameters are rounded to a three decimal point precision to be compatible with the datapack's floating point arithmetic. Due to the large number of command executions involved, the number of input features and network width cannot exceed 784. However, there is no limit to network depth. The number of ticks a forward pass takes increases with both the width and the depth of the network but not with the number of input features. All converted models are automatically stored in ``./data/ajjnn/functions/models/`` as ``<model_name>.mcfunction``, where the name can be specified. They can then be loaded with ``/function ajjnn:__load {model:<model_name>}``.

## Available Demos

To test the datapack, some simple neural networks for handwritten character classification have been trained on the [EMNIST dataset](https://www.nist.gov/itl/products-and-services/emnist-dataset) and converted to their respective mcfunction files. These are ``demo_digits.mcfunction`` (10 classes, 96% accuracy), ``demo_letters.mcfunction`` (27 classes, 86% accuracy) and ``demo_balanced.mcfunction`` (47 classes, 80% accuracy). The models can be loaded by specifying their name (e.g., ``/function ajjnn:__load {model:"demo_digits"}``).

The neural networks receive an input vector of 784 features, which take the values 0 (background) or 1 (character) in a flattened 28x28-pixel image. Along with these demos, a canvas is provided that allows the user to draw characters through raycasting. The canvas can be placed or relocated with ``/function ajjnn:__demo/place_canvas`` and removed with ``/function ajjnn:__demo/remove_canvas``. A brush-eraser kit can be obtained with ``/function ajjnn:__demo/kit``. White is used for pixels not drawn and black for drawn pixels. The drawable area of the canvas is restricted to 20x20 pixels to indicate the expected character size as the dataset had been padded. On top of the canvas, there is a gray arrow facing south, showing the upward direction when drawing characters. As part of this demo setup, inference is performed as the user is drawing, giving real-time feedback on their actionbar.

## Running Models

| Data Storage NBT Tag      | Description                                                                         | Type          |
|:--------------------------|:------------------------------------------------------------------------------------|:--------------|
| ``ajjnn:data in``         | Model input                                                                         | Double List   |
| ``ajjnn:data model_name`` | Model name                                                                          | String        |
| ``ajjnn:data modules``    | Model modules                                                                       | Compound List |
| ``ajjnn:data num_params`` | Number of model parameters                                                          | Int           |
| ``ajjnn:data out``        | Model output                                                                        | Any           |
| ``ajjnn:data status``     | Model status                                                                        | Byte          |
| ``ajjnn:data values``     | List of model module outputs, where ``ajjnn:data values[-1]`` is ``ajjnn:data out`` | List          |

The currently loaded model's architecture and parameters are stored in the ``ajjnn:data modules`` NBT tag. Mapmakers can set the input ``ajjnn:data in``, perform a forward pass with ``/function ajjnn:__forward`` and retrieve the output ``ajjnn:data out``. The status of the model is determined by the ``ajjnn:data status`` NBT tag. If this value is set to ``0b``, the model is idle and can be used. If it is set to ``1b``, the model is running and cannot be used. Once the output has been calculated, this value is set to ``2b`` for a single tick and then back to ``0b``.

## Crediting

Made by Ajj and published under the MIT license. Please share the repository link.
