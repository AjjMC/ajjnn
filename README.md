# A Neural Network Deployment Library for Minecraft Mapmaking

> **THIS IS A DEMO**
>
> **The datapack is still under development. This repository has been published as an early preview for Minecraft 1.20.4.**

## Overview

This datapack allows mapmakers to deploy neural networks in Minecraft. A Python script is provided, which converts a PyTorch model to an mcfunction file. This file loads the model into the game, enabling the datapack to perform inference.

## Downloading and Installing

The datapack can be downloaded from this repository by clicking on "Code" and then "Download ZIP". The folder inside the ZIP file is the datapack. After this folder has been added to the "datapacks" folder of a Minecraft world, ``/reload`` needs to be run in-game. A list of the datapack's commands is available via ``/function ajjnn:__help``. By convention, all functions run directly by the mapmaker start with two underscores. Functions starting with a single underscore are aliases that do not give any feedback messages in the chat. These are meant to be used by the mapmaker as part of their own map's datapack. Any functions not listed here are internal and are not meant to be used.

| Function                                 | Description                                          |
|:-----------------------------------------|:-----------------------------------------------------|
| ``/function ajjnn:__copyright``          | Displays datapack copyright information              |
| ``/function ajjnn:__demo/kit``           | Gives demo kit                                       |
| ``/function ajjnn:__demo/place_canvas``  | Places or relocates demo canvas                      |
| ``/function ajjnn:__demo/remove_canvas`` | Removes demo canvas                                  |
| ``/function ajjnn:__forward``            | Performs forward pass                                |
| ``/function ajjnn:__help``               | Displays datapack command list                       |
| ``/function ajjnn:__load``               | Loads PyTorch model into Minecraft                   |
| ``/function ajjnn:__install``            | Installs datapack                                    |
| ``/function ajjnn:__manual``             | Displays datapack manual link                        |
| ``/function ajjnn:__uninstall``          | Uninstalls datapack                                  |
| ``/function ajjnn:__view``               | Displays model architecture                          |
| ``/function ajjnn:_forward``             | Runs ``/function ajjnn:__forward`` without feedback  |
| ``/function ajjnn:_load``                | Runs ``/function ajjnn:__load`` without feedback     |

The datapack can be installed by running ``/function ajjnn:__install``. It can be uninstalled using ``/function ajjnn:__uninstall``, which removes all data associated with it from the world.

## Technical Details

The datapack is limited to models trained in PyTorch using ``torch.nn.Sequential``. The following layers are supported at the moment:

| Datapack Layer | Pytorch Layer Based On                         |
|:---------------|:-----------------------------------------------|
| Argmax         | ``torch.nn.Softmax``                           |
| Hard Sigmoid   | ``torch.nn.HardSigmoid``, ``torch.nn.Sigmoid`` |
| Linear         | ``torch.nn.Linear``                            |
| ReLU           | ``torch.nn.ReLU``                              |

The provided Python script ``convert.py`` maps the PyTorch layers on the right to the datapack layers on the left. The model parameters are rounded to a three decimal point precision to be compatible with the datapack's floating point arithmetic. Due to the large number of command executions involved, the number of input features and network width cannot be (much) more than 784. However, there is no limit to network depth. The number of ticks a forward pass takes increases with both the width and the depth of the network but not with the number of input features.

## Handwritten Digit Classification Demo

To test the datapack, a simple model for handwritten digit classification was trained on the Modified National Institute of Standards and Technology (MNIST) database and converted to a file ``mnist_demo.mcfunction``, located in ``./data/ajjnn/functions/models/``. This model can be loaded with ``/function ajjnn:__load {model:"mnist_demo"}``. This fully-connected neural network receives an input vector of 784 features, which have been preprocessed to correspond to black and white pixels, labeled with 0 (drawn) and 1 (not drawn) respectively in a flattened 28x28-pixel image. The model consists of two hidden layers, each one having 32 units, and the ReLU activation function after each. The output is passed to a softmax function to yield the probability distribution of 10 classes, corresponding to digits 0-9. The last one is, however, replaced by an argmax function in the datapack, which simply gives the most likely digit.

A canvas demo has been provided that allows the user to draw digits through raycasting. The canvas can be placed or relocated with ``/function ajjnn:__demo/place_canvas`` and removed with ``/function ajjnn:__demo/remove_canvas``. A brush and eraser kit can be obtained with ``/function ajjnn:__demo/kit``. To be more intuitive, the demo uses white for pixels not drawn and black for drawn pixels. Furthermore, the drawable area of the canvas is restricted to 20x20 pixels, which gives better results as the original dataset had been padded. On top of the canvas, there is a gray arrow facing south, indicating the upward direction when drawing digits. The demo has been designed to perform inference as the user is drawing digits, giving real-time feedback on the user's actionbar.

> **NOTE:** This is a very simple neural network architecture, constrained by the computational limitations associated with datapacks! Classification may often not be correct depending on one's own handwriting. When I test it, it almost always gives the right prediction for all digits but 7 and 9.

## Running Neural Networks

| Data Storage NBT        | Description                | Type                   |
|:------------------------|:---------------------------|:-----------------------|
| ``ajjnn:nn input``      | Model input                | Double List            |
| ``ajjnn:nn name``       | Model name                 | String                 |
| ``ajjnn:nn output``     | Model output               | Integer or Double List |
| ``ajjnn:nn parameters`` | Number of model parameters | Integer                |
| ``ajjnn:nn sequence``   | Model layers               | Compound List          |
| ``ajjnn:nn status``     | Model status               | Byte                   |

The currently loaded model's architecture and parameters are stored in the ``ajjnn:nn sequence`` NBT tag. Mapmakers can set the input ``ajjnn:nn input``, perform a forward pass with ``/function ajjnn:__forward`` and retrieve the output ``ajjnn:nn output``. The status of the model is determined by the ``ajjnn:nn status`` NBT tag. If this value is set to ``0b``, the model is idle and can be used. If it is set to ``1b``, the model is running and cannot be used. Once the output has been calculated, this value is set to ``2b`` for a single tick and then back to ``0b``.

## Copyright

Copyright © 2023 - 2024 Ajj (https://github.com/AjjMC/ajjnn)
