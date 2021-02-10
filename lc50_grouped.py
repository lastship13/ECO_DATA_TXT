#! /usr/bin/env python

# Modules
import parsing_def as ps
import pandas as pd
import re
import csv
import operator
import pickle

## 1. read csv file
data = pd.read_csv("./LC50_tox.csv", header=None)
#print(data.head)

## 2. format change for using def
data_list = data.values.tolist()
#print(data_list)

## 3. tag and except words
tag = ['species', 'conditions', 'tration', 'condtions', 'condtiions']
species_except = ['embryo', 'egg', 'larvae', 'embryo', 'young', 'adult', 'hatch',
                  'life', 'stage', 'organism', 'new', 'mid', 'late', 'first', 'instar',
                  'early', 'male', 'female', 'second', 'year', 'age','interface',
                  'equilibrium', 'death', 'mature', 'type', 'length', 'growth', 'log',
                  'larva', 'asexual', 'weight', 'oxygen', 'static', 'fresh',
                  'juvenile', 'mixed', 'tadpole', 'semi', 'site', 'swim', 'gastrulae',
                  'blastu', 'gastulae','lab','obtained','clone','reproduc', 'neonat',
                  'loss', 'wild', 'sub','strain','recent','unfed' ]

## 4-1. text grouping
splited_list = []
for tox in data_list:
    tox_grouped = []
    split_list = re.split(';|:|\(|\)| \/| for | ,|, |lc50| and | or | of |concen| at |chromium| in ',tox[1])
    split_list = [ v.strip(' /') for v in split_list if v ]

    tag_id = [ i for i, word in enumerate(split_list)
               if ( (word.strip() in tag) or (tag[1] in word.strip()) )]

    previd = 0 
    for id in tag_id :
        add = split_list[previd:id]
        if add : tox_grouped.append(add) # not append empty list
        previd = id
    tox_grouped.append(split_list[id:])

    splited_list.append([tox[0],tox_grouped])

## **. Save Datas
with open("lc50_good_grouped.pickle",'wb') as fw:
    pickle.dump(splited_list, fw)

###### print ######
#for i in splited_list:
#    print(i[1:])
###################
