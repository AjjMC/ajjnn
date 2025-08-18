execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~ ~ ~ ~-27 ~ ~-27 minecraft:air
kill @e[type=minecraft:marker,tag=ajjnn.canvas]

function ajjnn:general/clear_schedules

scoreboard players reset #column_count ajjnn
scoreboard players reset #columns_length ajjnn
scoreboard players reset #constant ajjnn
scoreboard players reset #count ajjnn
scoreboard players reset #dot_product_limit ajjnn
scoreboard players reset #in_rows_length ajjnn
scoreboard players reset #length ajjnn
scoreboard players reset #max ajjnn
scoreboard players reset #modules_count ajjnn
scoreboard players reset #modules_length ajjnn
scoreboard players reset #position ajjnn
scoreboard players reset #row_count ajjnn
scoreboard players reset #rows_length ajjnn
scoreboard players reset #sum ajjnn
scoreboard players reset #x1 ajjnn
scoreboard players reset #x2 ajjnn

scoreboard objectives remove ajjnn

data remove storage ajjnn:data in
data remove storage ajjnn:data model_name
data remove storage ajjnn:data modules
data remove storage ajjnn:data num_params
data remove storage ajjnn:data out
data remove storage ajjnn:data status
data remove storage ajjnn:data values
data remove storage ajjnn:data version

tellraw @a [{text:"Uninstalled "},{text:"ajjnn",color:"gray"}]