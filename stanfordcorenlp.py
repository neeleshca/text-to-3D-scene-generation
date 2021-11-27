import subprocess
def punc(sent):
    l=['.',',']
    sent=list(sent)
    a=len(sent)
    sent.append(' ')
  
    i=0
    while i<=(a):
        if(i>len(sent)):
            break
        if sent[i] in l:
            sent.insert(i,' ')
            a+=1
            i+=1
        i+=1
    sent.pop()  
    s=''
    for i in range(len(sent)):
        s+=str(sent[i])
    s=str(s)
    print('what')
    return s

from nltk import sent_tokenize


from nltk.tag.stanford import StanfordPOSTagger as pos
import sys
import nltk
from nltk.corpus import wordnet as wn
from pycorenlp import StanfordCoreNLP
#home="/home/ninaad/CDSAML"
_path_to_model='postagger/models/english-bidirectional-distsim.tagger'                               
_path_to_jar='postagger/stanford-postagger.jar' 
tagger=pos(_path_to_model,_path_to_jar)
nlp = StanfordCoreNLP('http://localhost:9000')
#start a session by typing java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 150000
fp=open('coref.txt','w')
fp1=open('relations.txt','w')
text =input('enter the sentence\n')
text=punc(text)
#print('hello what happened')
sample=text.split()
andnoun=[]
acceptedpreposition=['on(','in_front_of(','next_to(','behind(','beside(']
#print(sample)
#print(postag)
def andcheck(sample):
    postag=tagger.tag(sample)
    tag2=[]
    tag3=[]
   
    for i in range(len(postag)):
        if postag[i][0]=='round':
            postag[i]=list(postag[i])
            postag[i][1]='JJ'
            postag[i]=tuple(postag[i])
        tag2.append(postag[i][1]) 
        if postag[i][0]=='next':
            postag[i]=list(postag[i])
            postag[i][1]='IN'
            postag[i]=tuple(postag[i])
        tag2.append(postag[i][1]) 
        if postag[i][0]=='front':
            postag[i]=list(postag[i])
            postag[i][1]='IN'
            postag[i]=tuple(postag[i])
        tag2.append(postag[i][1]) 
    andnoun=[]
    andnounflag=0
    andflag=0
    andnoun1=[]
    m=-1
    if '.' in sample[:len(sample)-2]:
        sample=sample[sample.index('.')+1:]
        return andcheck(sample)
    if 'and' in sample:
            m=sample.index('and')
            andnoun1=sample[m+1:]
            tag3=tag2[m+1:]
            #print('andnoun1 inside and is',andnoun1)
            if 'and' in andnoun1:
                    andnoun2=andnoun1
                    return andcheck(andnoun2)
            if 'is' in andnoun1 or 'are' in andnoun1 :
             #   print('entered 70',andnoun1)
              #  print('is' in andnoun1)
                andflag=1
            if 'IN' not in tag3:
                andflag=1
    #print('length of sample is',len(sample))
    #print(postag)
   
    for i in range(len(sample)):
        if postag[i][1]=='NN' or postag[i][1]=='NNS':
            if i<m and andflag==0:
                andnoun.append(postag[i][0])
            elif i>m and andnounflag==0 and andflag==0:
                andnoun.append(postag[i][0])
                andnounflag=1
    return andnoun
if 'and' in sample:
    andnoun=andcheck(sample)
#print(andnoun)
#print(postag)
#print(text)
wall=['frontwall','rightwall','leftwall','wall','ceiling']
wall1=['front_wall','right_wall','left_wall','wall','ceiling']
position=['leftof','rightof']
wallflag=-1
positionflag=0
for i in range(len(sample)-1):
    if sample[i]+sample[i+1] in wall:
        sample[i]=sample[i]+'_'+sample[i+1]
        wallflag=i+1
    if sample[i]+sample[i+1] in position:
        positionflag=1
        #sample.remove(sample[i+1])
        
