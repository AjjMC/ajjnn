scoreboard players set #sum ajjnn 0
scoreboard players set #count ajjnn 0
execute store result score #length ajjnn run data get storage ajjnn:math v1

execute if score #count ajjnn < #length ajjnn run function ajjnn:control/math/dot_vector_elements

execute store result storage ajjnn:math y double 0.000001 run scoreboard players get #sum ajjnn