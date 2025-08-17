data modify storage ajjnn:data temp.module set from storage ajjnn:data modules[0]
data modify storage ajjnn:data temp.module_name set value "Unknown"

execute if data storage ajjnn:data {temp:{module:{type:"argmax"}}} run function ajjnn:general/display/module/argmax
execute if data storage ajjnn:data {temp:{module:{type:"hard_sigmoid"}}} run function ajjnn:general/display/module/hard_sigmoid
execute if data storage ajjnn:data {temp:{module:{type:"linear"}}} run function ajjnn:general/display/module/linear
execute if data storage ajjnn:data {temp:{module:{type:"relu"}}} run function ajjnn:general/display/module/relu

execute if data storage ajjnn:data {temp:{module_name:"Unknown"}} run function ajjnn:general/display/module/unknown

data modify storage ajjnn:data modules append from storage ajjnn:data modules[0]
data remove storage ajjnn:data modules[0]

scoreboard players add #modules_count ajjnn 1

execute if score #modules_count ajjnn < #modules_length ajjnn run function ajjnn:general/display/loop