if wallflag!=-1:
    while 'wall' in sample:
        sample.remove('wall')
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]
      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

m=len(sample)
z=sample.count('next')

text=' '.join(sample)
print('text is',text)
output = nlp.annotate(text, properties={
   'annotators': 'tokenize,ssplit,depparse,ner,parse,pos,dcoref',
'outputFormat': 'conll'})
output2=nlp.annotate(text, properties={
   'annotators': 'tokenize,ssplit,depparse,ner,parse,pos,dcoref',
'outputFormat': 'json'})
'''for i in output2['sentences']:
    print(i)
    for j in i['basic-dependencies']:
        for k in j:
            if j[k]=='nmod':
                print('asd',j)
'''       
text1 = nlp.annotate(text, properties={
   'annotators': 'tokenize,ssplit,depparse,ner,parse,pos,dcoref',
'outputFormat': 'text'})
fp.write(output)
print(text1)
text2=text1.split()
#print(text2)
textcopy=text2
text3=[]
conj=[]

#print(text2)
mweflag=0
mwestring=[]
certainflag=0
onflag=0
flagon=0
if ('and' in sample and 'on' in sample):
    onflag=1
if ' in front of' in text:
    print('188')
    certainflag=1
    
if 'front' in sample and 'and' in sample:
    certainflag=2
for i in range(len(text2)-1):
    mwestring1=''
    if ('nmod' in text2[i]):
        
        textof=text2[i].split(":")
        textof1=textof[1].split('(')
        print(textof1)
        for z in range(len(textof1)):
            if textof1[z]=='of':
                textof1[z]='in_front_of'
        textof1="(".join(textof1)
        textof[1]=textof1
        textof=":".join(textof)
        text2[i]=textof
        print('text2[i] is',text2[i])
        for prep in acceptedpreposition:
            
            if prep in text2[i]:
                print('entered 198')
                text3.append(text2[i]+text2[i+1])
               
        '''if 'on' in text2 and flagon==0:
            print('entered flagon')
            print(text2[i]+text2[i+1])
            text3.append(text2[i]+text2[i+1])
            flagon=1'''
        if certainflag==0 and positionflag==0:
            print('entered')
            text3.append(text2[i]+text2[i+1])
    if 'conj' in text2[i]:
        conj.append(text2[i])
    if 'nmod' not in text1 or certainflag>0 or positionflag>0:
        if onflag==1:
            print('entered through onflag')
            mwestring.append('on')
            mweflag=1
            onflag=2
        if certainflag==1:
            print('enteredad')
            mwestring.append('in_front_of')
            mweflag=1
            certainflag=3
        if positionflag==1:
            if 'left' in sample:
                print('enteredad')
                mwestring.append('left_of')
                mweflag=1
                positionflag=2
            else:
                mwestring.append('right_of')
                mweflag=1
                positionflag=2                
        elif 'mwe' in text2[i] and certainflag==2:
            if mweflag==0:
                mwe=text2[i].split('(')
               
                mwe1=text2[i+1].split('-')
                mwe.remove('mwe')
                for i in mwe:
                    i=i.split('-')
                    mwestring1+=i[0]+'_'+mwe1[0]
                mwestring.append(mwestring1)
                mweflag=1
            elif mweflag==1:
 #               print('127')
  #              print(mwestring)
                mwe=text2[i].split('(')
   #             print(mwe)
                mwe1=text2[i+1].split('-')
    #            print(mwe1)
                mwe.remove('mwe')
                for k in mwe:
                    k=k.split('-')
                   
     #               print(k)
                    for l in k:
      #                  print(l)
                        for m in mwe1:
       #                     print(m)
                            if l not in mwestring:
        #                        print('l before indexing',l)
                                if ',' in l:
         #                           print('yes')
                                    l=l[:l.index(',')]
          #                          print('l is',l)
                                    if l.isdigit()==0:
                                        mwestring1+='_'+l
                                        mwestring.append(mwestring1)
                                elif l.isdigit()==0:
                                        mwestring1+='_'+l
                                        mwestring.append(mwestring1)
                            if m not in mwestring:
           #                     print('m before indexing',m)
                                if ')' in m:
                                    m=m[:m.index(')')]
            #                        print('m is',m)
                                    if m.isdigit()==0:
                                        mwestring1+='_'+m
                                        mwestring.append(mwestring1)
                                elif m.isdigit()==0:
                                    mwestring1+='_'+m
                                    mwestring.append(mwestring1)

