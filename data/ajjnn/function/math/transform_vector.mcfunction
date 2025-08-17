data modify storage ajjnn:data temp.math.u set value []
scoreboard players set #row_count ajjnn 0
execute store result score #column_count ajjnn run data get storage ajjnn:data temp.math.M

data modify storage ajjnn:data temp.math.v3 set from storage ajjnn:data temp.math.v2

execute if score #row_count ajjnn < #column_count ajjnn run function ajjnn:general/math/transform_vector_elements