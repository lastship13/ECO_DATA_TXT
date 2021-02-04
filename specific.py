#! /usr/bin/env python

# Modules
import parsing_def as ps
import csv

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


#3-1 lc50 good
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

t = open('LC50_tox.csv', 'w')
csvwriter = csv.writer(t)
for dat in tox_list:
    dat[0] = dat[0].replace('\n','')
    dat[1] = dat[1].replace('\n','')
    csvwriter.writerow(dat)
t.close()


#3-2 ec50 good
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

t = open('EC50_tox.csv', 'w')
csvwriter = csv.writer(t)
for dat in tox_list:
    dat[0] = dat[0].replace('\n','')
    dat[1] = dat[1].replace('\n','')
    csvwriter.writerow(dat)
t.close()