#print(mweflag) 
print(mwestring)
text3=list(set(text3))
#print(text3)
#fp1.write(text3+'\n')
print(text3)
for i in range(len(text2)):
    if text2[i]=='Coreference':
        text2=text2[i:]
        text4=text2[-1]
        break
#print(output)
coreferencerelation=[]
quoteflag=0
string=''
text2=" ".join(text2)
copy=text2
#print(copy)
noun=[]



for i in range(len(copy)):
    if copy[i]=='"':
        quoteflag+=1
        if quoteflag==1:
            j=i
        if quoteflag==4:
            coreferencerelation.append(copy[j:i])
            quoteflag=0
for i in coreferencerelation:
    i=i.split()
    sent=tagger.tag(i)
    for j in sent:
        if 'NN' in j:
            noun.append(j[0])
#print(coreferencerelation)  
#print(noun)
count=0
splittext=[]
splitcount=0
for i in range(len(text3)):
    z=len(text3[i])
   
    splittext.append(text3[i].split(','))
    print(splittext[i])
    for it in list(splittext[i]):
        indx=splittext[i].index(it)
        it=it.split('-')
        print(it)
        for bingo in it:
            if bingo=='it':
                if len(noun)>0:
                    it[it.index(bingo)]=noun[count]
                #print(it)
                count+=1
        it="-".join(it)
        #print(it)
        splittext[i][indx]=it
        #print(splittext)
        #splittext=",".join(splittext)
    
    splittext[i]=",".join(splittext[i])
#print(splittext)
text7=text2.split()
if text7[0]=='Coreference':
    for i in range(len(text7)):
        if text7[i]=='Coreference':
            #print('entered')
            fp.write('\n')
            fp.write(text7[i]+' ')
            #print(text7[i]+ ' ')
        else:
            fp.write(text7[i]+ ' ')
            #print(text7[i]+ ' ')
#for i in output['sentences']:
 #   print(i)
fp.close()
totalnoun=[]
num=0
fp=open('modifiedconll.txt','w')
modifying=[]
with open('coref.txt','r') as f:
    l=1
    k=l
    flag=0
    for j in f:
        modifying.append(j)

for i in range(len(modifying)-1):
    if "NN" in modifying[i] and 'NN' in modifying[i+1]:
        z=modifying[i].split()
        z[z.index('NN')]='JJ'
        z.append("\n")
        modifying[i]="\t".join(z)
modifying.pop()
for i in modifying:
    fp.write(i)
fp.close()
tag1=[]
tags=[]
with open('modifiedconll.txt','r') as f:
    for j in f:
        text=j.split()
        if len(text)>0:
            tag1.append(text[3])
            tags.append(text[2])
tagflag=0
print('tags is',tags)
print('tag1 is',tag1)
string1=''
listofstrings=[]
for i in range(len(tag1)):
    if tag1[i]!='NN' and tag1[i]!='NNS':
        if tag1[i]=='JJ':
            tagflag+=1
            if string1=='':
                if tags[i] not in ['front','next','left','right']:
                    #print('378')
                    string1+=tags[i]
                print(tags[i])
                print(string1)
            else:
                #print('381')
                if tags[i] not in ['front','next','left','right']:
                    string1=string1+'_'+tags[i]
                
    else:
        tagflag=0
        #print('385')
        listofstrings.append(string1)
        string1=''
