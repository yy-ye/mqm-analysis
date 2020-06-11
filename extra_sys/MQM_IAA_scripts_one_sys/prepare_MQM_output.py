#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import os

# to test this script on one file
file='/Users/yuyingye/Desktop/EAMT/extra_sys/annotated_extra_sys_test_set.csv'
run='/Users/yuyingye/Desktop/EAMT/extra_sys/'


def prepare1(run, file):

    reference=[]
    sys1=[]
    #sys2=[]

    with open(file, "r") as input:
        annotation = csv.reader(input, delimiter=",", quotechar='"')
        for line in annotation:
            sentID=line[0]
            sourcesent=line[1]
            refsent=line[2]
            sys1sent=line[3]#m3sys=line[3]
            #sys2sent=line[4]#nmtsys=line[4]
        
        
            reference.append(refsent)
            sys1.append(sys1sent)
            #sys2.append(sys2sent)
    
    filename=os.path.basename(file)
    output1=os.path.join(run, 'sys1_'+filename+'.xml')
    #output2=os.path.join(run, 'sys2_'+filename+'.xml')
    
    sys1data=open(output1, 'w')
    sys1data.write('<docs>\n')

    for sentence in sys1:
        doc = '<doc>'+ sentence + '</doc>'
        sys1data.write(doc+'\n')

    sys1data.write('</docs>\n')
    sys1data.close()
    return output1
"""
def prepare2(run, file):
    sys2=[]

    with open(file, "r") as input:
        annotation = csv.reader(input, delimiter=",", quotechar='"')
        for line in annotation:
            sys2sent=line[4]#nmtsys=line[4]
        
            sys2.append(sys2sent)
    
    filename=os.path.basename(file)
    output2=os.path.join(run, 'sys2_'+filename+'.xml')

    sys2data=open(output2, 'w')
    sys2data.write('<docs>\n')

    for sentence in sys2:
        doc = '<doc>'+ sentence + '</doc>'
        sys2data.write(doc+'\n')

    sys2data.write('</docs>\n')
    sys2data.close()
    return output2 
"""
if __name__ == "__main__":
    print(prepare1(run, file))
    #print(prepare2(run, file))
