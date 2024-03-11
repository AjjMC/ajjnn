execute unless data storage ajjnn:nn name run tellraw @s [{"text":"Unable to load model; ","color":"red"},{"text":"ajjnn","color":"gray"},{"text":" is not installed","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__install"},"hoverEvent":{"action":"show_text","contents":"Click Here"}}]
execute unless data storage ajjnn:nn name run return fail

data remove storage ajjnn:temp argument
$data modify storage ajjnn:temp argument.model set value $(model)
function ajjnn:_load with storage ajjnn:temp argument

execute if data storage ajjnn:nn {sequence:[]} run tellraw @s {"text":"Unable to load model; model was not found","color":"red"}
execute if data storage ajjnn:nn {sequence:[]} run return fail

tellraw @a {"text":"Loaded PyTorch model"}

function ajjnn:__view