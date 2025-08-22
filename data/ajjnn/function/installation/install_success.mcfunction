scoreboard objectives add ajjnn dummy

execute unless data storage ajjnn:data version run data modify storage ajjnn:data in set value []
execute unless data storage ajjnn:data version run data modify storage ajjnn:data model_name set value ""
execute unless data storage ajjnn:data version run data modify storage ajjnn:data modules set value []
execute unless data storage ajjnn:data version run data modify storage ajjnn:data num_params set value 0
execute unless data storage ajjnn:data version run data modify storage ajjnn:data out set value []
execute unless data storage ajjnn:data version run data modify storage ajjnn:data status set value 0b
execute unless data storage ajjnn:data version run data modify storage ajjnn:data values set value []

function ajjnn:installation/set_version
data modify storage ajjnn:data version set from storage ajjnn:data temp.version

tellraw @a [{text:"Installed "},{text:"ajjnn",color:"gray"}]
tellraw @a [{text:"Version: "},{nbt:"version",storage:"ajjnn:data",color:"gray"},{text:"\n"}]

execute as @a run function ajjnn:__crediting

tellraw @a [{text:"\nType "},{text:"/function ajjnn:__help",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__help"},hover_event:{action:"show_text",value:"Click Here"}},{text:" for help"}]