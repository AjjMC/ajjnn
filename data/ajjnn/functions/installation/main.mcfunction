execute if entity @e[type=minecraft:marker,tag=ajjnn.canvas] run function ajjnn:control/demo/main

execute as @a if score @s ajjnn.canvas matches 1.. run scoreboard players reset @s ajjnn.canvas