execute unless data storage ajjnn:data version run tellraw @s [{text:"Unable to get version; ",color:"red"},{text:"ajjnn",color:"gray"},{text:" is not installed",color:"green",click_event:{action:"suggest_command",command:"/function ajjnn:__install"},hover_event:{action:"show_text",value:"Click Here"}}]
execute unless data storage ajjnn:data version run return fail

tellraw @s {nbt:"version",storage:"ajjnn:data",color:"gray"}