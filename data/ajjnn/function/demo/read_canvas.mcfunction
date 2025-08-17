data modify storage ajjnn:data in set value []

scoreboard players set #count ajjnn 1
scoreboard players set #length ajjnn 28

execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run summon minecraft:marker ~ ~ ~ {Tags:["ajjnn.canvas_reader"]}
execute as @e[type=minecraft:marker,tag=ajjnn.canvas_reader] at @s run function ajjnn:demo/move_canvas_reader

kill @e[type=minecraft:marker,tag=ajjnn.canvas_reader]