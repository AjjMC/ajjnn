fill ~-1.5 ~ ~-1.5 ~1.5 ~ ~1.5 minecraft:white_concrete replace minecraft:black_concrete

execute unless block ~ ~ ~ #minecraft:concrete positioned ^ ^ ^0.5 run function ajjnn:control/demo/erase_canvas

execute if data storage ajjnn:data {status:0b} run schedule function ajjnn:control/demo/forward 1s