countfortellingnoun=0
print(listofstrings)
with open('modifiedconll.txt','r') as f:
    a=f.readlines()
    #print("Value of a is",a)
    for j in a:
        #print(j)
        text=j.split()
        for l in range(len(text)-2):
                if text[l]=='CD' and text[l-2].isdigit()==True:
                    num=text[l-2]
                if text[l]=='CD' and text[l-2].isdigit()==False:
                    num=text2int(text[l-2])
                if text[l]=='NNS':
                    j=sample.index(text[l-2])
                    print("the index of",text[l-2],"is",j,text[l-1])
                    
                    sample[j]=text[l-1]
                    if listofstrings[countfortellingnoun]!='':
                        for i in range(num):
                            totalnoun.append(listofstrings[countfortellingnoun]+'_'+text[l-1])
                            countfortellingnoun+=1  
                    else:
                        for i in range(num):
                            totalnoun.append(text[l-1])
                if text[l]=='NN' and text[l-2]!='front' and text[l-2]!='next':
                    print('413')
                    if listofstrings[countfortellingnoun]!='':
                        print('415')
                        if (listofstrings[countfortellingnoun]+'_'+text[l-2]) not in totalnoun:
                            print('417')
                            totalnoun.append(listofstrings[countfortellingnoun]+'_'+text[l-2])
                            countfortellingnoun+=1
                       
                    else:
                         print('422')
                         if (text[l-2]) not in totalnoun:
                             totalnoun.append(text[l-2])
                             print(countfortellingnoun)
                             countfortellingnoun+=1
print(totalnoun)
totalnoun1=[]
for i in totalnoun:
    if i not in wall1 and i not in ['right','left']:
        totalnoun1.append(i)
#print(num)

multipleflag=1
dontflag=0
dontdo=0
baseflag=0
nexttonpflag=0
fp1.write(str(totalnoun1)+'\n')
if mweflag==1:
    for j in mwestring:
       if j!='':
            print('488',j)
            for i in range(len(totalnoun)):
                if '-' not in totalnoun[i]:
                    print('hello world\n',totalnoun[i])
                    totalnoun[i]=totalnoun[i]+'-'+str(sample.index(totalnoun[i]))
            print('totalnoun before',totalnoun)
            for k in totalnoun:
                if 'wall' in k:
                    print('k is',k)
                    
                    dontdo=1
            #if onflag==1:
             #   totalnoun=totalnoun[::-1]
            totalnoun3=[]
            if len(totalnoun)>2:
                for z in totalnoun:
                    if totalnoun.count(z)>1 and baseflag==0:
                        totalnoun3.append(z)
                        print('totalnoun3 is',totalnoun3)
                        multipleflag=totalnoun.count(z)
                        baseflag=1
                    elif totalnoun.count(z)==1:
                        totalnoun3.append(z)
                    
            else:
                totalnoun3=totalnoun[:2]
            if len(totalnoun3)>2:
                totalnoun3=totalnoun3[:2]
            if certainflag==2 or onflag==2 :
                totalnoun3=totalnoun3[::-1]
            print('total 3 noun after',totalnoun)
            totalnoun4=totalnoun3
            totalnoun3=','.join(totalnoun3)
            print('totalnoun after afrer',totalnoun3)
            for k in range(multipleflag):
                print('523 roxx')
                if j!='' and dontdo==0:
                    fp1.write('nmod:'+j +'(')
                    for i in totalnoun3:
                        if i!='-' and  i.isdigit()==0:
                            fp1.write(i)
                    fp1.write(' )')
                fp1.write('\n')
    if(len(splittext)!=0):
        if len(andnoun)!=0:
        #print(andnoun)
            print('it has entered line 527\n')
            for i in range(len(splittext)):
                splittext1=splittext[i].split(":")
                splittext2=splittext1[1].split('(')
                splittext2[0]+='('
                splittext3=splittext2[1].split('-')
                print('splittext 3 is',splittext3)
                for j in splittext3:
                    print('j in line 535',j)
                    print(totalnoun3)
                    if j in totalnoun3:
                        dontflag=1
                splittext3[0]=','.join(andnoun)
                splittext3[1]=splittext3[1].split(',')
                splittext3[1][0]+=')'
                splittext3[1]=",".join(splittext3[1])
                #print(splittext3)
                splittext3='-'.join(splittext3)
                splittext2[1]=splittext3
                splittext2='('.join(splittext2)
                splittext1[1]=splittext2
                splittext1=':'.join(splittext1)
                splittext[i]=splittext1
                print(splittext)
                for j in splittext:
                    for k in j:
                        if k!='-' and k.isdigit()==0:
                            fp1.write(k)
                    fp1.write('\n')
        else:
            for key in range(len(splittext)):
                splittext1=splittext[key].split(":")
                splittext2=splittext1[1].split('(')
                splittext3=splittext2[1].split('-')
                print('splittext 3 is',splittext3)
                for j in splittext3:
                    print('j in line 564',j)
                    if j[-1]=='s':
                        spli=list(j)
                        spli[-1]=''
                        j="".join(spli)
                    print(totalnoun3)
                    if j in totalnoun3 and dontdo==0:
                        dontflag=1
                splittext3[1]=splittext3[1].split(',')
                splittext3[1]=",".join(splittext3[1])
                #print(splittext3)
                splittext3='-'.join(splittext3)
                splittext2[1]=splittext3
                splittext2='('.join(splittext2)
                splittext1[1]=splittext2
                splittext1=':'.join(splittext1)
                splittext[key]=splittext1                            
                print('splittext is', splittext)
                print('dont flag is',dontflag)
            for k in range(multipleflag):
                for key in splittext:
                    for enter in key:
                        print('hello 592',enter)
                        if enter!='-' and enter.isdigit()==0 and dontflag==0:
                            fp1.write(enter)
                    fp1.write('\n')
                print('hello')
            

        
        
