data modify storage ajjnn:data temp.math.v2 set from storage ajjnn:data temp.math.M[0]

function ajjnn:math/dot_vectors

data modify storage ajjnn:data temp.math.x1 set from storage ajjnn:data temp.math.y
data modify storage ajjnn:data temp.math.x2 set from storage ajjnn:data temp.math.v3[0]

function ajjnn:math/add_doubles

data modify storage ajjnn:data temp.math.M append from storage ajjnn:data temp.math.M[0]
data modify storage ajjnn:data temp.math.v3 append from storage ajjnn:data temp.math.v3[0]

data remove storage ajjnn:data temp.math.M[0]
data remove storage ajjnn:data temp.math.v3[0]

data modify storage ajjnn:data temp.math.u append from storage ajjnn:data temp.math.y

scoreboard players add #row_count ajjnn 1

scoreboard players operation #count ajjnn = #row_count ajjnn
scoreboard players operation #count ajjnn %= #dot_product_limit ajjnn

execute if score #row_count ajjnn < #column_count ajjnn if score #count ajjnn matches 0 run schedule function ajjnn:general/math/transform_vector_elements 1t
execute if score #row_count ajjnn < #column_count ajjnn unless score #count ajjnn matches 0 run function ajjnn:general/math/transform_vector_elements