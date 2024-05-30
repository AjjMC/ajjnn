data modify storage ajjnn:math x1 set from storage ajjnn:math v1[0]

function ajjnn:control/math/relu_double

data modify storage ajjnn:math v1 append from storage ajjnn:math v1[0]

data remove storage ajjnn:math v1[0]

data modify storage ajjnn:math u append from storage ajjnn:math y

scoreboard players add #count ajjnn 1

execute if score #count ajjnn < #length ajjnn run function ajjnn:control/math/relu_vector_elements