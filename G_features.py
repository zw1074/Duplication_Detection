# -*- coding: utf-8 -*-
'''''
Feature 0: 0 reserved
Feature 1: a.Country=b.Country
Feature 2: a.name=b.name (hash)
Feature 3: a.street=b.street (hash)
Feature 4: a.firstname=b.firstname (hash)
Feature 5: a.lastname=b.lastname (hash)
Feature 6: minimum number of words in name, assume "names" is a list of string without prefixes & suffixes
Feature 7: max...
Feature 8: proportion of characters in shared words --todo
Feature 9: proportion of shared words               --todo
Feature 10: name similarity, close to LCS
Feature 11: Similar to 10, but with prefixes and suffixes
Feature 12: Proportion of shared suffixes
Feature 13: Proportion of shared prefixes
Feature 14: Common Char of firstname
Feature 15: Common Char of lastname
Feature 16: LCS of firstname, similar to F14
Feature 17: LCS of lastname, similar to F15
Feature 18: Common Char of skills
Feature 19,20: Similar to F6,7, but with whole name(pre and suffixes)
Feature 21: Common Char in street
Feature 22: Common Char in name
Feature 23: State similarity: just the length of shared prefix in two strings
Feature 24: Count Common of skill words
'''''

'''''
need to add to parse:
name 有空格，没有前缀与后缀
names split by 空格
hash_names list of hash value
hash_name
whole_names(with title, list) 所有都有，split by 空格
hash_whole_names(list)
fix skills to be string
'''''
import pickle
import csv
import numpy as np
def cleanStringAlpha(string):
        k=""
        for i in string:
                if i.isalpha():
                        k=k+i.upper()
        return k
def cleanStringAlnum(string):
        k=""
        for i in string:
                if i.isalnum():
                        k=k+i.upper()
        return k
def hashString(s):#32-bit rolling hash
        if len(s):s=''.join(sorted(s))
        x=0
        for i in range(0,len(s)):
                #print s[i]
                x=x*131+ord(s[i].upper())
        return x
def nameSimilarity(names1,names2,hash_names1,hash_names2):
    #names is a list of string
    #hash_name is a list of hash value
    score=np.zeros((len(names1)+1,len(names2)+1))
    for i in range(0,len(names1)):
        for j in range(0,len(names2)):
            same=0
            try:
                if names1[i][0]==names2[j][0]: same=1
                if hash_names1[i]==hash_names2[j]: same=2
            except IndexError:
                continue
            score[i+1][j+1]=max(score[i+1][j+1],score[i][j]+same)
            score[i][j]=max(score[i][j+1],score[i][j])
            score[i+1][j]=max(score[i+1][j],score[i][j])
    return score[len(names1)][len(names2)]
def stateSimilarity(s1,s2):
    if len(s1)==0 or len(s2)==0: return 0
    i=0
    while i<len(s1) and i<len(s2) and s1[i]==s2[i]:i+=1
    return i
def countCommon(list1,list2):
    return len(set(list1) & set(list2))
def countCommonChar(string1,string2):
    s1=''.join(sorted(string1))
    s2=''.join(sorted(string2))
    pa=0
    pb=0
    common=0
    while(pa<len(s1) and pb < len(s2)):
        if (s1[pa]==s2[pb]):
            pa+=1
            pb+=1
            common+=1
        elif s1[pa] < s2[pb]:
            pa+=1
        else:
            pb+=1
    return 1.0 * common / max(1,min(len(s1),len(s2)))
def LCS(s1, s2):
    score=np.zeros((len(s1)+1,len(s2)+1))
    for i in range(0,len(s1)):
        for j in range(0,len(s2)):
            score[i+1][j+1]=max(score[i+1][j+1],score[i][j]+(s1[i]==s2[j]))
            score[i+1][j]=max(score[i+1][j],score[i][j])
            score[i][j+1]=max(score[i][j+1],score[i][j])
    return 1.0*score[len(s1)][len(s2)] / max(1, min(len(s1),len(s2)))
# ParsedEntry=pickle.load(open("parse.o","rb"))
#print ParsedEntry
#print ParsedEntry[0]["city"]

