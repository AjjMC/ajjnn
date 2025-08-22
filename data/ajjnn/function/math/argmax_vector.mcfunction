scoreboard players set #max ajjnn -2147483648
scoreboard players set #count ajjnn 0
execute store result score #length ajjnn run data get storage ajjnn:data temp.math.v1

execute if score #count ajjnn < #length ajjnn run function ajjnn:math/internal/argmax_vector_elements