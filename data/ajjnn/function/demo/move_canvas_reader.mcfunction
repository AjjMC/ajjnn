execute unless block ~ ~ ~ minecraft:black_concrete run data modify storage ajjnn:data in append value 0.0
execute if block ~ ~ ~ minecraft:black_concrete run data modify storage ajjnn:data in append value 1.0

scoreboard players operation #position ajjnn = #count ajjnn
scoreboard players operation #position ajjnn %= #length ajjnn

execute if score #position ajjnn matches 0 run tp @s ~27 ~ ~-1
execute unless score #position ajjnn matches 0 run tp @s ~-1 ~ ~

scoreboard players add #count ajjnn 1

execute if score #count ajjnn matches ..784 at @s run function ajjnn:demo/move_canvas_reader