data modify storage ajjnn:data values set from storage ajjnn:data temp.values
data modify storage ajjnn:data out set from storage ajjnn:data values[-1]
data modify storage ajjnn:data status set value 2b

schedule function ajjnn:inference/end 1t