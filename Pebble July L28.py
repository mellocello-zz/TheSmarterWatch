import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as datetime

L282 = pd.read_csv('14890082.csv')

L282[0:5]

L282['newtime'] = [datetime.datetime.fromtimestamp(x).day for x in L282['time']]

L282['newtime'][100000]

len(L282)

type(L282['newtime'])


len(L282[L282['newtime']==1]['identity_0_user'].unique())

count=[len(L282[L282['identity_0_user'] == user]['newtime'].unique()) for user in L282['identity_0_user'].unique()]

len(L282[L282['identity_0_user'] == '5320f56ba2062929b40000af']['newtime'].unique())

len([L282['identity_0_user'] == '5320f56ba2062929b40000af'])

len(L282[L282['identity_0_user'] == '52fb64a75d7f927cd10006aa']['newtime'])

len(L282[L282['identity_0_user'] == '52fb64a75d7f927cd10006aa']['newtime'].unique())



total = len(L282['identity_0_user'].unique())
count = np.zeros(total)
n = 0
for user in L282['identity_0_user'].unique():
    count[n] = (len(L282[L282['identity_0_user'] == user]['newtime'][0:1].unique()))
    n=n+1



total = len(L282['identity_0_user'].unique())
count = np.zeros(total)
n = 0
for user in L282['identity_0_user'][0:10000].unique():
    count[n] = (len(L282[L282['identity_0_user'] == user]['newtime'].unique()))
    n=n+1
print count

countreal = count[0:8180]

usercount = np.bincount(countreal.astype(int))

len(count)

np.bincount(count.astype(int))

np.arange(0,31)

daycount = np.arange(0,31)

plt.bar(daycount[1:30], usercount[1:30], color = 'b', alpha = 0.5)
plt.ylabel('Users')
plt.xlabel('Days Active')
plt.show()

