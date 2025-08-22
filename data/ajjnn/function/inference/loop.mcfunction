function ajjnn:inference/save_module_values

execute if score #modules_count ajjnn = #modules_length ajjnn run function ajjnn:inference/complete

execute if data storage ajjnn:data {status:2b} run return fail

function ajjnn:inference/init_iter

execute if data storage ajjnn:data {temp:{module:{type:"argmax"}}} run function ajjnn:inference/module/argmax
execute if data storage ajjnn:data {temp:{module:{type:"hard_sigmoid"}}} run function ajjnn:inference/module/hard_sigmoid
execute if data storage ajjnn:data {temp:{module:{type:"linear"}}} run function ajjnn:inference/module/linear
execute if data storage ajjnn:data {temp:{module:{type:"relu"}}} run function ajjnn:inference/module/relu

execute if data storage ajjnn:data {status:0b} run return fail

data modify storage ajjnn:data temp.modules append from storage ajjnn:data temp.modules[0]

data remove storage ajjnn:data temp.modules[0]

scoreboard players add #modules_count ajjnn 1

execute if score #modules_count ajjnn <= #modules_length ajjnn run function ajjnn:inference/next_module with storage ajjnn:data temp.args