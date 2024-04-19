clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{ajjnn.brush:1b}]
clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{ajjnn.eraser:1b}]

give @s minecraft:carrot_on_a_stick[minecraft:custom_data={ajjnn.brush:1b},minecraft:custom_name='{"text":"Canvas Brush","italic":false}',minecraft:lore=['{"text":"Right click to use","color":"yellow","italic":false}']]
give @s minecraft:carrot_on_a_stick[minecraft:custom_data={ajjnn.eraser:1b},minecraft:custom_name='{"text":"Canvas Eraser","italic":false}',minecraft:lore=['{"text":"Right click to use","color":"yellow","italic":false}']]

tellraw @s {"text":"Gave demo kit"}