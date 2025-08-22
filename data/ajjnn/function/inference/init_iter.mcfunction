data remove storage ajjnn:data temp.args

data modify storage ajjnn:data temp.module set from storage ajjnn:data temp.modules[0]

data modify storage ajjnn:data temp.math.v1 set from storage ajjnn:data temp.math.u
data modify storage ajjnn:data temp.math.v2 set from storage ajjnn:data temp.module.biases
data modify storage ajjnn:data temp.math.M set from storage ajjnn:data temp.module.weights