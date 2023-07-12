import csv
f = open('dataset.csv','r',encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    print(line)
f.close()