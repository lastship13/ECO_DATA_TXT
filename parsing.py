#! /usr/bin/env python

# Modules
import os
import html
import re
import xml.etree.ElementTree as ET
import operator

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

## 2. count
count_dic = {}
for idx in cid_list:
    name, tox = load_poison_info(int(idx))
    lines = ''.join(tox)
    count_dic[idx] = lines.count(':')

  #2-1 
tox_txt_list = []
for idx in count_dic.keys():
    val = count_dic[idx]
    if val == 0 :
        name, tox = load_poison_info(int(idx))
        for tid in range(len(tox)):
            tline = tox[tid]
            tox_txt_list.append([idx, tline])

#print(tox_txt_list)
NUM_FM = 0
NUM_DP = 0
txt_sum =''
for tline in tox_txt_list:
    #print(tline[1])
    NUM_FM += tline[1].lower().count("fathead")
    NUM_DP += tline[1].lower().count("daphnia")
    txt_sum += " }{ "
    txt_sum += tline[1]
print(NUM_FM)
print(NUM_DP)
print(len(tox_txt_list))
  #2-2
#print(txt_sum)

words = txt_sum.lower().split()
word_counts = dict()

for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1
    
sdict = sorted(word_counts.items(), key=operator.itemgetter(1))

print(sdict)



#    if test == 20 : break

## 3. histo
#import matplotlib.pyplot as plt
#import numpy as np

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


