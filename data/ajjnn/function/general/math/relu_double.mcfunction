execute store result score #x1 ajjnn run data get storage ajjnn:data temp.math.x1 1000

execute if score #x1 ajjnn matches 1.. run data modify storage ajjnn:data temp.math.y set from storage ajjnn:data temp.math.x1
execute if score #x1 ajjnn matches ..0 run data modify storage ajjnn:data temp.math.y set value 0.0