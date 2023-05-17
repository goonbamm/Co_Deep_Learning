f = open("./newtext.txt","w")

PROMPTS = ["ethereal Bohemian Waxwing bird,Bombycilla garrulus :: intricate details,ornate,detailed illustration,octane render :: Johanna Rupprecht style,William Morris style :: trending on artstation --ar 9:16",
           "THE CHERRY BLOSSOM TREE HOUSE :: beautiful ornate treehouse in a gigantic pink cherry blossom tree :: on a high blue grey and brown cliff with light snow and pink cherry blossom trees :: Roger Deakins and Moebius and Alphonse Much and Guweiz :: Intricate details, very realistic, cinematic lighting, volumetric lighting, photographic, --ar 9:20 --no blur bokeh defocus dof --s 4000""space suit with boots, futuristic, character design, cinematic lightning, epic fantasy, hyper realistic, detail 8k --ar 9:16",
           "character design, void arcanist, mist, photorealistic, octane render, unreal engine, hyper detailed, volumetric lighting, hdr. --ar 9:16",
           "beautiful pale cyberpunk female with heavy black eyeliner, blue eyes, shaved side haircut, hyper detail, cinematic lighting, magic neon, dark red city --ar 9:16 --testp --upbeta",
           "liquid otherworldly cool dreamy dog, cuddly, arrogant, powerful, high fantasy, epic, cinematic, internal glow --ar 2:3 --test --s 1625 --upbeta"]


for prompt in PROMPTS :
   
    f.write(prompt + "\n\n")
f.close()