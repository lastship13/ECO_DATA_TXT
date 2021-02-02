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

print("# of chemicals : ", len(cid_list))
print("total : ", len(total_tox))
print("lc50 : ",len(lc50_tox))
print("ec50 : ",len(ec50_tox))


tox_list = ps.word_tox_list("species:", lc50_tox)
tox_list = ps.word_tox_list("concentration:", tox_list)

print("lc50_good:",len(tox_list))

Ncid = ps.count_cid(tox_list)
print("lc50_good_cid:", Ncid)

cids = ps.mk_cid_list(tox_list)
c = open('LC50_cid.txt','w')
for cid in cids:
    c.write(cid)
c.close()

tox_list = ps.word_tox_list("species:", ec50_tox)
tox_list = ps.word_tox_list("concentration:", tox_list)

print("ec50_good:",len(tox_list))

Ncid = ps.count_cid(tox_list)
print("ec50_good_cid:", Ncid)

cids = ps.mk_cid_list(tox_list)
c = open('EC50_cid.txt','w')
for cid in cids:
    c.write(cid)
c.close()


