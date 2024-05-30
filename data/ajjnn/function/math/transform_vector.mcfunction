data modify storage ajjnn:math u set value []
scoreboard players set #row_count ajjnn 0
execute store result score #column_count ajjnn run data get storage ajjnn:math M

data modify storage ajjnn:math b set from storage ajjnn:math v2

execute if score #row_count ajjnn < #column_count ajjnn run function ajjnn:control/math/transform_vector_elements