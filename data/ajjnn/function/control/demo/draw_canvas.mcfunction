fill ~-0.75 ~ ~-0.75 ~0.75 ~ ~0.75 minecraft:black_concrete replace minecraft:white_concrete

execute if entity @s[distance=..64] positioned ^ ^ ^0.5 run function ajjnn:control/demo/draw_canvas

execute if data storage ajjnn:data {status:0b} run schedule function ajjnn:control/demo/forward 1s