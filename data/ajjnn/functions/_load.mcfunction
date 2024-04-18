execute unless data storage ajjnn:data name run return fail

data modify storage ajjnn:data input set value []
data modify storage ajjnn:data output set value []
data modify storage ajjnn:data sequence set value []

$function ajjnn:models/$(model)

execute if data storage ajjnn:data {sequence:[]} run return fail