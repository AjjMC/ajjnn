execute unless data storage ajjnn:data version run tellraw @s [{"text":"Unable perform forward pass; ","color":"red"},{"text":"ajjnn","color":"gray"},{"text":" is not installed","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__install"},"hoverEvent":{"action":"show_text","contents":"Click Here"}}]
execute unless data storage ajjnn:data version run tellraw @s {"text":"(Use a single underscore to hide feedback)","color":"yellow"}
execute unless data storage ajjnn:data version run return fail

execute if data storage ajjnn:data {sequence:[]} run tellraw @s {"text":"Unable to perform forward pass; model was not found","color":"red"}
execute if data storage ajjnn:data {sequence:[]} run tellraw @s {"text":"(Use a single underscore to hide feedback)","color":"yellow"}
execute if data storage ajjnn:data {sequence:[]} run return fail

execute unless data storage ajjnn:data {status:0b} run tellraw @s [{"text":"Unable to perform forward pass; model is currently running","color":"red"}]
execute unless data storage ajjnn:data {status:0b} run tellraw @s {"text":"(Use a single underscore to hide feedback)","color":"yellow"}
execute unless data storage ajjnn:data {status:0b} run return fail

tellraw @a {"text":"Performing forward pass..."}

function ajjnn:_forward

tellraw @a {"text":"(Use a single underscore to hide feedback)","color":"yellow"}