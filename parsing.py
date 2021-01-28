#! /usr/bin/env python

# Modules
import os
import html
import re
import xml.etree.ElementTree as ET
import operator
import matplotlib.pyplot as plt
import numpy as np

# Functions
def load_poison_info(cid):
    xml_file = os.path.join('XML','output.{}.xml'.format(cid))

    xml_data = ET.parse(xml_file).getroot()
    str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

    name_start_str = '<ns0:RecordTitle>'
    name_end_str = name_start_str.replace('ns0', '/ns0')
    regex = re.compile(r'{}.*{}'.format(name_start_str, name_end_str))
    name = regex.findall(str_data)[0]
    name = name.replace(name_start_str, '').replace(name_end_str, '')

    start_str = '<ns0:String>'
    end_str = start_str.replace('ns0', '/ns0')
    regex = re.compile(r'{}.*{}'.format(start_str, end_str))

    toxic_list = regex.findall(str_data)
    toxic_list = [html.unescape(i.replace(start_str, '').replace(end_str, ''))
                   for i in toxic_list]

    return name, toxic_list


## 1. output cid list
f = open('XML/log_output','r')
cid_list = f.readlines()
f.close()

## 2. count words
count_dic = {}
for idx in cid_list:
    name, tox = load_poison_info(int(idx))
    lines = ''.join(tox)
    count_dic[idx] = lines.count(':')

## 2-1. tot_txt_list 
tox_txt_list = []
for idx in count_dic.keys():
    val = count_dic[idx]
    if val == 0 :
        name, tox = load_poison_info(int(idx))
        for tid in range(len(tox)):
            tline = tox[tid]
            tox_txt_list.append([idx, tline])

## 3. text sum
txt_sum =''

NUM_FM = 0
NUM_DP = 0
NUM_LC = 0
NUM_EC = 0

for tline in tox_txt_list:
    NUM_FM += tline[1].lower().count("fathead")
    NUM_DP += tline[1].lower().count("daphnia")
    NUM_LC += tline[1].lower().count("lc50")
    NUM_EC += tline[1].lower().count("ec50")
    txt_sum += " }{ "
    txt_sum += tline[1]

print("# of fathead :",NUM_FM)
print("# of daphnia :",NUM_DP)
print("# of LC50 :",NUM_LC)
print("# of EC50 :",NUM_EC)
print("# of total tox infos :",len(tox_txt_list))


## 4. text split & dictionary making
words = txt_sum.lower().split()
word_counts = dict()

for word in words:
    word = word.strip(" ,.;'()/|") 
    word_counts[word] = word_counts.get(word, 0) + 1
    
sdict = sorted(word_counts.items(), key=operator.itemgetter(1))
#print(sdict)

## 5. histo

## 5-1. count histogram images
#g = open('histogram.txt','w')
#bins = np.arange(0,100,1)
#hist, bins = np.histogram(list(count_dic.values()),bins)

#print(bins)
#print(hist)

#for index, value in enumerate(hist):
#    g.write(str(bins[index])+str(hist[index])+"\n")

#g.close()
#plt.hist(list(count_dic.values()),bins)
#plt.show()


## 5-2. word split dictionary images
sdict.reverse() # 내림차순으로 변경
x_index = np.arange(0,60)
x = [ tpl[0] for tpl in sdict ]
y = [ tpl[1] for tpl in sdict ]

# color & choose
colors = [ 'royalblue' for i in range(0,60) ]
chsidx = [ 0, 2, 18, 36, 43, 44, 49, 53, 54 ]
for id in chsidx : colors[id] = 'tab:red'

#print(colors)
print( sdict[:60] )
print( [sdict[id] for id in chsidx] )

plt.bar(x_index,y[:60], color=colors)
plt.show()
