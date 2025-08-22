execute unless data storage ajjnn:data version run return fail
execute if data storage ajjnn:data {modules:[]} run return fail
execute unless data storage ajjnn:data {status:0b} run return fail

scoreboard players set #dot_product_limit ajjnn 5
scoreboard players set #modules_count ajjnn 0
execute store result score #modules_length ajjnn run data get storage ajjnn:data modules

data modify storage ajjnn:data status set value 1b
data modify storage ajjnn:data temp.math.u set from storage ajjnn:data in
data modify storage ajjnn:data temp.modules set from storage ajjnn:data modules
data modify storage ajjnn:data temp.values set value []

function ajjnn:inference/loop