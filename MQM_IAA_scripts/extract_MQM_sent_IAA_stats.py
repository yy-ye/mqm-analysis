#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to use this function $pip install future
import os
from past.utils import old_div
import sys
"""
# to run this script on one file
parsedfile1='path to the parsed file'
parsedfile2='path to the parsed file'
run='path to the run directory'
"""

def calculating_iaa(parsedfile1, parsedfile2, run):
    
    # output filr
    filename=os.path.basename(parsedfile1)
    output=os.path.join(run, filename[:-26]+'.iaa')
    orig_stdout = sys.stdout
    o=open(output, 'w')
    sys.stdout = o

    def count_sentence_errors(doc):
        sent=False
        sent_counter=0
        sent_annos={}
    
        for line in doc:
            line=line.strip()
            try:
                ID=line.split(', ')[1]
                tag=line.split(', ')[2]
            except:
                pass
            error_c=0
            if line == 'open doc':
                sent=True
                sent_counter+=1
                sent_annos[sent_counter]=[]
                continue
            elif line== 'close doc':
                sent=False
                continue
            elif line.startswith('mqm:issue,'):
                if tag not in sent_annos[sent_counter]:
                    sent_annos[sent_counter].append(tag)
        return sent_annos   #sent_annos=={1:['Mistranslation'], 2:['Unintelligible','Agreement'], ...}

    def calculate_kappa(xyyes,xyesyno,xnoyyes,xyno):
        a=xyyes
        b=xyesyno
        c=xnoyyes
        d=xyno   

        po=old_div((float(a)+d),(a+b+c+d))
        marginala=old_div(((float(a)+b)*(a+c)),(a+b+c+d))
        marginalb=old_div(((c+d)*(b+d)),(float(a)+b+c+d))
        pe=old_div((marginala+marginalb),(float(a)+b+c+d))

        kappa=old_div((po-pe),(1.0-pe))
    
        return kappa

    annotator1=open(parsedfile1, "r") 
    annotator2=open(parsedfile2, "r") 

    a1_errors=count_sentence_errors(annotator1)
    a2_errors=count_sentence_errors(annotator2)

    fdyes={'Accuracy':0,'Mistranslation':0, 'Overly-literal':0, 'Entity':0, 'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Typograhy':0, 'Unpaired-marks':0, 'Punctuation':0, 'Unintelligible':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0, 'Preposition':0, 'Adverb': 0, 'Particle':0, 'Incorrect':0,'Missing':0, 'Classifier':0, 'Unintelligible':0}
    fnodyes={'Accuracy':0,'Mistranslation':0, 'Overly-literal':0, 'Entity':0, 'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Typograhy':0, 'Unpaired-marks':0, 'Punctuation':0, 'Unintelligible':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0, 'Preposition':0, 'Adverb': 0, 'Particle':0, 'Incorrect':0,'Missing':0, 'Classifier':0, 'Unintelligible':0}
    fyesdno={'Accuracy':0,'Mistranslation':0, 'Overly-literal':0, 'Entity':0, 'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Typograhy':0, 'Unpaired-marks':0, 'Punctuation':0, 'Unintelligible':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0, 'Preposition':0, 'Adverb': 0, 'Particle':0, 'Incorrect':0,'Missing':0, 'Classifier':0, 'Unintelligible':0}
    fdno={'Accuracy':0,'Mistranslation':0, 'Overly-literal':0, 'Entity':0, 'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Typograhy':0, 'Unpaired-marks':0, 'Punctuation':0, 'Unintelligible':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0, 'Preposition':0, 'Adverb': 0, 'Particle':0, 'Incorrect':0,'Missing':0, 'Classifier':0, 'Unintelligible':0}


#f_errors={1:[],2:[], 3:['Mistranslation'], 4:['Mistranslation','Untranslated']}
#d_errors={1:[],2:['Mistranslation'], 3:[], 4:['Mistranslation','Missing']}


#agreement overall and for every existing error category
    for sentence in a1_errors:
        if len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) == 0:
            for error in fdno:
                fdno[error]+=1
        elif len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) > 0:
            for error in fnodyes:
                if error in a2_errors[sentence]:
                    fnodyes[error]+=1
                else:
                    fdno[error]+=1
        elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) == 0:
            for error in fyesdno:
                if error in a1_errors[sentence]:
                    fyesdno[error]+=1
                else:
                    fdno[error]+=1
        elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) > 0:
            for error in fdyes:
                if error in a2_errors[sentence] and error in a1_errors[sentence]:
                    fdyes[error]+=1             
                elif error in a2_errors[sentence] and error not in a1_errors[sentence]:
                    fnodyes[error]+=1
                elif error not in a2_errors[sentence] and error in a1_errors[sentence]:
                    fyesdno[error]+=1
                else:
                    fdno[error]+=1  

    print('Total kappa: '+str(calculate_kappa(sum(fdyes.values()),sum(fyesdno.values()),sum(fnodyes.values()),sum(fdno.values()))))

    lista=[fdyes,fnodyes,fdno,fyesdno]

    for error_counts in lista:
        for error_type in error_counts:
            if error_type in ['Mistranslation','Addition','Omission','Untranslated']:
                error_counts['Accuracy']+=error_counts[error_type]

            elif error_type in ['Overly-literal','Entity']:
                error_counts['Mistranslation']+=error_counts[error_type]

            elif error_type in ['Typograhy','Grammar','Unintelligible']:
                error_counts['Fluency']+=error_counts[error_type]

            elif error_type in ['Extraneous','Missing','Incorrect']:
                error_counts['Function words']+=error_counts[error_type]
            
            elif error_type in ['Preposition','Adverb','Particle']:
                error_counts['Extraneous']+=error_counts[error_type]

            elif error_type in ['Punctuation','Unpaired-marks']:
                error_counts['Typograhy']+=error_counts[error_type]
            
            elif error_type in ['Classifier','Word order','Function words']:
                error_counts['Grammar']+=error_counts[error_type]

    for error in fdyes:
        if fdyes[error]==fyesdno[error]==fnodyes[error]==0:
            print('Annotators did not use error type '+error)
        else:
            try:
                print('Kappa for '+error+': '+str(calculate_kappa(fdyes[error],fyesdno[error],fnodyes[error],fdno[error])))
            except:
                print('Oops, problem with '+error)

    fdyes=0
    fnodyes=0
    fyesdno=0
    fdno=0

#agreement for 'any' error per sentence

    for sentence in a1_errors:
        print('annotator1:', a1_errors[sentence])
        print('annotator2', a2_errors[sentence])
        if len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) == 0:
            fdno+=1
            print('fdno', fdno)
        elif len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) > 0:
            fnodyes+=1
            print('fnodyes', fnodyes)
        elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) == 0:
            fyesdno+=1
            print('fyesdno', fyesdno)
        elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) > 0:
            fdyes+=1
            print('fdyes', fdyes)

    print(fdyes, fnodyes, fyesdno, fdno)

    print('Overall kappa: '+str(calculate_kappa(fdyes,fyesdno,fnodyes,fdno)))
    
    sys.stdout = orig_stdout
    o.close()
    return output

if __name__ == "__main__":
    print(calculating_iaa(parsedfile1, parsedfile2, run))
