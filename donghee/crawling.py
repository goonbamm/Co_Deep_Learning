from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
import pandas as pd

COLUMNS = ['PROMPT','IMAGE_URL']
df = pd.DataFrame(columns=COLUMNS)
midjournery_prompt_image_pair = pd.read_csv("./dataset.csv",encoding="utf-8",index_col=0)
df = pd.concat([df,midjournery_prompt_image_pair])
req = Request("https://www.midjourney.com/showcase/recent/",headers={'User-Agent':'Mozilla/5.0'})
html = urlopen(req).read()
bsObject = BeautifulSoup(html, "html.parser")
bsStr = str(bsObject)
memory = dict()

IMAGE_URL = "seedImageURL"
FULL_COMMAND = "full_command"
image_count = 0
command_count = 0
image = ""
prompt = ""

for i in range(len(bsStr)) :
    if bsStr[i] == IMAGE_URL[image_count] :
        image_count += 1
        if image_count == len(IMAGE_URL) :
            imageurl_index = i+4
            while True :
                if bsStr[imageurl_index] == '"' :
                    break
                image += bsStr[imageurl_index] 
                imageurl_index += 1                
            i = imageurl_index
            image_count = 0
    else : image_count = 0
    
    if bsStr[i] == FULL_COMMAND[command_count] :
        command_count += 1
        if command_count == len(FULL_COMMAND) :
            fullcommand_index = i+4
            while True :
                if bsStr[fullcommand_index] == '"' :
                    break
                prompt += bsStr[fullcommand_index] 
                fullcommand_index += 1
            i = fullcommand_index
            command_count = 0
            # dict 형태로 저장
            memory[prompt] = image
            image = ""
            prompt = ""
    else : command_count = 0

for prompt,image in memory.items():
    newDF = list()
    newDF.append(prompt)
    newDF.append(image)
    newDF = pd.DataFrame(data=[newDF], columns = COLUMNS)
    if len(df.loc[(df['PROMPT'] == prompt)]) == 0:
        df = pd.concat([df,newDF])

df.to_csv("dataset.csv")