execute unless data storage ajjnn:data version run tellraw @s [{text:""},{text:"Unable to place the demo canvas; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not ",color:"red"},{text:"installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
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

tellraw @a {text:"Placed demo canvas"}