import pandas as pd
import datetime as datetime

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from sklearn.cluster import KMeans
from sklearn import datasets

df = pd.read_csv('test.csv')

rows = [row for row in df.iterrows()]


apps = {}

for line in rows[:10000]:
    line = str(line[1])
    user, app, time, launch, _, _ = line.split()[1::2]
    if '0' in launch:
        launch = 1
    
    if app not in apps:
        apps[app] = {}
        
    if user not in apps[app]:
        apps[app][user] = []
        apps[app][user].append([float(time), float(launch)])
        
    else:
        apps[app][user].append([float(time), float(launch)])



df2 = pd.read_csv('15313902.csv', error_bad_lines=False)
df2[:52]


appidarray = np.array(df2).T
x1 = appidarray[0,:]
x2 = appidarray[1,:]
appiddict = dict(zip(x1,x2))
appiddict


uuidarray = np.array(df2).T
x1 = uuidarray[0,:]
x2 = uuidarray[1,:]
uuiddict = dict(zip(x2,x1))
uuiddict

documents = []
for app in apps:
    documents.append(' '.join(apps[app].keys()))
print documents[800]


from gensim import corpora, models, similarities


## calculate number of clusters
nclust = 4

## Tokenize:
texts = [[word for word in document.lower().split()] for document in documents]

## build "user language" dictionary
dictionary = corpora.Dictionary(texts)

## make a sparse vectorization of the documents and store as the "corpus"
corpus = [dictionary.doc2bow(word) for word in texts]

### utilize term-frequency inverse-document-frequency since how long someone runs an app is important
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus] ## apply tfidf to corpus


## compute a latent dirichlet allocation (LDA) to design the X topics (X = nclust)
model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=nclust, passes=1)

## Try to make this more elegant... structure of model[] output is not great
clust = np.zeros((nclust,len(texts)))
for j in np.arange(len(corpus)):
    res = model[corpus[j]]
    for i,val in res:
        try: clust[i][j] = val
        except: pdb.set_trace()

## if you want to add those as columns on your dataframe:
#for i in np.arange(nclust): apps_df[('cluster%i'%(i+1))]= [c for c in clust[i]]



appclust = pd.DataFrame(clust[0], columns= ['c1'])
for i in np.arange(nclust):
    appclust[('c%i'%(i+1))]= [c for c in clust[i]]


fig = plt.figure(figsize=(12, 9))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=15, azim=45)

N=50
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2

#cmap = plt.cm.jet
#colors = cmap(0,0)

#plt.cla()

ax.scatter(appclust['c1'], appclust['c2'], appclust['c3'], s=area, color=colors, alpha=0.4)


fig = plt.figure(figsize=(8, 6))
plt.clf()
ax = fig.gca(projection = '3d')

#cmap = plt.cm.reds
#_colors = cmap(appclust)

ax.scatter(appclust['c1'], appclust['c2'], appclust['c3'], color='teal')



#how apps are related to all other apps
crossapp = np.dot(appclust,appclust.T)


#normalize
# appclust/=np.max(appclust)

# don't recommend apps they already have
crossapp[np.diag_indices(len(appclust))] = 0

#cache applist + crossapp for online ref
def giverec(applist, crossapp, apprec, numreturn):
    place = np.where(np.array(applist) == apprec)[0][0]
    
#creates rec list with probabilities of being recommended
    #print zip(crossapp[place], applist)
    #zip(crossapp[place], applist)
    prob_matrix = np.sort(np.array(zip(crossapp[place], applist), dtype=[('probability', 'float'), ('recommendation', 'object')]), order = 'probability')[-numreturn:]
    return prob_matrix

#runs giverec
#recs = giverec(apps.keys(), crossapp, apps.keys()[203], 3)
recs = giverec(apps.keys(), crossapp, uuiddict['cartier square'], 2)
#print recs

recs[0][1]
print recs

for rec in recs:
    print appiddict[rec[1]]


querylist = []

for jim in uuiddict:
    apprec2 = uuiddict[jim]
    place = np.where(np.array(apps.keys()) == apprec2)

    if len(place[0]) > 0:
        #if uuiddict[jim] in appiddict:
        recs = giverec(apps.keys(), crossapp, uuiddict[jim], 1)
        if recs[0][1] in appiddict:
            querylist.append(jim)
            print jim

len(querylist)

dd = dict(patek=["Twebble", 0.893, "SmartStatus Pro", 0.672], katy=["Pokemon", 0.841, "Fair Weather", 0.838], cartier=["Real Weather", 0.810, "xTime", 0.808], music=["C25K", 0.701,"Motiv8 Health", 0.623], dragon=["Undefeated", 0.811, "Superman", 0.613], homer=["Pokemon", 0.734, "Superman", 0.612], pannerai=["Nearby Specials", 0.604, "Battery Life", 0.524], pokemon=["Mastermind",0.762,"Two Player Tic Tac Toe", 0.721], seven=["C25K - Couch to 5K",0.88,"PebbGPS", 0.847 ], universe=["SmartWatch+", 0.833, "Evernote", 0.712], taller=["Morpheuz Sleep Monitor", 0.719, "Deck of Cards", 0.672], ballet=["Evernote", 0.781,"WatchShopper", 0.778], guardian=["Live Cricket", 0.842,"Deck of Cards", 0.621], medical=["Evernote", 0.867, "Four Square", 0.855], R2D2=["Pokemon", 0.883, "iUnlockYourMind", 0.79], Nightscout=["Evernote", 0.694, "PebbleCam", 0.616], transformers=["MiniDungeon", 0.761, ], steam=["MagicPebble", 0.634,"Pebbble Note", 0.611], fourSquare=["Evernote", 0.877, "ESPN", 0.873], couch=["7-Min Workout", 0.923, "Motiv8 Health", 0.897])
for key in dd:
    print key, ":", dd[key], ","


dd = [("patek", "Patek"), ("katy", "Katy Perry Hop"), ("cartier", "Cartier Square"), ("music", "Music for Pebble"), ("dragon", "DRAGON BALL-MOD"),("homer", "Homer Simpson v2"), ("pannerai", "PEBBLE PANERAI"), ("pokemon", "Pokémon Battle"), ("seven", "7-Minute Workout"),("universe", "Big Univers"), ("taller", "Taller"), ("ballet", "Arabesque"), ("guardian", "The Guardian for Pebble"), ("medical", "Medical Staff"), ("R2D2", "Artoo (R2D2)"), ("Nightscout", "Nightscout"), ("tranformers", "Transformers"), ("steam", "SteamPebble Mark II"), ("fourSquare", "Four Square"), ("couch", "C25K - Couch to 5K")   ]
for value, name in dd:
    print '<option value="%s">%s</option>' % (value, name)




