clear @s minecraft:carrot_on_a_stick{ajjnn.brush:1b}
clear @s minecraft:carrot_on_a_stick{ajjnn.eraser:1b}

give @s minecraft:carrot_on_a_stick{ajjnn.brush:1b,display:{Name:'{"text":"Canvas Brush","italic":false}',Lore:['{"text":"Right Click to Use","color":"yellow","italic":false}']}}
give @s minecraft:carrot_on_a_stick{ajjnn.eraser:1b,display:{Name:'{"text":"Canvas Eraser","italic":false}',Lore:['{"text":"Right Click to Use","color":"yellow","italic":false}']}}

tellraw @a [{"text":"Gave demo kit to "},{"selector":"@s"}]