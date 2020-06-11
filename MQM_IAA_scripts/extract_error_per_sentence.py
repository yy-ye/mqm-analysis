#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.parsers.expat
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
"""
# to run this script on one file
file1=''
run=''
file2=''
"""
def graph(file1, file2, run):
    
    def error_per_sent(file):  
        errorlist=[]
        count=0
        error='type='
        with open(file, 'r') as text:
            for line in text:
                if line.startswith('<doc>'):
                    count=line.count(error)
                    errorlist.append(count)
                count=0

        # remove the first item, because the first item is the system name, not a sentence
            errorlist=errorlist[1:]
            return errorlist
            
    list1=error_per_sent(file1)
    list2=error_per_sent(file2)

        #creat a histogram 
    labels, counts = np.unique(list1,return_counts=True)
    print(labels)
    print(counts)
    label2, count2 = np.unique(list2,return_counts=True)
    print(label2)
    print(count2)

    #change this according to labels, counts, labels2 and counts2
    df = pd.DataFrame({'Transformer': [75, 63, 31, 15, 11, 2, 2, 1, 1, 0,0],
                       'RNN':[42, 59, 52, 25, 9, 6, 4, 1, 2, 0, 1]}, index=[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    #print(df)
    df.plot.bar() 
    plt.xticks(rotation=0) 
    plt.xlabel('Errors per sentence')
    plt.ylabel('Numbers of Sentence')
    plt.savefig(os.path.join(run,'error_per_sent.png'), dpi=300)
    plt.show()
    print('error_per_sent.png is created')

if __name__ == "__main__":
    print(graph(file1, file2, run))

