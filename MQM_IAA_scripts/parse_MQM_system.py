#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.parsers.expat
import os
import sys

'''
# to test this script on one file
file='path to file'
run='path to run directory'
'''
 
def parsing(file, run):  
    def start_element(name, attrs):
        if name=='doc':
            print('open '+name)
        else:   
            if len(attrs) > 1:
                print(name+', '+attrs['xml:id']+', '+attrs[u'type'])
            elif len(attrs) == 1:
                print(name+', '+attrs['id'])

    def end_element(name):
        if name == 'doc':
            print('close '+name)
        elif name == 'mqm:issue':
            print(name)
    
    def char_data(data):
        if data !='\n':
            print(data)  


    filename=os.path.basename(file)
    output=os.path.join(run, filename+'.parsed')
    orig_stdout = sys.stdout
    f=open(output, 'w')
    sys.stdout = f

    parser = xml.parsers.expat.ParserCreate()

    parser.StartElementHandler = start_element
    parser.EndElementHandler = end_element
    parser.CharacterDataHandler= char_data

    lines=open(file, 'r')
    for line in lines:
        parser.Parse(line)

    sys.stdout = orig_stdout
    f.close()
    return output 
if __name__ == "__main__":
    print(parsing(file, run))