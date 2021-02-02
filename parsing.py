#! /usr/bin/env python

# Modules
import os
import html
import re
import xml.etree.ElementTree as ET
import operator
import matplotlib.pyplot as plt
import numpy as np
import parsing_def as ps

## 1. output cid list
f = open('XML/log_output','r')
cid_list = f.readlines()
f.close()

## 2. total tox infos
total_tox = []

for cid in cid_list:
    name, tox = ps.load_poison_info(int(cid))
    total_tox += [ [cid,info.lower()] for info in tox ]


## 2-1. 
lc50_tox = ps.word_tox_list("lc50", total_tox)
ec50_tox = ps.word_tox_list("ec50", total_tox)
daphnia_tox = ps.word_tox_list("daphnia", total_tox)

print("# of chemicals : ", len(cid_list))
print("total : ", len(total_tox))
print("lc50 : ",len(lc50_tox))
print("ec50 : ",len(lc50_tox))
print("daphnia : ",len(daphnia_tox))

## 2-2. # of chemicals in lc50_tox
lc50_cid_list = []
for tox in lc50_tox:
    if tox[0] not in lc50_cid_list : lc50_cid_list.append(tox[0])

print(len(lc50_cid_list))

## 3. Word joinging
txt_sum = ''
for tox in total_tox:
    txt_sum += " }{ "
    txt_sum += tox[1]

## 4. text split & dictionary making
words = txt_sum.lower().split()
word_counts = dict()

for word in words:
    word = word.strip(" ,.;'()/|") 
    word_counts[word] = word_counts.get(word, 0) + 1 
    
sdict = sorted(word_counts.items(), key=operator.itemgetter(1))
sdict.reverse() # 내림차순으로 변경
x_index = np.arange(0,60)
x = [ tpl[0] for tpl in sdict ]
y = [ tpl[1] for tpl in sdict ]

# color & choose
colors = [ 'royalblue' for i in range(0,60) ]
chsidx = [ 0, 6, 23, 37, 38, 43, 44, 45, 46 ]
for id in chsidx : colors[id] = 'tab:red'

print( [sdict[id] for id in chsidx] )
print(sdict[:50])
plt.bar(x_index,y[:60], color=colors)
plt.show()

## 4. text split
#num = 0
#for tox in lc50_tox :
#    words = tox[1].split()
#    for (pos, w) in enumerate(words) :
#        w.strip(" ,.;'()/|")
#        if "/l" in w :
#            if "hardness" in words[pos-2] : num += 1
            #print( words[pos-4], words[pos-3], words[pos-2], words[pos-1], words[pos] )
#            break
#print(num)
