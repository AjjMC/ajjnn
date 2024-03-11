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

tellraw @a [{"text":"Installed "},{"text":"ajjnn","color":"gray"}]