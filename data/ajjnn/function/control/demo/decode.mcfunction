execute if data storage ajjnn:data {name:"demo_digits"} run function ajjnn:control/demo/decode_digits
execute if data storage ajjnn:data {name:"demo_letters"} run function ajjnn:control/demo/decode_letters
execute if data storage ajjnn:data {name:"demo_balanced"} run function ajjnn:control/demo/decode_balanced

title @a actionbar [{"text":"PREDICTION: ","bold":true},{"storage":"ajjnn:temp","nbt":"decoded","color":"yellow"}]