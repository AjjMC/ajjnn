execute store result score #x1 ajjnn run data get storage ajjnn:data temp.math.x1 1000

execute if score #x1 ajjnn matches ..-3000 run data modify storage ajjnn:data temp.math.y set value 0.0
execute if score #x1 ajjnn matches 3000.. run data modify storage ajjnn:data temp.math.y set value 1.0

execute if score #x1 ajjnn matches -2999..2999 run scoreboard players set #constant ajjnn 6
execute if score #x1 ajjnn matches -2999..2999 run scoreboard players operation #x1 ajjnn /= #constant ajjnn
execute if score #x1 ajjnn matches -2999..2999 run scoreboard players set #constant ajjnn 500
execute if score #x1 ajjnn matches -2999..2999 run scoreboard players operation #x1 ajjnn += #constant ajjnn
execute if score #x1 ajjnn matches -2999..2999 store result storage ajjnn:data temp.math.y double 0.001 run scoreboard players get #x1 ajjnn