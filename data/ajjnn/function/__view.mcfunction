execute unless data storage ajjnn:data version run tellraw @s [{text:"Unable to view architecture; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
execute unless data storage ajjnn:data version run return fail

execute if data storage ajjnn:data {modules:[]} run tellraw @s {text:"Unable to view architecture; model was not found",color:"red"}
execute if data storage ajjnn:data {modules:[]} run return fail

scoreboard players set #modules_count ajjnn 0
execute store result score #modules_length ajjnn run data get storage ajjnn:data modules

tellraw @s [{text:"Name: "},{storage:"ajjnn:data",nbt:"model_name",color:"gray"}]
tellraw @s [{text:"Parameters: "},{storage:"ajjnn:data",nbt:"num_params",color:"gray"}]

execute if score #modules_count ajjnn < #modules_length ajjnn run function ajjnn:general/display/loop