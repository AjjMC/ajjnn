execute unless data storage ajjnn:data version run tellraw @s [{"text":"Unable to place canvas; ","color":"red"},{"text":"ajjnn","color":"gray"},{"text":" is not installed","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__install"},"hoverEvent":{"action":"show_text","contents":"Click Here"}}]
execute unless data storage ajjnn:data version run return fail

execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~ ~ ~ ~-27 ~ ~-27 minecraft:air
kill @e[type=minecraft:marker,tag=ajjnn.canvas]

execute align xyz run summon minecraft:marker ~13 ~ ~13 {Tags:["ajjnn.canvas"]}

tp @s ~ ~30 ~

execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~ ~ ~ ~-27 ~ ~-27 minecraft:white_wool
execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~-4 ~ ~-4 ~-23 ~ ~-23 minecraft:white_concrete

execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~-13 ~ ~ ~-14 ~ ~-2 minecraft:light_gray_wool
execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~-12 ~ ~-1 ~-15 ~ ~-2 minecraft:light_gray_wool
execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~-11 ~ ~-2 ~-16 ~ ~-2 minecraft:light_gray_wool

tellraw @a {"text":"Placed canvas"}