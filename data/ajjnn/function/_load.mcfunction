execute unless data storage ajjnn:data version run return fail

function ajjnn:control/clear_schedules
data modify storage ajjnn:data status set value 0b

data modify storage ajjnn:data input set value []
data modify storage ajjnn:data output set value []
data modify storage ajjnn:data sequence set value []

$function ajjnn:models/$(model)

execute if data storage ajjnn:data {sequence:[]} run return fail