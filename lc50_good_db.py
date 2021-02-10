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
species_except = ['embryo', 'egg', 'larvae', 'embryo', 'young', 'adult', 'hatch',
                  'life', 'stage', 'organism', 'new', 'mid', 'late', 'first', 'instar',
                  'early', 'male', 'female', 'second', 'year', 'age','interface',
                  'equilibrium', 'death', 'mature', 'type', 'length', 'growth', 'log',
                  'larva', 'asexual', 'weight', 'oxygen', 'static', 'fresh',
                  'juvenile', 'mixed', 'tadpole', 'semi', 'site', 'swim', 'gastrulae',
                  'blastu', 'gastulae','lab','obtained','clone','reproduc', 'neonat',
                  'loss', 'wild', 'sub','strain','recent','unfed' ]
concent_except = ['confidence','interval','purity','limit',
                  'dowacide','technical','material','formulation',
                  'reagent', 'grade','dowicide', 'na-pcp', 'table',
                  'total','racemic', 'mixture', 'office', 'pesticide','program',
                  'active', 'ingredient','formulated','product','on 1-[', '1e', '-1-[',
                  'pure', '%','oxygen','trate', 'emulsifiable','alkalinity','hardness',
                  'flow','soft','meth', 'ion', 'hard', 'therefore', 'exposure', 'caco3',
                  'salinity', 'capacitor','temperature', 'nominal', 'fluro', 'pyrethrins']


## search species
species_list = []

concen_unit = [ 'g/l','l/l','g/kg', 'gl', 'mol','ppm','ppb','pp']
time_unit = [' hr', 'hr ','day','hour', 'week', ' min', 'min ', 'year', ' yr', 'yr ']


for tox in splited_list :
    species = [ v for v in tox[1] if v[0] == tag[0] ]
    concent = [ v for v in tox[1] if v[0] == tag[2] ]

    ## SPECIES
    species = species[0]
    # Not contain digit
    species = [ v for v in species if not bool(re.search(r'\d', v)) ]

    # Not contain except words
    result_spec = []
    for v in species :
        flag = True
        for w in species_except :
            if w in v : flag = False
        if len(v) < 3 or len(v) > 50: flag = False
        if flag : result_spec.append(v)

    ## CONCENTRATION
    concent = concent[0]
    
    # Not contain except words
    result_conc = []
    for v in concent :
        flag = True
        for w in concent_except :
            if w in v : flag = False
        if len(v) > 25 : flag = False
        if flag : result_conc.append(v)

    structure = [ 0 for i in range(len(result_conc)) ]    
    for i, word in enumerate(result_conc) :
       for unit in concen_unit :
           if unit in word : structure[i] = 1
       for unit in time_unit :
           if unit in word : 
               if structure[i] != 1 :
                   structure[i] = 2
               else : structure[i] = 3

    #print(result_conc)
    #print(structure)
    #if structure.count(3) == 0 :
    #    if structure.count(1) == 1 and structure.count(2) == 1 :
    #        print(structure
    #else : 
        #print(structure)

   # for word in result[1:]:
   #     for unit in concen_unit :
   #         if unit in word :
