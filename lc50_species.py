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
tag = ['species', 'conditions', 'concentration', 'condtions', 'condtiions']
species_except = ['embryo', 'egg', 'larvae', 'embryo', 'young', 'adult', 'hatch',
                  'life', 'stage', 'organism', 'new', 'mid', 'late', 'first', 'instar',
                  'early', 'male', 'female', 'second', 'year', 'age','interface',
                  'equilibrium', 'death', 'mature', 'type', 'length', 'growth', 'log',
                  'larva', 'asexual', 'weight', 'oxygen', 'static', 'fresh',
                  'juvenile', 'mixed', 'tadpole', 'semi', 'site', 'swim', 'gastrulae',
                  'blastu', 'gastulae','lab','obtained','clone','reproduc', 'neonat',
                  'loss', 'wild', 'sub','strain','recent','unfed' ]

## 3. species processing
word_counts = dict()
for tox in splited_list :
    species = [ v for v in tox[1] if v[0] == tag[0] ]
    species = species[0]

    # Not contain digit
    species = [ v for v in species if not bool(re.search(r'\d', v)) ]
    
    # Not contain except words
    result = []
    for v in species :
        flag = True
        for w in species_except :
            if w in v : flag = False
        if len(v) < 3 or len(v) > 50: flag = False
        if flag : result.append(v)
    
    # print(result[1:])
    for word in result[1:]:
        word_counts[word] = word_counts.get(word, 0) + 1


sdict = sorted(word_counts.items(), key=operator.itemgetter(1))

## **. Save Datas
outname="lc50_good_species_dictionary.pickle"
with open(os.path.join(pickle_dir,outname),'wb') as fw:
    pickle.dump(sdict, fw)

###### print ######
for i in sdict:
    print(i)
###################
