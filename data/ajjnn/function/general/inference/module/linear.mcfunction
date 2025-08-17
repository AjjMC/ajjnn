execute store result score #in_rows_length ajjnn run data get storage ajjnn:data temp.math.u
execute store result score #rows_length ajjnn run data get storage ajjnn:data temp.module.weights
execute store result score #columns_length ajjnn run data get storage ajjnn:data temp.module.weights[0]
execute unless score #in_rows_length ajjnn = #columns_length ajjnn run tellraw @a [{text:"Mismatch at module ",color:"red"},{score:{name:"#modules_count",objective:"ajjnn"}},{text:"; "},{score:{name:"#in_rows_length",objective:"ajjnn"}},{text:" != "},{score:{name:"#columns_length",objective:"ajjnn"}}]
execute unless score #in_rows_length ajjnn = #columns_length ajjnn run function ajjnn:general/inference/end
scoreboard players operation #rows_length ajjnn += #dot_product_limit ajjnn
execute store result storage ajjnn:data temp.args.ticks int 1 run scoreboard players operation #rows_length ajjnn /= #dot_product_limit ajjnn
function ajjnn:math/transform_vector