#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
main.py FILEPATH
'''

import sys
import os
import csv

from datetime import datetime
from prepare_MQM_output import prepare1, prepare2
from parse_MQM_system import *
from extract_MQM_stats import extracting
from extract_MQM_sent_IAA_stats import calculating_iaa
from extract_error_per_sentence import graph

#the path to directory with the annotation csv files to be processed
filepath='/Users/yuyingye/Desktop/EAMT/'
csvpath=os.path.join(filepath,'csv')


#new output diretory per run
run="{:%Y%m%d%H%M}".format(datetime.now())
os.makedirs(filepath+run,exist_ok=True)
print("Created new folder: {}".format(run))
xmlpath=os.path.join(filepath, run)

    # 1 Prepare the xml files
for file in os.listdir(csvpath):
    if file.endswith('.csv'):
        sys1xml=prepare1(xmlpath, os.path.join(csvpath, file))
        print('Prepared', sys1xml)
        sys2xml=prepare2(xmlpath, os.path.join(csvpath, file))
        print('Prepared', sys2xml)

    # 2 Parse the xml files

for file in os.listdir(xmlpath):
    if file.endswith('.xml'):
        parsedxml=parsing(os.path.join(xmlpath, file), xmlpath)
        print('Parsed', parsedxml)

    # 3 Extract amounts of tokens with errors per system per annotator
for file in os.listdir(xmlpath):
    if file.endswith('.parsed'):
        stats=extracting(os.path.join(xmlpath, file), xmlpath)
        print('Extracted', stats)

    # 4 Calculate IAA (Inter Annotataor Agreement)

for file in os.listdir(xmlpath):
    if file.endswith('.parsed'):
        a1name=os.path.basename(file)
        if 'annotator1' in a1name: #one of the annotator
            parsedfile1 = os.path.join(xmlpath, file)
            a2name=a1name.replace('annotator1','annotator2') #replace the name of Annotator 1 with Annotator 2
            parsedfile2 = os.path.join(xmlpath, a2name)
            iaa=calculating_iaa(parsedfile1, parsedfile2, xmlpath)
            print('Calculated IAA', iaa)

    # 5 create a histogram of error distribution per sentences
sys1=[]
sys2=[]
for file in os.listdir(xmlpath):
    if file.endswith('.xml') and 'test_set' in file:
        if 'sys1' in file:
            sys1.append(os.path.join(xmlpath,file))
            outfile1=os.path.join(xmlpath, file[:13]+'.merge')
        else:
            sys2.append(os.path.join(xmlpath,file))
            outfile2=os.path.join(xmlpath, file[:13]+'.merge')

with open (outfile1, 'w') as outfile: 
    for name in sys1:
        with open(name) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
    outfile.close()

with open (outfile2, 'w') as outfile: 
    for name in sys2:
        with open(name) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
    outfile.close()
graph = graph(outfile1, outfile2, xmlpath)

   # 6 Extract amounts of tokens with errors per system from both annotators concatenated for the test set 
parsedsys1=[]
parsedsys2=[]
for file in os.listdir(xmlpath):
    if file.endswith('.parsed') and 'test_set' in file:
        if 'sys1' in file:
            parsedsys1.append(os.path.join(xmlpath,file))
            file1=os.path.join(xmlpath, file[:13]+'.parsedmerge')
        else:
            parsedsys2.append(os.path.join(xmlpath,file))
            file2=os.path.join(xmlpath, file[:13]+'.parsedmerge')

with open (file1, 'w') as outfile: 
    for name in parsedsys1:
        with open(name) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
    outfile.close()

with open (file2, 'w') as outfile: 
    for name in parsedsys2:
        with open(name) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
    outfile.close()

for file in os.listdir(xmlpath):
    if file.endswith('.parsedmerge'):
        stats=extracting(os.path.join(xmlpath, file), xmlpath)
        print('Extracted', stats)
