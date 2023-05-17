import openai
import time
import copy

# gpt-turbo api key

PROMPTS = ["ethereal Bohemian Waxwing bird,Bombycilla garrulus :: intricate details,ornate,detailed illustration,octane render :: Johanna Rupprecht style,William Morris style :: trending on artstation --ar 9:16",
           "THE CHERRY BLOSSOM TREE HOUSE :: beautiful ornate treehouse in a gigantic pink cherry blossom tree :: on a high blue grey and brown cliff with light snow and pink cherry blossom trees :: Roger Deakins and Moebius and Alphonse Much and Guweiz :: Intricate details, very realistic, cinematic lighting, volumetric lighting, photographic, --ar 9:20 --no blur bokeh defocus dof --s 4000""space suit with boots, futuristic, character design, cinematic lightning, epic fantasy, hyper realistic, detail 8k --ar 9:16",
           "character design, void arcanist, mist, photorealistic, octane render, unreal engine, hyper detailed, volumetric lighting, hdr. --ar 9:16",
           "beautiful pale cyberpunk female with heavy black eyeliner, blue eyes, shaved side haircut, hyper detail, cinematic lighting, magic neon, dark red city --ar 9:16 --testp --upbeta",
           "liquid otherworldly cool dreamy dog, cuddly, arrogant, powerful, high fantasy, epic, cinematic, internal glow --ar 2:3 --test --s 1625 --upbeta"]

def Make_scinario(prompt,tmp):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "system", "content": "예시 시나리오와 비슷하게 target prompt를 만드는 최적의 시나리오를 만드는 AI 모델"},
            {"role": "user", "content": '다음의 예시는 이미지 생성 모델에 아이가 명령을 하고 이미지 생성 모델이 아이의 명령에 맞춰서 적절한 영어 prompt를 생성하는 예시야.\
                                        아이는 한번 명령을 내릴 때마다 생성된 이미지를 확인할 수 있고, 아이가 다시 피드백을 할 때마다 이미지 생성 모델은 아이의 피드백을 반영하여 수정된 prompt를 생성해줘.\
                                        예시 시나리오: \
                                        아이: 셰익스피어 연극 무대 같은 그림을 그려봐. 그리고 황금빛 안개로 분위기를 내고 싶어.\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric"\
                                        아이: 그럼 무대 디자인은 저번에 본 거처럼, 그리고 공중에서 돌아다니는 사람들이 있는 느낌도 넣어줘.\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric, set design by Michel Crête, Aerial acrobatics design by André Simard"\
                                        아이: 와, 그게 무슨 느낌일지 상상이 가! 그런데 그림이 더 진짜 같았으면 좋겠어. 아주 아주 진짜같이 그리면 어때?\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric, set design by Michel Crête, Aerial acrobatics design by André Simard, hyperrealistic"\
                                        아이: 그리고 그림이 아주 아주 선명하게 보이면 좋겠어. 그리고 그거처럼 컴퓨터로 만든 그림같이 그려보는 건 어때?\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric, set design by Michel Crête, Aerial acrobatics design by André Simard, hyperrealistic,\
                                        4K, Octane render, unreal engine"\
                                        아이: 그림 비율은 핸드폰 화면에 잘 맞게 해서, 위에서 빛이 비춰지는 걸로 해서 더 독특한 분위기를 내봐.\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric, set design by Michel Crête, Aerial acrobatics design by André Simard, hyperrealistic,\
                                        4K, Octane render, unreal engine, –ar 9:16 –uplight"\
                                        아이: 아 확인해보니까 초현실적인 느낌은 안어울리는거 같아. 빼줘.\
                                        "Model: a Shakespeare stage play, yellow mist, atmospheric, set design by Michel Crête, Aeria acrobatics design by André Simard,\
                                        4K, Octane render, unreal engine, –ar 9:16 –uplight"'},            
             {"role": "user", "content": f"자 지금까지의 대화와 아래의 조건을 바탕으로 아이가 명령을 내리면 최종적으로 {prompt}를 AI가 생성하는 시나리오를 내가 준 예시 시나리오의 형식으로 만들어줘.\
             조건:\
             1.아이는 한국어만을 사용하여 명령 해, 모델은 영어 prompt만으로 답변 해(아이와 상호작용할 필요 없이 영어 prompt 결과만을 답변해)\
             2.아이의 지식수준은 10살 아래라고 가정해. 아이는 어려운 단어를 사용하지 않아.\
             3.발화의 개수는 6개 이상으로 해야 해.\
             4.아이는 한번에 최대 2개의 조건을 말할 수 있어."},],
        temperature=tmp)
    return response['choices'][0]['message']['content']



f = open("./newtext1.txt","w", encoding="utf-8")

for prompt in PROMPTS :
   scinario = Make_scinario(prompt,0.5)
   print("-" * 100)
   print(scinario)
   print("-" * 100)
   f.write(scinario + "\n----------------------------------------------------\n")

f.close()

