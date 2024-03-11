schedule clear ajjnn:nn/layers/forward
schedule clear ajjnn:nn/demo/forward

scoreboard objectives add ajjnn dummy
scoreboard objectives add ajjnn.canvas minecraft.used:minecraft.carrot_on_a_stick

data modify storage ajjnn:nn name set value ""
data modify storage ajjnn:nn parameters set value 0
data modify storage ajjnn:nn status set value 0b
data modify storage ajjnn:nn input set value []
data modify storage ajjnn:nn sequence set value []
data modify storage ajjnn:nn output set value []

tellraw @a [{"text":"Installed "},{"text":"ajjnn\n","color":"gray"}]

execute as @a run function ajjnn:__copyright

tellraw @a [{"text":"\nType "},{"text":"/function ajjnn:__help","color":"green","clickEvent":{"action":"suggest_command","value":"/function ajjnn:__help"},"hoverEvent":{"action":"show_text","contents":"Click Here"}},{"text":" for help"}]