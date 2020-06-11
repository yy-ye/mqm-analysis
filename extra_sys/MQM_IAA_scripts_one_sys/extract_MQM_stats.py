#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import tokeniser


# to test this script on one file
file='/Users/yuyingye/Desktop/EAMT/extra_sys/sys1_annotated_extra_sys_test_set.csv.xml.parsed'
run='/Users/yuyingye/Desktop/EAMT/extra_sys/'


#def count_tokens(string):
    #return len(tokeniser.represent_tomaz(tokeniser.process['standard'](tokeniser.generate_tokenizer('hr'),string,'hr'),0).encode('utf8').strip().split('\n'))  

def extracting(file, run):
    doc=False
    tokenNo=0
    errorhash={'Total error count':0} #the number of tokens that have a certain error markup
    openIssues=[]


    f=open(file, 'r')
    for line in f:
        line=line.strip()
        try:
            ID=line.split(', ')[1]
            tag=line.split(', ')[2]
        except:
            pass
        if line == 'open doc':
            doc=True
            continue
        elif line.startswith('System'):
            continue
        elif line=='close doc':
            doc=False
            continue
        elif line.startswith('mqm:issue,'):
            openIssues.append((ID,tag))
            for t in openIssues:
                if t[1]=='Omission' or t[1]=='Missing' or t[1]=='Punctuation':
                    if t[1] not in errorhash:
                        errorhash[t[1]]=1 #add these categories into the dictionary
                    else:
                        errorhash[t[1]]+=1
            continue
# IF counting all agreement errors as affecting only 2 tokens (due to long-distance agreement)                  
#           elif tjupl[1] in ['Agreement','Case','Number','Gender']:
#               if tjupl[1] not in errorhash:
#                   errorhash[tjupl[1]]=2
#               else:
#                   errorhash[tjupl[1]]+=2
        elif line.endswith('mqm:issue'):
            for t in openIssues:
                if t[0]==(ID):
                    openIssues.remove(t)
            continue
        elif len(openIssues) > 0: 
            length=len(line.replace(" ", ""))
            tokenNo+=length
            for t in openIssues:
            #Punctuation should not be annotated to more than one punctuation at a time
                if t[1] not in errorhash and t[1]!='Punctuation':
                    errorhash[t[1]]=length #add other types into the dictionary
                elif t[1]!='Punctuation':
                    errorhash[t[1]]+=length
        elif len(openIssues) == 0: 
            tokenNo+=len(line.replace(" ", ""))
            continue

    #save output into text file
    filename=os.path.basename(file)
    #change the index to the way you want to save the file
    output=os.path.join(run, filename[:-15]+'.stats')
    o=open(output, 'w')

    errorhash['Total error count']=sum(errorhash.values())

    o.write('### Error breakdown ###\n')
    for entry in errorhash:
        o.write(entry+': '+str(errorhash[entry])+'\n')
    o.write('Total token count: '+str(tokenNo)+'\n')

    o.close()
    return output

if __name__ == "__main__":
    print(extracting(file, run))
