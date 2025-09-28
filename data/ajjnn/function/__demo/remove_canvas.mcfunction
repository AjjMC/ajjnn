execute unless entity @e[type=minecraft:marker,tag=ajjnn.canvas] run tellraw @s {text:"Unable to remove the demo canvas; the canvas was not found",color:"red"}
execute unless entity @e[type=minecraft:marker,tag=ajjnn.canvas] run return fail

execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~ ~ ~ ~-27 ~ ~-27 minecraft:air
kill @e[type=minecraft:marker,tag=ajjnn.canvas]

tellraw @a {text:"Removed demo canvas"}