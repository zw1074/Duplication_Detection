import pickle
with open("training_ground_truth.csv") as fobj:
    truth = fobj.readlines()
with open("ip_list7.npy", 'rb+') as fobj:
    ip_list = pickle.load(fobj)

with open("data_parse.pkl",'rb+') as fobj:
    data = pickle.load(fobj)

# Change to dict
ip_dict = dict((x,1) for x in ip_list)
k = 0
notin = []
for i in truth:
    i = i.strip()
    j = tuple(sorted([int(i.split(',')[0]), int(i.split(',')[1])]))
    try:
        ip_dict[j]
        k += 1
    except KeyError:
        notin.append(j)
        continue
print k
