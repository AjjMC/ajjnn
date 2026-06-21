clear @s *[minecraft:custom_data~{ajjnn:{brush:1b}}]
clear @s *[minecraft:custom_data~{ajjnn:{eraser:1b}}]

give @s minecraft:ink_sac[minecraft:custom_data={ajjnn:{brush:1b}},minecraft:consumable={consume_seconds:2147483647f},minecraft:use_effects={can_sprint:true,speed_multiplier:1f},minecraft:item_name=[{text:"Brush",color:"green"},{text:" (Right Click on Canvas)",color:"gray"}]]
give @s minecraft:bone_meal[minecraft:custom_data={ajjnn:{eraser:1b}},minecraft:consumable={consume_seconds:2147483647f},minecraft:use_effects={can_sprint:true,speed_multiplier:1f},minecraft:item_name=[{text:"Eraser",color:"green"},{text:" (Right Click on Canvas)",color:"gray"}]]

tellraw @s {text:"Gave demo kit"}