execute at @e[type=minecraft:marker,tag=ajjnn.canvas] run fill ~ ~ ~ ~-27 ~ ~-27 minecraft:air
kill @e[type=minecraft:marker,tag=ajjnn.canvas]

function ajjnn:control/clear_schedules

scoreboard players reset #column_count ajjnn
scoreboard players reset #columns ajjnn
scoreboard players reset #constant ajjnn
scoreboard players reset #count ajjnn
scoreboard players reset #dot_product_limit ajjnn
scoreboard players reset #finish ajjnn
scoreboard players reset #input_rows ajjnn
scoreboard players reset #layer_count ajjnn
scoreboard players reset #length ajjnn
scoreboard players reset #max ajjnn
scoreboard players reset #position ajjnn
scoreboard players reset #row_count ajjnn
scoreboard players reset #rows ajjnn
scoreboard players reset #sequence_length ajjnn
scoreboard players reset #sum ajjnn

scoreboard objectives remove ajjnn

data remove storage ajjnn:data input
data remove storage ajjnn:data name
data remove storage ajjnn:data output
data remove storage ajjnn:data parameters
data remove storage ajjnn:data sequence
data remove storage ajjnn:data status
data remove storage ajjnn:data version

data remove storage ajjnn:math b
data remove storage ajjnn:math M
data remove storage ajjnn:math u
data remove storage ajjnn:math v1
data remove storage ajjnn:math v2
data remove storage ajjnn:math x1
data remove storage ajjnn:math x2
data remove storage ajjnn:math y

data remove storage ajjnn:temp argument
data remove storage ajjnn:temp decoded
data remove storage ajjnn:temp layer
data remove storage ajjnn:temp layer_name
data remove storage ajjnn:temp layers
data remove storage ajjnn:temp version

tellraw @a [{"text":"Uninstalled "},{"text":"ajjnn","color":"gray"}]