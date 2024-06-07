execute if data storage ajjnn:data {name:"demo_mnist"} run function ajjnn:control/demo/decode_mnist
execute if data storage ajjnn:data {name:"demo_emnist_letters"} run function ajjnn:control/demo/decode_emnist_letters

title @a actionbar [{"text":"PREDICTED DIGIT: ","bold":true},{"storage":"ajjnn:temp","nbt":"decoded","color":"yellow"}]