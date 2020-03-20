import matplotlib.pyplot as plt
UP=True
Uj=open
UL=round
Uz=len
UC=range
Ua=False
import pandas as pd
Us=pd.DataFrame
import pickle
Uf=pickle.load
import sys
UN=sys.argv
from tqdm import trange
UW=[]
UG=[]
x=[]
for i in Ui(1500+1,ascii=UP):
 with Uj(UN[1]+'/trades/episode_%04d.pkl'%i,'rb')as f:
  UJ=Uf(f)
 s=0
 p=[]
 n=0
 for d in UJ:
  if d['activated']:
   s+=UL(d['profit'],5)
   n+=1
  p.append(s)
 UG.append(s)
 a=s/n
 UW.append(a)
 x.append(i)
 if Uz(UN)>2:
  plt.plot(UC(Uz(p)),p)
  plt.show()
plt.plot(UC(Uz(UW)),UW)
plt.title("average rewards")
plt.show()
plt.plot(UC(Uz(UG)),UG)
plt.title("total rewards")
plt.show()
UM={'episode':x,'average_reward':UW,'total_reward':UG}
Us(UM).to_csv('train_reward-episode.csv',index=Ua)