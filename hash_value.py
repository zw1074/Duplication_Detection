import pickle
from parse_hash import *
import numpy as np
from multiprocessing import Pool
with open("data_parse.pkl", "rb+") as fobj:
    data_parse = pickle.load(fobj)
global vec_list
def hash_value(s, vec_list, n):
    """
    Use locality sensitive hashing to hash the string

    Input:
        s - TODO
        vec_list - TODO

    Output:
        TODO
    """
    value = 0
    for i in xrange(n):
        key_value = 0
        for key in s.keys():
            if key not in ['id','country','valid']:
                if type(s[key]) == list:
                    key_value += vec_list[key][i]*sum([hashString(j) for j in s[key]])
                else:
                    key_value += vec_list[key][i]*hashString(s[key])
        value += 2**(i)*int(np.max([0, np.sign(key_value)]))
    return value

def Generate_vec(n):
    """
    Generate different subspace

    Input:
        n - TODO

    Output:
        TODO
    """
    vec_list = {}
    key_name = ['city', 'firstname', 'skills', 'lastname', 'fullstate', 'skillWords', 'prefixes', 'state', 'street', 'suffixes']
    for key in key_name:
        vec_list[key] = np.random.normal(0.0, 100.0, 1000)
    return vec_list

def f(s):
    return (hash_value(s, vec_list, 100), s['id'])

hash_table = {}
n = 100
vec_list = Generate_vec(n)
p = Pool(8)
test = p.map(f, data_parse)
hash_table = {}
for i in test:
    hash_table.setdefault(i[0], [])
    hash_table[i[0]].append(i[1])
with open('hash_table.npy', 'wb+') as fobj:
    pickle.dump(hash_table, fobj)
# for i in data_parse:
#     print i['id']
#     value = hash_value(i, vec_list, 1000)
#     hash_table.setdefault(value, [i['id']])
#     hash_table[value].append(i['id'])
