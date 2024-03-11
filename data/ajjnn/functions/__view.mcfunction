execute unless data storage ajjnn:nn name run tellraw @s [{"text":"Unable to view architecture; ","color":"red"},{"text":"ajjnn","color":"gray"},{"text":" is not installed","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__install"},"hoverEvent":{"action":"show_text","contents":"Click Here"}}]
execute unless data storage ajjnn:nn name run return fail

execute if data storage ajjnn:nn {sequence:[]} run tellraw @s {"text":"Unable to view architecture; model was not found","color":"red"}
execute if data storage ajjnn:nn {sequence:[]} run return fail

scoreboard players set #layer_count ajjnn 0
execute store result score #sequence_length ajjnn run data get storage ajjnn:nn sequence

tellraw @s [{"text":"Name: "},{"storage":"ajjnn:nn","nbt":"name","color":"gray"}]
tellraw @s [{"text":"Parameters: "},{"storage":"ajjnn:nn","nbt":"parameters","color":"gray"}]

execute if score #layer_count ajjnn < #sequence_length ajjnn run function ajjnn:nn/layers/display