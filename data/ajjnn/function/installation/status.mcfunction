execute unless data storage ajjnn:data version run tellraw @a [{text:"ajjnn",color:"gray"},{text:" is not installed",color:"red"}]
execute unless data storage ajjnn:data version run tellraw @a [{text:"Type "},{text:"/function ajjnn:__install",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}},{text:" to install"}]

function ajjnn:installation/set_version

scoreboard objectives add ajjnn.temp dummy

execute store success score #temp ajjnn.temp run data modify storage ajjnn:data temp.version set from storage ajjnn:data version
execute if data storage ajjnn:data version if score #temp ajjnn.temp matches 1 run function ajjnn:__install
execute if data storage ajjnn:data version if score #temp ajjnn.temp matches 1 run tellraw @a [{text:"\nUpdated "},{text:"ajjnn",color:"gray"},{text:" to version "},{nbt:"version",storage:"ajjnn:data",color:"gray"}]

scoreboard players reset #temp ajjnn.temp
scoreboard objectives remove ajjnn.temp
data remove storage ajjnn:data temp.version