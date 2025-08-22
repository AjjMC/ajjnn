data modify storage ajjnn:data temp.math.x1 set from storage ajjnn:data temp.math.v1[0]
data modify storage ajjnn:data temp.math.x2 set from storage ajjnn:data temp.math.v2[0]

function ajjnn:math/add_doubles

data modify storage ajjnn:data temp.math.v1 append from storage ajjnn:data temp.math.v1[0]
data modify storage ajjnn:data temp.math.v2 append from storage ajjnn:data temp.math.v2[0]

data remove storage ajjnn:data temp.math.v1[0]
data remove storage ajjnn:data temp.math.v2[0]

data modify storage ajjnn:data temp.math.u append from storage ajjnn:data temp.math.y

scoreboard players add #count ajjnn 1

execute if score #count ajjnn < #length ajjnn run function ajjnn:math/internal/add_vector_elements