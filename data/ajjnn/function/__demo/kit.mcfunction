clear @s *[minecraft:custom_data~{ajjnn:{brush:1b}}]
clear @s *[minecraft:custom_data~{ajjnn:{eraser:1b}}]

give @s minecraft:ink_sac[minecraft:custom_data={ajjnn:{brush:1b}},minecraft:consumable={consume_seconds:2147483647},minecraft:custom_name='[{"text":"Brush","color":"green","italic":false},{"text":" (Right Click on Canvas)","color":"gray"}]']
give @s minecraft:bone_meal[minecraft:custom_data={ajjnn:{eraser:1b}},minecraft:consumable={consume_seconds:2147483647},minecraft:custom_name='[{"text":"Eraser","color":"green","italic":false},{"text":" (Right Click on Canvas)","color":"gray"}]']

tellraw @s {"text":"Gave demo kit"}