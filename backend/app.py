from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
import json
from flask import Flask, request
import requests

app = Flask(__name__)

fires = json.load(open('emergencies.json'))
fire_stations = open('hubs.txt').read().split('\n')[:-1]


# In[2]:


fire_stations = [x.split(', ') for x in fire_stations]
fire_stations = [[float(x[1]), float(x[0])] for x in fire_stations]


# In[3]:


# create new figure, axes instances.
'''
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=32., llcrnrlat=34., urcrnrlon=35., urcrnrlat=36.,
            resolution='i', projection='merc')
'''

data = []
for fire in fires:
    # x, y = m(fire['longitude'], fire['latitude'])
    data.append([fire['longitude'], fire['latitude'], fire['frp']])
    # m.plot(x, y, 'o')

# draw great circle route between NY and London
# m.drawcoastlines()
# m.fillcontinents()
# plt.show()


# In[4]:


'''
print(len(data))
data_all = data
data = []
for fire in data_all:
    for fire_close in data:
        if euc_dist(fire_close, fire) < 0.0005:
            break
    else:
        data.append(fire)
len(data)'''


def euc_dist(a, b):
    return (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])


db = DBSCAN(eps=0.0003, min_samples=1, metric=euc_dist)
db = db.fit(data, sample_weight=[x[2] for x in data])


# In[5]:


num_labels = 0
for label in db.labels_:
    num_labels = max(num_labels, label + 1)

all_data = np.zeros((num_labels, 3))
fire_cnt = np.zeros(num_labels)
for fire, label in zip(data, db.labels_):
    all_data[label] += fire
    fire_cnt[label] += 1
for ind, cnt in enumerate(fire_cnt):
    all_data[ind] /= cnt
all_data


# In[6]:


data = all_data
'''
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=32.,llcrnrlat=34.,urcrnrlon=35.,urcrnrlat=36.,            resolution='i',projection='merc')

for fire in data:
    x,y = m(fire[0], fire[1])
    m.plot(x,y, 'o')

# draw great circle route between NY and London
m.drawcoastlines()
m.fillcontinents()
plt.show()
'''

# In[7]:


len(data)


# In[18]:


def precompute_dist():
    global distance_matrix
    global centers
    fires_used = 80
    fire_ind = 0
    distance_matrix = [[] for x in range(len(centers))]
    while fire_ind < len(data):
        if fires_used + fire_ind > len(data):
            fires_used = len(data) - fire_ind
        coord_string = ";".join([",".join(list(map(str, fire[:2]))) for fire in data[fire_ind: fires_used + fire_ind]])
        coord_string += ";" + ";".join([",".join(list(map(str, fire_st))) for fire_st in centers])
        sources = ";".join([str(x) for x in range(fires_used,
                                                  fires_used + len(centers))])
        destinations = ";".join([str(x) for x in range(fires_used)])
        url = 'http://127.0.0.1:5000/table/v1/driving/' \
              f'{coord_string}?sources={sources}&destinations={destinations}'
        r = requests.get(url).json()
        r = r['durations']
        for i, x in enumerate(distance_matrix):
            for y in r[i]:
                distance_matrix[i].append(y)
        fire_ind += fires_used


def dist(fire, firest):
    return distance_matrix[firest][fire]


# In[19]:
data = np.array(data)


@app.route('/fires')
def fires():
    json_data = json.dumps(data.tolist())
    return '{"data": ' + json_data + '}'


@app.route('/get')
def get():
    NUM = 30
    NUM_ITERS = 5
    if request.args.get('num'):
        NUM = int(request.args.get('num'))
    global centers
    res_data = {
        "old": [],
        "new": [],
        "effect": []
    }
    best_risk = 0
    for init_iter in range(NUM_ITERS):
        centers = data[np.random.choice(len(data), NUM)][:, :2]
        centers[:len(fire_stations)] = fire_stations
        col = [0] * len(data)
        old_risk = 0
        new_risk = 0
        risk = 0
        for it in range(5):
            print(it)
            cnt = [0] * NUM
            tot = [[0, 0]] * NUM
            precompute_dist()
            print('Found distances')
            for fire_ind, fire in enumerate(data):
                mind = 100000
                mindpos = -1
                for pos, center in enumerate(centers):
                    if mind > dist(fire_ind, pos):
                        mind = dist(fire_ind, pos)
                        mindpos = pos
                col[fire_ind] = mindpos
                tot[mindpos] += fire[2] * fire[:2]
                cnt[mindpos] += fire[2]
                MIN_DIST = 10
                risk += fire[2] / max(mind, MIN_DIST)
                if mindpos < len(fire_stations):
                    old_risk += fire[2] / max(mind, MIN_DIST)
                else:
                    new_risk += fire[2] / max(mind, MIN_DIST)
            for pos, center in enumerate(centers):
                if cnt[pos] == 0 or pos < len(fire_stations):
                    continue
                centers[pos] = tot[pos] / cnt[pos]
            print(centers)
        old_risk /= len(fire_stations)
        new_risk /= (len(centers) - len(fire_stations))

        curr_res_data = {
            "old": [],
            "new": [],
            "effect": []
        }
        for ind, center in enumerate(centers):
            if ind < len(fire_stations):
                curr_res_data['old'].append(center.tolist())
            else:
                curr_res_data['new'].append(center.tolist())
            curr_res_data['effect'] = [old_risk, new_risk]

        if risk > best_risk:
            res_data = curr_res_data
            best_risk = risk

        return json.dumps(res_data)

# In[16]:


'''
fig=plt.figure()

ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=32.,llcrnrlat=34.,urcrnrlon=35.,urcrnrlat=36.,            resolution='i',projection='merc')

m.drawcoastlines()
m.fillcontinents()

colors = plt.cm.tab20
cluster = {}
for c, fire in zip(col, fires):
    if c==-1:
        continue
    x,y = m(fire['longitude'], fire['latitude'])
    if c in cluster:
        cluster[c].append((x,y))
    else:
        cluster[c] = [(x,y)]
for x in cluster:
    xs, ys = zip(*cluster[x])
    plt.scatter(xs, ys, marker='o', zorder=100)
for ind, c in enumerate(centers):
    xs, ys = m(c[0], c[1])
    print(c)
    if ind < len(fire_stations):
        plt.scatter(xs, ys, c='r', marker='s', zorder=101)
    plt.scatter(xs, ys, c='r', marker='x', zorder=101)

plt.show()


# In[ ]:



'''

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
