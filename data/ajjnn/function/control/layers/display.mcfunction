data modify storage ajjnn:temp layer set from storage ajjnn:data sequence[0]
data modify storage ajjnn:temp layer_name set value "Unknown"

execute if data storage ajjnn:temp {layer:{layer:"linear"}} run data modify storage ajjnn:temp layer_name set value "Linear"
execute if data storage ajjnn:temp {layer:{layer:"relu"}} run data modify storage ajjnn:temp layer_name set value "ReLU"
execute if data storage ajjnn:temp {layer:{layer:"hard_sigmoid"}} run data modify storage ajjnn:temp layer_name set value "Hard Sigmoid"
execute if data storage ajjnn:temp {layer:{layer:"argmax"}} run data modify storage ajjnn:temp layer_name set value "Argmax"

execute if data storage ajjnn:temp layer.weights store result score #rows ajjnn run data get storage ajjnn:temp layer.weights
execute if data storage ajjnn:temp layer.weights store result score #columns ajjnn run data get storage ajjnn:temp layer.weights[0]

execute unless data storage ajjnn:temp {layer:"Unknown"} if data storage ajjnn:temp layer.weights run tellraw @s [{score:{name:"#layer_count",objective:"ajjnn"}},{text:". "},{storage:"ajjnn:temp",nbt:"layer_name",color:"red"},{text:" Layer ("},{score:{name:"#rows",objective:"ajjnn"}},{text:"x"},{score:{name:"#columns",objective:"ajjnn"}},{text:")"}]
execute unless data storage ajjnn:temp {layer:"Unknown"} unless data storage ajjnn:temp layer.weights run tellraw @s [{score:{name:"#layer_count",objective:"ajjnn"}},{text:". "},{storage:"ajjnn:temp",nbt:"layer_name",color:"blue"},{text:" Layer"}]
execute if data storage ajjnn:temp {layer:"Unknown"} run tellraw @s [{score:{name:"#layer_count",objective:"ajjnn"}},{text:". "},{storage:"ajjnn:temp",nbt:"layer_name",color:"dark_gray"},{text:" Layer"}]

data modify storage ajjnn:data sequence append from storage ajjnn:data sequence[0]
data remove storage ajjnn:data sequence[0]

scoreboard players add #layer_count ajjnn 1

execute if score #layer_count ajjnn < #sequence_length ajjnn run function ajjnn:control/layers/display