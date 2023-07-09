from rouge import Rouge
import csv
from tqdm import tqdm
import numpy as np 

answer_prompt = []
alpaca_translation = []
alpaca_conversation = []
alpaca_baseline = []
a = []
b = []
c = []
d = []
e = []
g = []
h = []
j = []
f = open('record.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

count = 0
for line in rdr:
    if not count == 0 :       
        answer_prompt.append(line[0])
        a.append(line[2])
        b.append(line[4])
        c.append(line[5])
        d.append(line[6])
        e.append(line[8])
        g.append(line[9])
        h.append(line[10])    
        alpaca_baseline.append(line[-1])
        alpaca_translation.append(line[3])
        alpaca_conversation.append(line[7])    
    count += 1     
f.close()   

def rouge_s(model, answer) :
    rouge = Rouge()
    return rouge.get_scores(model,answer,avg=True)["rouge-1"]

bleu_scores = []
alpaca_translation_score = []
alpaca_conversation_score = []
alpaca_baseline_score = []

rouge = Rouge()
score = rouge.get_scores(alpaca_translation,answer_prompt,avg=True)["rouge-1"]
rouge = Rouge()
score = rouge.get_scores(alpaca_conversation,answer_prompt,avg=True)["rouge-1"]
rouge = Rouge()
score = rouge.get_scores(alpaca_baseline,answer_prompt,avg=True)["rouge-1"]

print(rouge_s(a,answer_prompt))
print(rouge_s(b,answer_prompt))
print(rouge_s(c,answer_prompt))
print(rouge_s(d,answer_prompt))
print(rouge_s(e,answer_prompt))
print(rouge_s(g,answer_prompt))
print(rouge_s(h,answer_prompt))


