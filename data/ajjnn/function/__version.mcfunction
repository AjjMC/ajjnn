execute unless data storage ajjnn:data version run tellraw @s [{"text":"Unable to get version; ","color":"red"},{"text":"ajjnn","color":"gray"},{"text":" is not installed","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__install"},"hoverEvent":{"action":"show_text","contents":"Click Here"}}]
execute unless data storage ajjnn:data version run return fail

tellraw @s {"nbt":"version","storage":"ajjnn:data","color":"gray"}