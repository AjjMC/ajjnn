data modify storage ajjnn:data temp.module_name set value "Linear"
execute store result score #rows_length ajjnn run data get storage ajjnn:data temp.module.weights
execute store result score #columns_length ajjnn run data get storage ajjnn:data temp.module.weights[0]
tellraw @s [{score:{name:"#modules_count",objective:"ajjnn"}},{text:". "},{storage:"ajjnn:data",nbt:"temp.module_name",color:"red"},{text:" Module ("},{score:{name:"#rows_length",objective:"ajjnn"}},{text:"x"},{score:{name:"#columns_length",objective:"ajjnn"}},{text:")"}]