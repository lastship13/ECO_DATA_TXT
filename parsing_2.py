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

## 2. total tox infos
total_tox = []
lc50_tox = []
ec50_tox = []
ld50_tox = []

for cid in cid_list:
    name, tox = load_poison_info(int(cid))
    total_tox += [ [cid,info.lower()] for info in tox ]

for tox in total_tox :
    if "lc50" in tox[1].lower() : lc50_tox.append(tox)
    if "ec50" in tox[1].lower() : ec50_tox.append(tox)
    if "ld50" in tox[1].lower() : ld50_tox.append(tox)

## 4. text split
num = 0
for tox in lc50_tox :
    words = tox[1].split()
    for (pos, w) in enumerate(words) :
        w.strip(" ,.;'()/|")
        if "/l" in w :
            if "concentration" in words[pos-2] : num += 1
            print( words[pos-2], words[pos-1], words[pos] )
            break
print(num)
