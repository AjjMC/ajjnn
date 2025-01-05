execute unless data storage ajjnn:data version run return fail
execute if data storage ajjnn:data {sequence:[]} run return fail
execute unless data storage ajjnn:data {status:0b} run return fail

scoreboard players set #dot_product_limit ajjnn 5
scoreboard players set #layer_count ajjnn 0
execute store result score #sequence_length ajjnn run data get storage ajjnn:data sequence

data modify storage ajjnn:data status set value 1b
data modify storage ajjnn:temp layers set from storage ajjnn:data sequence

function ajjnn:control/layers/forward