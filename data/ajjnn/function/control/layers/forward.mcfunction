execute if score #layer_count ajjnn matches 0 run data modify storage ajjnn:math u set from storage ajjnn:data input

data modify storage ajjnn:math v1 set from storage ajjnn:math u
data modify storage ajjnn:math v2 set from storage ajjnn:temp layers[0].biases
data modify storage ajjnn:math M set from storage ajjnn:temp layers[0].weights

data modify storage ajjnn:temp layer set from storage ajjnn:temp layers[0]

execute if data storage ajjnn:temp layer.weights store result score #input_rows ajjnn run data get storage ajjnn:math u
execute if data storage ajjnn:temp layer.weights store result score #rows ajjnn run data get storage ajjnn:temp layer.weights
execute if data storage ajjnn:temp layer.weights store result score #columns ajjnn run data get storage ajjnn:temp layer.weights[0]

execute if data storage ajjnn:temp layer.weights unless score #input_rows ajjnn = #columns ajjnn run tellraw @a [{text:"Mismatch at layer ",color:"red"},{score:{name:"#layer_count",objective:"ajjnn"}},{text:"; "},{score:{name:"#input_rows",objective:"ajjnn"}},{text:" != "},{score:{name:"#columns",objective:"ajjnn"}}]
execute if data storage ajjnn:temp layer.weights unless score #input_rows ajjnn = #columns ajjnn run function ajjnn:control/layers/finish
execute if data storage ajjnn:data {status:0b} run return fail

data remove storage ajjnn:temp argument
execute unless data storage ajjnn:temp layer.weights run data modify storage ajjnn:temp argument.ticks set value 0
execute if data storage ajjnn:temp layer.weights run scoreboard players operation #rows ajjnn += #dot_product_limit ajjnn
execute if data storage ajjnn:temp layer.weights store result storage ajjnn:temp argument.ticks int 1 run scoreboard players operation #rows ajjnn /= #dot_product_limit ajjnn

execute if data storage ajjnn:temp {layer:{layer:"linear"}} run function ajjnn:layers/linear
execute if data storage ajjnn:temp {layer:{layer:"relu"}} run function ajjnn:layers/relu
execute if data storage ajjnn:temp {layer:{layer:"hard_sigmoid"}} run function ajjnn:layers/hard_sigmoid
execute if data storage ajjnn:temp {layer:{layer:"argmax"}} run function ajjnn:layers/argmax

data modify storage ajjnn:temp layers append from storage ajjnn:temp layers[0]

data remove storage ajjnn:temp layers[0]

scoreboard players add #layer_count ajjnn 1

execute if score #layer_count ajjnn = #sequence_length ajjnn run data modify storage ajjnn:data output set from storage ajjnn:math y
execute if score #layer_count ajjnn = #sequence_length ajjnn run data modify storage ajjnn:data status set value 2b
execute if score #layer_count ajjnn = #sequence_length ajjnn run schedule function ajjnn:control/layers/finish 1t

execute if score #layer_count ajjnn < #sequence_length ajjnn run function ajjnn:control/layers/next with storage ajjnn:temp argument