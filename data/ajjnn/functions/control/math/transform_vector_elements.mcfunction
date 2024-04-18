data modify storage ajjnn:math v2 set from storage ajjnn:math M[0]

function ajjnn:math/dot_vectors

data modify storage ajjnn:math M append from storage ajjnn:math M[0]
data modify storage ajjnn:math b append from storage ajjnn:math b[0]
data modify storage ajjnn:math x1 set from storage ajjnn:math b[0]

data remove storage ajjnn:math M[0]
data remove storage ajjnn:math b[0]

data modify storage ajjnn:math x2 set from storage ajjnn:math y

function ajjnn:math/add_doubles

data modify storage ajjnn:math u append from storage ajjnn:math y

scoreboard players add #row_count ajjnn 1

scoreboard players operation #count ajjnn = #row_count ajjnn
scoreboard players operation #count ajjnn %= #dot_product_limit ajjnn

execute if score #row_count ajjnn < #column_count ajjnn if score #count ajjnn matches 0 run schedule function ajjnn:control/math/transform_vector_elements 1t
execute if score #row_count ajjnn < #column_count ajjnn unless score #count ajjnn matches 0 run function ajjnn:control/math/transform_vector_elements