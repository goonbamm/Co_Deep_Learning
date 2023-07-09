from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
import csv
from tqdm import tqdm
import numpy as np
import nltk
nltk.download('omw-1.4')


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

def meteor_s(model):
    score = 0
    for cand, ref in (zip(model, answer_prompt)):
        cand_tokens = word_tokenize(cand)    
        ref_tokens = word_tokenize(ref)
        score  += meteor_score([ref_tokens], cand_tokens)
    return score/128

print(meteor_s(a))
print(meteor_s(b))
print(meteor_s(c))
print(meteor_s(d))
print(meteor_s(e))
print(meteor_s(g))
print(meteor_s(h))


meteor_scores = []
alpaca_translation_score = []
alpaca_conversation_score = []
alpaca_baseline_score = []

for cand, ref in tqdm(zip(alpaca_translation, answer_prompt)):
    cand_tokens = word_tokenize(cand)    
    ref_tokens = word_tokenize(ref)
    score = meteor_score([ref_tokens], cand_tokens)
    alpaca_translation_score.append(score)

for cand, ref in tqdm(zip(alpaca_conversation, answer_prompt)):
    cand_tokens = word_tokenize(cand)    
    ref_tokens = word_tokenize(ref)
    score = meteor_score([ref_tokens], cand_tokens)
    alpaca_conversation_score.append(score)

for cand, ref in tqdm(zip(alpaca_baseline, answer_prompt)):
    cand_tokens = word_tokenize(cand)    
    ref_tokens = word_tokenize(ref)
    score = meteor_score([ref_tokens], cand_tokens)
    alpaca_baseline_score.append(score)

#print(np.mean(alpaca_translation_score))
#print(np.mean(alpaca_conversation_score))
#print(np.mean(alpaca_baseline_score))