def extract_feature(ParsedEntry,ida,idb):
    feature_list=[]
    feature_list.append(0)#Feature 0
    feature_list.append(int(ParsedEntry[ida]["country"]==ParsedEntry[idb]["country"]))#Feature 1
    feature_list.append(int(hashString(ParsedEntry[ida]["fullname"])==hashString(ParsedEntry[idb]["fullname"]))) #F2
    feature_list.append(int(hashString(ParsedEntry[ida]["street"])==hashString(ParsedEntry[idb]["street"])))#F3
    feature_list.append(int(hashString(ParsedEntry[ida]["firstname"])==hashString(ParsedEntry[idb]["firstname"])))#F4
    feature_list.append(int(hashString(ParsedEntry[ida]["lastname"])==hashString(ParsedEntry[idb]["lastname"])))#F5
    feature_list.append(min(len(ParsedEntry[ida]["names"]),len(ParsedEntry[idb]["names"])))#F6
    feature_list.append(max(len(ParsedEntry[ida]["names"]),len(ParsedEntry[idb]["names"])))#F7
    #F8
    #F9
    feature_list.append(nameSimilarity(ParsedEntry[ida]["names"],ParsedEntry[idb]["names"],ParsedEntry[ida]["hash_names"],ParsedEntry[idb]["hash_names"]) / float(min(len(ParsedEntry[ida]["names"]),len(ParsedEntry[idb]["names"])))) #F10
    feature_list.append(nameSimilarity(ParsedEntry[ida]["whole_names"],ParsedEntry[idb]["whole_names"],ParsedEntry[ida]["hash_whole_names"],ParsedEntry[idb]["hash_whole_names"]) / float(min(len(ParsedEntry[ida]["whole_names"]),len(ParsedEntry[idb]["whole_names"])))) #F11

    if ParsedEntry[ida]['suffixes']==ParsedEntry[idb]['suffixes']:
        sus=1
    else:
        sus=1.0*countCommon(ParsedEntry[ida]['suffixes'],ParsedEntry[idb]['suffixes']) / max(len(ParsedEntry[ida]['suffixes']),len(ParsedEntry[idb]['suffixes']))
    feature_list.append(sus)#F12

    if ParsedEntry[ida]['prefixes']==ParsedEntry[idb]['prefixes']:
        prs=1
    else:
        prs=1.0*countCommon(ParsedEntry[ida]['prefixes'],ParsedEntry[idb]['prefixes']) / max(len(ParsedEntry[ida]['prefixes']),len(ParsedEntry[idb]['prefixes']))
    feature_list.append(prs)#F13
    feature_list.append(countCommonChar(ParsedEntry[ida]["firstname"],ParsedEntry[idb]["firstname"]))#F14
    feature_list.append(countCommonChar(ParsedEntry[ida]["lastname"],ParsedEntry[idb]["lastname"]))#F15
    feature_list.append(LCS(ParsedEntry[ida]["firstname"],ParsedEntry[idb]["firstname"]))#F16
    feature_list.append(LCS(ParsedEntry[ida]["lastname"],ParsedEntry[idb]["lastname"]))#F17
    feature_list.append(countCommonChar(ParsedEntry[ida]["skills"],ParsedEntry[idb]["skills"]))#F18
    feature_list.append(min(len(ParsedEntry[ida]["whole_names"]),len(ParsedEntry[idb]["whole_names"])))#F19
    feature_list.append(max(len(ParsedEntry[ida]["whole_names"]),len(ParsedEntry[idb]["whole_names"])))#F20
    feature_list.append(countCommonChar(cleanStringAlnum(ParsedEntry[ida]["street"]),cleanStringAlnum(ParsedEntry[idb]["street"])))#F21
    feature_list.append(countCommonChar(cleanStringAlpha(ParsedEntry[ida]["name"]),cleanStringAlpha(ParsedEntry[idb]["name"])))#F22
    feature_list.append(stateSimilarity(ParsedEntry[ida]["state"],ParsedEntry[idb]["state"]))#F23
    feature_list.append(1.0 * countCommon(ParsedEntry[ida]["skillWords"],ParsedEntry[idb]["skillWords"]) / max(1,min(len(ParsedEntry[ida]["skillWords"]),len(ParsedEntry[idb]["skillWords"]))))#F24
    return feature_list
# print extract_feature(ParsedEntry,11,1)
# print ParsedEntry[11]
# print ParsedEntry[1]
#names1=["tom","cat","jerry","mouse"]
#names2=["tos","sdflisjf","jerry","mouse","cat"]
#names2=["the","bone","of","sword"]
#hash_name1=[hashString(names1[0]),hashString(names1[1]),hashString(names1[2]),hashString(names1[3])]
#print hash_name1
#hash_name2=[hashString(names2[0]),hashString(names2[1]),hashString(names2[2]),hashString(names2[3]),hashString(names2[4])]
#print hash_name2
#print nameSimilarity(names1,names2,hash_name1,hash_name2)
# print stateSimilarity("CT13873","CO80222")
