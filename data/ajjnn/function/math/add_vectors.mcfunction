data modify storage ajjnn:data temp.math.u set value []
scoreboard players set #count ajjnn 0
execute store result score #length ajjnn run data get storage ajjnn:data temp.math.v1

execute if score #count ajjnn < #length ajjnn run function ajjnn:math/internal/add_vector_elements