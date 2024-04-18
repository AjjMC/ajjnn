execute as @a if items entity @s weapon *[minecraft:custom_data~{ajjnn.brush:1b}] if score @s ajjnn.canvas matches 1.. at @s anchored eyes run function ajjnn:control/demo/draw_canvas
execute as @a if items entity @s weapon *[minecraft:custom_data~{ajjnn.eraser:1b}] if score @s ajjnn.canvas matches 1.. at @s anchored eyes run function ajjnn:control/demo/erase_canvas

execute if data storage ajjnn:data {status:1b} run title @a actionbar {"text":"RUNNING...","bold":true}
execute if data storage ajjnn:data {status:2b} run title @a actionbar [{"text":"PREDICTED DIGIT: ","bold":true},{"storage":"ajjnn:data","nbt":"output","color":"yellow"}]

execute as @a if score @s ajjnn.canvas matches 1.. if data storage ajjnn:data {status:0b} run schedule function ajjnn:control/demo/forward 1s