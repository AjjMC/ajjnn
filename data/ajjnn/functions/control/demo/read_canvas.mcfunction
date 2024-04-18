execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run summon minecraft:marker ~ ~ ~ {Tags:["ajjnn.canvas_reader"]}

scoreboard players set #count ajjnn 1
scoreboard players set #length ajjnn 28

execute as @e[type=minecraft:marker,tag=ajjnn.canvas_reader] at @s run function ajjnn:control/demo/move_canvas_reader

kill @e[type=minecraft:marker,tag=ajjnn.canvas_reader]