#! /usr/bin/env python

# Modules
import parsing_def as ps
import pandas as pd
import re
import csv
import operator
import pickle
import os

## 1. read pickle file
pickle_dir = './PICKLES'
fname = 'lc50_good_grouped.pickle'
with open(os.path.join(pickle_dir,fname),"rb") as fr:
    splited_list = pickle.load(fr)

## 2. tag and except words
tag = ['species', 'conditions', 'tration', 'condtions', 'condtiions']
concent_except = ['confidence','interval','purity','limit',
                  'dowacide','technical','material','formulation',
                  'reagent', 'grade','dowicide', 'na-pcp', 'table',
                  'total','racemic', 'mixture', 'office', 'pesticide','program',
                  'active', 'ingredient','formulated','product','on 1-[', '1e', '-1-[',
                  'pure', '%','oxygen','trate', 'emulsifiable','alkalinity','hardness',]

concen_unit = [ 'g/l','l/l','g/kg', 'gl', 'mol','ppm','ppb','pp']
time_unit = ['hr','day','hour', 'week', 'min', 'year', 'yr']

num_con = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
num_time = [ 0, 0, 0, 0, 0, 0, 0 ]
num_false = 0

## 3. species processing
word_counts = dict()
for tox in splited_list :
    concent = [ v for v in tox[1] if v[0] == tag[2] ]
    if len(concent) == 0 :
        print(tox[1])
        break
    concent = concent[0]

    # Not contain digit
    #species = [ v for v in species if not bool(re.search(r'\d', v)) ]
    
    # Not contain except words
    result = []
    for v in concent :
        flag = True
        for w in concent_except :
            if w in v : flag = False
        if len(v) > 25 : flag = False
        if flag : result.append(v)
    
    #print(result[1:])
    flag_c = False
    flag_t = False
    for word in result[1:]:
        for i, unit in enumerate(concen_unit) :
            if unit in word :
                num_con[i] += 1
                flag_c = True
        for i, unit in enumerate(time_unit) :
            if unit in word :
                num_time[i] += 1
                flag_t = True
    if not (flag_t) : 
        print(result[1:])
        num_false += 1

    #    word_counts[word] = word_counts.get(word, 0) + 1

print('con : ',num_con)
print('time : ',num_time)
print(num_false)
print(len(splited_list))
#sdict = sorted(word_counts.items(), key=operator.itemgetter(1))

## **. Save Datas
#outname="lc50_good_species_dictionary.pickle"
#with open(os.path.join(pickle_dir,outname),'wb') as fw:
#    pickle.dump(sdict, fw)

###### print ######
#for i in sdict:
#    print(i)
###################