else:
    totalnoun3=[]
    if len(totalnoun)>2:
        for z in totalnoun:
            if totalnoun.count(z)>1 and baseflag==0:
                totalnoun3.append(z)
                print('totalnoun3 is',totalnoun3)
                multipleflag=totalnoun.count(z)
                baseflag=1
            elif totalnoun.count(z)==1:
                totalnoun3.append(z)
                
    if len(andnoun)!=0:
        #print(andnoun)
        for i in range(len(splittext)):
            splittext1=splittext[i].split(":")
            splittext2=splittext1[1].split('(')
            splittext2[0]+='('
            splittext3=splittext2[1].split('-')
            splittext3[0]=','.join(andnoun)
            splittext3[1]=splittext3[1].split(',')
            splittext3[1][0]+=')'
            splittext3[1]=",".join(splittext3[1])
            #print(splittext3)
            splittext3='-'.join(splittext3)
            splittext2[1]=splittext3
            splittext2='('.join(splittext2)
            splittext1[1]=splittext2
            splittext1=':'.join(splittext1)
            splittext[i]=splittext1
            print(splittext)
            for j in splittext:
                for k in j:
                    if k!='-' and k.isdigit()==0:
                        fp1.write(k)
                fp1.write('\n')
    
    else:
        for i in range(len(splittext)):
            splittext1=splittext[i].split(":")
            splittext2=splittext1[1].split('(')
            if multipleflag>1 and 'npmod' in splittext2[0]:
                splittext2[0]='next_to'
                splittext2[1]=",".join(totalnoun3)+')'
                nexttonpflag=1
                
            if nexttonpflag!=1:    
                splittext3=splittext2[1].split('-')
                print('splittext3 is',splittext3)
                for m in splittext3:
                    if m[-1]=='s':
                        n=splittext3.index(m)
                        spli=list(m)
                        spli[-1]=''
                        m="".join(spli)
                        splittext3[n]=m
                splittext3[1]=splittext3[1].split(',')
                
                splittext3[1]=",".join(splittext3[1])
                #print(splittext3)
                splittext3='-'.join(splittext3)
                splittext2[1]=splittext3
            splittext2='('.join(splittext2)
            splittext1[1]=splittext2
            splittext1=':'.join(splittext1)
            splittext[i]=splittext1
        print('splittext is', splittext)
        for k in range(multipleflag):
            for i in splittext:
                if 'are' not in i:
                    for j in i:
                        if j!='-' and j.isdigit()==0:
                            fp1.write(j)
                    fp1.write('\n')
            print('hello')
