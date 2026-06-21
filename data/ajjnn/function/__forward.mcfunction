execute unless data storage ajjnn:data version run tellraw @s [{text:""},{text:"Unable to perform the forward pass; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not ",color:"red"},{text:"installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
execute unless data storage ajjnn:data version run function ajjnn:general/display_feedback_message
execute unless data storage ajjnn:data version run return fail

execute if data storage ajjnn:data {modules:[]} run tellraw @s {text:"Unable to perform the forward pass; the model is not loaded",color:"red"}
execute if data storage ajjnn:data {modules:[]} run function ajjnn:general/display_feedback_message
execute if data storage ajjnn:data {modules:[]} run return fail

execute unless data storage ajjnn:data {status:0b} run tellraw @s [{text:"Unable to perform the forward pass; the model is currently running",color:"red"}]
execute unless data storage ajjnn:data {status:0b} run function ajjnn:general/display_feedback_message
execute unless data storage ajjnn:data {status:0b} run return fail

tellraw @a {text:"Performing forward pass..."}

function ajjnn:_forward

execute as @a run function ajjnn:general/display_feedback_message