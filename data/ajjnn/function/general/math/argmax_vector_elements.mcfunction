execute store result score #x1 ajjnn run data get storage ajjnn:data temp.math.v1[0] 1000

execute if score #max ajjnn < #x1 ajjnn store result storage ajjnn:data temp.math.y int 1 run scoreboard players get #count ajjnn
execute if score #max ajjnn < #x1 ajjnn run scoreboard players operation #max ajjnn = #x1 ajjnn

data modify storage ajjnn:data temp.math.v1 append from storage ajjnn:data temp.math.v1[0]

data remove storage ajjnn:data temp.math.v1[0]

scoreboard players add #count ajjnn 1

execute if score #count ajjnn < #length ajjnn run function ajjnn:general/math/argmax_vector_elements