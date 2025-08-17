scoreboard players set #sum ajjnn 0
scoreboard players set #count ajjnn 0
execute store result score #length ajjnn run data get storage ajjnn:data temp.math.v1

execute if score #count ajjnn < #length ajjnn run function ajjnn:general/math/dot_vector_elements

execute store result storage ajjnn:data temp.math.y double 0.000001 run scoreboard players get #sum ajjnn