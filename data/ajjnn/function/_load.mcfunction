execute unless data storage ajjnn:data version run return fail

function ajjnn:general/clear_schedules

data modify storage ajjnn:data in set value []
data modify storage ajjnn:data modules set value []
data modify storage ajjnn:data out set value []
data modify storage ajjnn:data status set value 0b
data modify storage ajjnn:data values set value []

$function ajjnn:model/$(model)

execute if data storage ajjnn:data {modules:[]} run return fail