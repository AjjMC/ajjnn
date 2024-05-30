data modify storage ajjnn:math u set value []
scoreboard players set #count ajjnn 0
execute store result score #length ajjnn run data get storage ajjnn:math v1

execute if score #count ajjnn < #length ajjnn run function ajjnn:control/math/hard_sigmoid_vector_elements