fp1.close()
#fp.close()

















#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:23:10 2017

@author: ninaad
"""
fp=open("example1",'w')
def parent(a,j):
    str2=' '
    str1=''
    i=len(a[j])-3
    while(i!=0):
        if(a[j][i]==','):
            break
        str2+=a[j][i]
        
        i-=1
    print(str2,"\n\n\n")
    str1=''
    i=len(str2)-1
    while(i!=0):
        str1+=str2[i]
        i-=1
    str2=str1    
    print(str2)
    str1=''
    for i in str2:
        if(i=='-'):
            break
        str1+=i
    str2=str1
    return str2

def children(a,j):
    str1=''
    bracket1="("
    bracket2=")"
    flagbracketopen=0
    flagbracketclose=0
    for i in a[j]:
        if(flagbracketopen-1==flagbracketclose and i==','):
            break
        if(flagbracketopen>0):
            str1+=i
        if(i == bracket1):
            flagbracketopen+=1
        if(i == bracket2):
            flagbracketclose+=1
        
        
            
    str2=''
    for i in str1:
        if(i=='-'):
            break
        str2+=i
    str1=str2
    if(str1.count(",")>0):
        str1=str1[1:-1]
        str1 = [x for x in str1.split(',') if x.strip()]
        return str1
    else:
        asd=[]
        asd.append(str1)
        return asd
def preposition(a,j):
    str1=''
    bracket1="("
    for i in a[j]:
        if(i==bracket1):
            break
        str1+=i
    
    str1=str1[5:]
    if('in_front_of' in str1):
        str1='front'
    elif('on' in str1):
        str1='on'
    elif('right' in str1):
        str1='right'
    elif('next' in str1):
        str1='next'
    elif('beside' in str1):
        str1='beside'
    elif('left' in str1):
        str1='left'
    elif('back' in str1):
        str1='back'
    elif('behind' in str1):
        str1='behind'
    
        
    return str1
with open("relations.txt",'r') as f:
    a=f.readlines()
flag=0 
for i in a:
    print(i)
apos=0
listofnouns2=[]
stringfornouns=""
for i in a[0]:    
    if(i=="'"):
        apos+=1
    if(apos%2==1):
        stringfornouns+=i
    else:
        if(stringfornouns!=""):
            stringfornouns=stringfornouns[1:]
            listofnouns2.append(stringfornouns)
            stringfornouns=""
            
listofstrings1=[]
listofstrings2=[]        
print("aosdoasdio123\n",listofnouns2)

for i in listofnouns2:
    print(i)
listofindependent=listofnouns2  
if(len(a)<=1):
    for i in listofnouns2:
            fp.write(i)
            fp.write(" info 0 0\n")
            
    
else:
    j=1
    while(j<(len(a))):
        if(len(a[j])>2):
            parentobj=parent(a,j)
            #print("lalalala1")
            #print(parentobj)
            childrenobj=children(a,j)
            print("lalalala2")
            print(childrenobj)
            prepobj=preposition(a,j)
            #print("lalalala3")
            #print(prepobj)
            #print("qwertyui",set(listofnouns2),set(childrenobj),"\n\n")
            #print("opwqei\n")
            listofindependent=list(set(listofindependent)-set(childrenobj))
            #print("aisdjoaisjd",listofindependent)
            
                
            for i in childrenobj:
                if (i not in wall1):
                    listofstrings1.append(i+" info "+prepobj+" "+parentobj+"\n")
            
        j+=1
    for i in listofindependent:
        if(i not in wall1):
            listofstrings2.append(i+" info 0 0\n")
                
    for i2 in listofstrings2:
        fp.write(i2)
    for i2 in listofstrings1:
        fp.write(i2)

fp.close()






#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 12:08:06 2017

@author: ninaad
"""

