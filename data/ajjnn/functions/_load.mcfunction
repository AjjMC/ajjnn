execute unless data storage ajjnn:nn name run return fail

data modify storage ajjnn:nn input set value []
data modify storage ajjnn:nn output set value []
data modify storage ajjnn:nn sequence set value []

$function ajjnn:models/$(model)

execute if data storage ajjnn:nn {sequence:[]} run return fail