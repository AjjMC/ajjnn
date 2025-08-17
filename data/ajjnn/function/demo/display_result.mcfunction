execute if data storage ajjnn:data {model_name:"demo_digits"} run function ajjnn:demo/decode_digits
execute if data storage ajjnn:data {model_name:"demo_letters"} run function ajjnn:demo/decode_letters
execute if data storage ajjnn:data {model_name:"demo_balanced"} run function ajjnn:demo/decode_balanced

title @a actionbar [{text:"Prediction: "},{storage:"ajjnn:data",nbt:"temp.decoded",color:"yellow"}]