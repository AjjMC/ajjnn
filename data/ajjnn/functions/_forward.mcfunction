execute unless data storage ajjnn:nn name run return fail
execute if data storage ajjnn:nn {sequence:[]} run return fail
execute unless data storage ajjnn:nn {status:0b} run return fail

scoreboard players set #dot_product_limit ajjnn 4
scoreboard players set #layer_count ajjnn 0
execute store result score #sequence_length ajjnn run data get storage ajjnn:nn sequence

data modify storage ajjnn:nn status set value 1b
data modify storage ajjnn:temp layers set from storage ajjnn:nn sequence

function ajjnn:nn/layers/forward