import pandas as pd
from operator import itemgetter
fp=open('testoutput','w')
with open('example1') as f:
    content = f.readlines()
listofwords=[]
for i in content:
    s=''
    for j in i:
        if(j!=' '):
            s+=j
        else:
            break
    listofwords.append(s)

while("\n" in listofwords):
    listofwords.remove("\n")
listofsyn=['2773838', '2801938', '2871439', '2876657', '2933112', '2946921', '2992529', '3001627', '3046257', '3085013', '3211117', '3261776', '3320046','3337140', '3636649', '3642806', '3759954', '3797390', '4004475', '4256520', '4379243', '4401088']
dictlocation={}
dictscale={}

path='csv/'
for d in listofsyn:
    f='0'
    f+=d
    c=f
    f+='.csv'
    #print(f)
    f1=path+f
    df = pd.read_csv(f1)
    saved_column = df['wnlemmas']
    #print(saved_column)
    l=[]
    for i in saved_column:
        #print(i)
        s=''
        for j in i:
            if(j!=';'):
                if(j==' '):
                    s+='_'
                else:
                    s+=j.lower()
               
            else:
                if(s not in l):
                    l.append(s)
                s=''
           
        if(s not in l):
            l.append(s)
            
    
    dictlocation[f1]=l
    #print('dictlocation is' , dictlocation['/home/ninaad/Desktop/csv/02871439.csv'])

listofaddress=[]
listofid=[]
listofeverything=[]
for i1 in listofwords:
    print("i1 is ",i1)
    flag=0
    listofidlem=[]
    #print(dictlocation)
    for i in dictlocation:
        if(i1 in dictlocation[i]):
            #print("i1 is ",i1)
            if(flag==0):
                listofaddress.append(i[-11:-4])
                flag=1
            #print(listofaddress)
            print("Value of i is",i)
            df = pd.read_csv(i)
            saved_column_wnlemmas = df['wnlemmas']
            saved_column_fullId   = df['fullId']
            saved_column_implied  = df['implied']
            saved_column_scale    = df['scale']
      
            #if(saved_column_implied[2]=='wall'):
              #print("KLSAKALSK\n\n\n",i,dictlocation[i])
           # print(saved_column_wnlemmas)
            for j in range(len(saved_column_wnlemmas)):
                #make underscore into space
                f=i1
                f=f.replace('_',' ')
                if(f in saved_column_wnlemmas[j]):
                    #print(saved_column_wnlemmas[j],saved_column_fullId[j],"\n")
                    listofidlem.append([saved_column_wnlemmas[j],saved_column_fullId[j],saved_column_implied[j],i[-11:-4]])


    #print('listofidlem',listofidlem)
    for i in range(len(listofidlem)):
        listofidlem[i].append(listofidlem[i][0].count(';'))
       
    listofidlem=sorted(listofidlem,key=itemgetter(4))
    #print('listofidlem is at 737',listofidlem)
    if len(listofidlem)!=0:
        happy_variable=listofidlem[0][2]
        happy_variable1=listofidlem[0][3]
        idoffile=listofidlem[0][1][4:]
        #print(idoffile)
        g="csv"+'/0'+ happy_variable1+'.csv'
        df = pd.read_csv(g)
        saved_column_scale    = df['scale']
        print("Scale 1 is ",saved_column_scale[0])
        listofeverything.append([i1,happy_variable,happy_variable1,idoffile,str(int(saved_column_scale[0]))])
        #print(listofeverything)
if len(listofeverything)!=0:
    for i in listofeverything:
        fp.write(str(i))
        
        
        fp.write("\n")
       
print(listofeverything)
fp.close()
#cwd='Text to 3d Scene',
subprocess.call('blender base.blend  --python blender.py',shell=True)