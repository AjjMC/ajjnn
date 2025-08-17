execute store result score #x1 ajjnn run data get storage ajjnn:data temp.math.x1 1000
execute store result score #x2 ajjnn run data get storage ajjnn:data temp.math.x2 1000

scoreboard players operation #x1 ajjnn += #x2 ajjnn

execute store result storage ajjnn:data temp.math.y double 0.001 run scoreboard players get #x1 ajjnn