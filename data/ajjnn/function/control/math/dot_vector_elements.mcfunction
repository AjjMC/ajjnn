execute store result score #x1 ajjnn run data get storage ajjnn:math v1[0] 1000
execute store result score #x2 ajjnn run data get storage ajjnn:math v2[0] 1000

data modify storage ajjnn:math v1 append from storage ajjnn:math v1[0]
data modify storage ajjnn:math v2 append from storage ajjnn:math v2[0]

data remove storage ajjnn:math v1[0]
data remove storage ajjnn:math v2[0]

scoreboard players operation #x1 ajjnn *= #x2 ajjnn
scoreboard players operation #sum ajjnn += #x1 ajjnn
scoreboard players add #count ajjnn 1

execute if score #count ajjnn < #length ajjnn run function ajjnn:control/math/dot_vector_elements