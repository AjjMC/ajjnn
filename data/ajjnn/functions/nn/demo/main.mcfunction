execute as @a if score @s ajjnn.canvas matches 1.. at @s[nbt={SelectedItem:{tag:{ajjnn.brush:1b}}}] anchored eyes run function ajjnn:nn/demo/draw_canvas
execute as @a if score @s ajjnn.canvas matches 1.. at @s[nbt={SelectedItem:{tag:{ajjnn.eraser:1b}}}] anchored eyes run function ajjnn:nn/demo/erase_canvas

execute if data storage ajjnn:nn {status:1b} run title @a actionbar {"text":"RUNNING...","bold":true}
execute if data storage ajjnn:nn {status:2b} run title @a actionbar [{"text":"PREDICTED DIGIT: ","bold":true},{"storage":"ajjnn:nn","nbt":"output","color":"yellow"}]

execute as @a if score @s ajjnn.canvas matches 1.. if data storage ajjnn:nn {status:0b} run schedule function ajjnn:nn/demo/forward 1s