execute unless data storage ajjnn:data version run tellraw @s [{text:"Unable to load model; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
execute unless data storage ajjnn:data version run tellraw @s {text:"(Use a single underscore to hide feedback)",color:"yellow"}
execute unless data storage ajjnn:data version run return fail

data remove storage ajjnn:temp argument
$data modify storage ajjnn:temp argument.model set value $(model)
function ajjnn:_load with storage ajjnn:temp argument

execute if data storage ajjnn:data {sequence:[]} run tellraw @s {text:"Unable to load model; model was not found",color:"red"}
execute if data storage ajjnn:data {sequence:[]} run tellraw @s {text:"(Use a single underscore to hide feedback)",color:"yellow"}
execute if data storage ajjnn:data {sequence:[]} run return fail

tellraw @a {text:"Loaded PyTorch model"}

function ajjnn:__view

tellraw @a {text:"(Use a single underscore to hide feedback)",color:"yellow"}