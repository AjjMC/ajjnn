schedule clear ajjnn:control/demo/forward
schedule clear ajjnn:control/layers/forward
schedule clear ajjnn:control/layers/finish
schedule clear ajjnn:control/math/transform_vector_elements

scoreboard objectives add ajjnn dummy

data modify storage ajjnn:data name set value ""
data modify storage ajjnn:data parameters set value 0
data modify storage ajjnn:data status set value 0b
data modify storage ajjnn:data input set value []
data modify storage ajjnn:data sequence set value []
data modify storage ajjnn:data output set value []

function ajjnn:installation/set_version
data modify storage ajjnn:data version set from storage ajjnn:temp version

tellraw @a [{"text":"Installed "},{"text":"ajjnn","color":"gray"}]
tellraw @a [{"text":"Version: "},{"nbt":"version","storage":"ajjnn:data","color":"gray"},{"text":"\n"}]

execute as @a run function ajjnn:__copyright

tellraw @a [{"text":"\nType "},{"text":"/function ajjnn:__help","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__help"},"hoverEvent":{"action":"show_text","contents":"Click Here"}},{"text":" for help"}]