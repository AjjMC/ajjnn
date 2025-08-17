execute unless data storage ajjnn:data version run tellraw @s [{text:"Unable to load model; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
execute unless data storage ajjnn:data version run tellraw @s {text:"(Use a single underscore to hide feedback)",color:"yellow"}
execute unless data storage ajjnn:data version run return fail

data remove storage ajjnn:data temp.args
$data modify storage ajjnn:data temp.args.model set value $(model)
function ajjnn:_load with storage ajjnn:data temp.args

execute if data storage ajjnn:data {modules:[]} run tellraw @s {text:"Unable to load model; model was not found",color:"red"}
execute if data storage ajjnn:data {modules:[]} run tellraw @s {text:"(Use a single underscore to hide feedback)",color:"yellow"}
execute if data storage ajjnn:data {modules:[]} run return fail

tellraw @a {text:"Loaded PyTorch model"}

function ajjnn:__view

tellraw @a {text:"(Use a single underscore to hide feedback)",color:"yellow"}