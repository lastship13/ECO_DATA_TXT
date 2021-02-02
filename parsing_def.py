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

def word_tox_list(word, toxlist):
    wordlist = []
    for tox in toxlist:
        if word in tox[1].lower() : wordlist.append(tox)
    return wordlist


