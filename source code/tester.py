from lib.Market import Market
fR=range
fD=open
fy=dict
fm=len
fp=False
fv=print
from lib.Record import Record
from lib.OrderManager import OrderManager
from lib.Trader import SureFireTrader
from lib.Series2GAF import gaf_encode
from tensorforce.agents import Agent
fL=Agent.from_spec
from tensorforce.agents.constant_agent import ConstantAgent
from tqdm import tqdm,trange
import matplotlib.pyplot as plt
import pandas as pd
fC=pd.DataFrame
import numpy as np
fU=np.stack
import logging
fJ=logging.warning
fq=logging.info
import json
fV=json.load
import os,sys
fn=sys.argv
import pickle
plt.style.use('ggplot')
def fi():
 fj=fn[1].split('\\')
 fd=fj[-2]
 fW=fj[-1]
 fh=Market(data_path="data/%s_Candlestick_4_Hour_BID_01.12.2018-31.12.2018.csv"%fW)
 fs=Record()
 fr=OrderManager(market=fh,record=fs)
 fE=SureFireTrader(orderManager=fr)
 fI=[20,25,30]
 fx=['BUY','SELL']
 fB=[2,3,4]
 fY=12
 fP={'episode':[],'total_trades':[],'win_trades':[],'lose_trades':[],'profit_factor':[],'net_profit':[],'max_drawdown':[],'trading_rounds':[]}
 if fd!="constant":
  fA=fR(0,100+1,100)
 else:
  fA=fR(1)
 for fa in fA:
  if fd!="constant":
   with fD("config/%s.json"%fd,'r')as fp:
    fk=fV(fp=fp)
   with fD("config/conv2d.json",'r')as fp:
    fF=fV(fp=fp)
   fo=fL(spec=fk,kwargs=fy(states=fy(type='float',shape=(fY,fY,4)),actions=fy(SLTP_pips=fy(type='int',num_actions=fm(fI)),start_order_type=fy(type='int',num_actions=fm(fx)),max_level_limit=fy(type='int',num_actions=fm(fB))),network=fF))
   fo.restore_model(fn[1]+'/%04d'%fa)
  else:
   fo=ConstantAgent(states=fy(type='float',shape=(fY,fY,4)),actions=fy(SLTP_pips=fy(type='int',num_actions=fm(fI)),start_order_type=fy(type='int',num_actions=fm(fx)),max_level_limit=fy(type='int',num_actions=fm(fB))),action_values={'SLTP_pips':2,'max_level_limit':2,'start_order_type':0})
  fQ=[]
  fz=0
  fN=0
  fK=fp
  fg=12
  fs.reset()
  fr.reset()
  fh.reset(start_index=fY)
  while(fh.next()):
   fr.orders_check()
   fw,fl=fE.status_check()
   fT=fh.get_ohlc(size=fY)
   fc=fh.get_indicators(size=fY)
   O,H,L,C=gaf_encode(fT['Open']),gaf_encode(fT['High']), gaf_encode(fT['Low']),gaf_encode(fT['Close'])
   fG=fU((O,H,L,C),axis=-1)
   if fw=='TRADE_OVER':
    fX=fo.act(fG)
    fS=fI[fX['SLTP_pips']]*2
    ft=fI[fX['SLTP_pips']]
    fE.set_max_level(fB[fX['max_level_limit']])
    fb=fx[fX['start_order_type']]
    fE.new_trade(SL_pip=fS,TP_pip=ft,start_order_type=fb)
    fN+=1
    fz=0
    fq("NewTradeStarted: current net profit=%f (price@%f)"%(fs.get_net_profit(),fh.get_market_price()))
   elif fw=='ADD_ORDER':
    fO=fE.get_orders_detail()[-1]
    if fO['order_type']=='BUY':
     fH=fO['price']-fh.get_pip(ft)
    elif fO['order_type']=='SELL':
     fH=fO['price']+fh.get_pip(ft)
    fE.add_reverse_order(price=fH,SL_pip=fS,TP_pip=ft)
    fz=0
   elif fw=='ERROR':
    fJ("SureFireError: order issues...")
   elif fw=='NONE':
    fz+=1
    if fz>=fg:
     fX=fo.act(fG)
     fS=fI[fX['SLTP_pips']]*2
     ft=fI[fX['SLTP_pips']]
     fE.set_max_level(fB[fX['max_level_limit']])
     fb=fx[fX['start_order_type']]
     fE.new_trade(SL_pip=fS,TP_pip=ft,start_order_type=fb)
     fz=0
     fq("NewTradeStarted: current net profit=%f (price@%f)"%(fs.get_net_profit(),fh.get_market_price()))
   fQ.append(fs.get_net_profit())
  fe=fs.show_details()
  fv("Rounds of Tradings: %d\n"%fN)
  fv('---')
  fP['episode'].append(fa)
  fP['trading_rounds'].append(fN)
  for k in fe:
   fP[k].append(fe[k])
 '''
    for k in output_record:
        plt.plot(output_record['episode'], output_record[k])
        plt.title(k)
        plt.show()
    '''
 fC(fP).to_csv('test_detail-episode.csv',index=fp)
if __name__=="__main__":
 fi()