import pickle
import numpy as np
from parse_hash import *
import itertools
from multiprocessing import Pool
import time
import gc

global dic

def generate_combination(data):
    b = []
    for key in data.keys():
        if len(data[key]) > 1:
            b += list(itertools.combinations(data[key], 2))
    return b

def transform(data_parse):
    dics = []
    for i in data_parse:
        if 'state' in i.keys():
            dics.append(i)
    return sorted(dics, key = lambda x:hashString(x['fullname']))

def transform2(data_parse):
    dics = []
    for i in data_parse:
        if 'state' in i.keys():
            dics.append(i)
    return sorted(dics, key = lambda x:hashString(x['state']))

def interest1(x,y):
    for key in x.keys():
        if key in ['fullname', 'firstname', 'lastname']:
            if type(x[key]) == list:
                a = sum([hashString(i) for i in x[key]])
                b = sum([hashString(i) for i in y[key]])
            else:
                try:
                    a = hashString(x[key])
                    b = hashString(y[key])
                except KeyError:
                    continue
            if np.abs((a - b)/float(b+1)) <= 0.1:
                continue
            else:
                return False
    return True

def interest2(x,y):
    for key in x.keys():
        if key in ['fullstreet', 'street', 'city']:
            if type(x[key]) == list:
                a = sum([hashString(i) for i in x[key]])
                b = sum([hashString(i) for i in y[key]])
            else:
                try:
                    a = hashString(x[key])
                    b = hashString(y[key])
                except KeyError:
                    continue
            if key == 'fullstreet':
                if np.abs((a - b)/float(b+1)) <= 1e-12:
                    return True
                else:
                    continue
            else:
                if np.abs((a - b)/float(b+1)) <= 0.001:
                    continue
                else:
                    return False
    return True

def f1(i):
    j = i+1
    pairs = []
    try:
        x = dic[i]
        a = hashString(dic[i]['fullname'])
        b = hashString(dic[j]['fullname'])
    except IndexError:
        return pairs
    while np.abs(a - b)/float(a+1) <= 0.1 and abs(j-i) <= 100:
        y = dic[j]
        if interest1(x,y):
            pairs.append(sorted([int(dic[i]['id']),int(dic[j]['id'])]))
        j += 1
        try:
            b = hashString(dic[j]['fullname'])
        except IndexError:
            return pairs
    return pairs

def f2(i):
    j = i+1
    pairs = []
    try:
        a = hashString(dic[i]['state'])
        b = hashString(dic[j]['state'])
    except IndexError:
        return pairs
    while abs(a - b)/float(b+1) <= 0.001:
        if interest2(dic[i],dic[j]):
            pairs.append(sorted([int(dic[i]['id']),int(dic[j]['id'])]))
        j += 1
        try:
            b = hashString(dic[j]['fullstreet'])
        except IndexError:
            return pairs
    return pairs

def find_ip(result):
    ip_list = []
    for i in result:
        if i.__len__() > 0:
            for j in i:
                ip_list.append(j)
    return ip_list

def parallel_process(f):
    result = []
    for i in range((len(dic) - 1)/1000 + 1):
        i_list = range(i*1000, i*1000 + 1000)
        p = Pool(8)
        result += p.map(f, i_list)
        p.close()
        gc.collect()
    return result

#with open('hash_table.npy','rb+') as fobj:
#    data = pickle.load(fobj)
with open('data_parse.pkl', 'rb+') as fobj:
    data_parse = pickle.load(fobj)
dic = transform(data_parse)
t = time.time()
result = []
for i in range((len(dic) - 1)/1000 + 1):
    print i
    i_list = range(i*1000, i*1000 + 1000)
    p = Pool(8)
    result += p.map(f1, i_list)
    p.close()
    gc.collect()
print time.time() - t
with open('ip_list_name_2.npy','wb+') as fobj:
    pickle.dump(result, fobj)
dic = transform2(data_parse)
t = time.time()
result2 = []
i_lists = range((len(dic) - 1)/1000 + 1)
for i in i_lists:
    print i
    i_list = range(i*1000, i*1000 + 1000)
    p = Pool(8)
    result2 += p.map(f2, i_list)
    p.close()
    gc.collect()
print time.time() - t
with open('ip_list_street_new_2.npy','wb+') as fobj:
    pickle.dump(result2, fobj)
# with open('ip_list_street_new_2.npy','rb+') as fobj:
#     result2 = pickle.load(fobj)
# with open('ip_list_name.npy','rb+') as fobj:
#     result = pickle.load(fobj)
# with open('ip_list_street_1.npy','rb+') as fobj:
#     result2 = pickle.load(fobj)
# with open('ip_list_street_2.npy','rb+') as fobj:
#     result3 = pickle.load(fobj)

ip_list = find_ip(result)
ip_list2 = find_ip(result2)
# ip_list3 = find_ip(result3)
ip_list = map(lambda x: tuple(x), ip_list)
ip_list2 = map(lambda x: tuple(x), ip_list2)
# ip_list3 = map(lambda x: tuple(x), ip_list3)
ip_list_final = list(set(ip_list + ip_list2))
with open('ip_list7.npy', 'wb+') as fobj:
    pickle.dump(ip_list_final, fobj) 

