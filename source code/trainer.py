from lib.Market import Market
tX=open
tv=dict
tR=len
tH=True
tI=False
from lib.Record import Record
from lib.OrderManager import OrderManager
from lib.Trader import SureFireTrader
from lib.Series2GAF import gaf_encode
from tensorforce.agents import Agent
Qo=Agent.from_spec
from tqdm import tqdm,trange
import matplotlib.pyplot as plt
import numpy as np
QM=np.abs
Qs=np.stack
import logging
Qp=logging.warning
Qb=logging.info
import json
QC=json.load
import os
Qx=os.makedirs
QS=os.path
import pickle
tQ=pickle.dump
plt.style.use('ggplot')
Qt='dqn'
QX='EURUSD'
def Ql():
 Qv=Market(data_path="data/%s_Candlestick_4_Hour_BID_01.08.2018-30.11.2018.csv"%QX)
 QR=Record()
 QH=OrderManager(market=Qv,record=QR)
 QI=SureFireTrader(orderManager=QH)
 Qd=[30,35,40,45,50]
 QP=['BUY','SELL']
 Qw=[1,2,3,4,5,6,7]
 QN=24
 with tX("config/%s.json"%Qt,'r')as fp:
  QD=QC(fp=fp)
 with tX("config/conv2d.json",'r')as fp:
  Qc=QC(fp=fp)
 QF=Qo(spec=QD,kwargs=tv(states=tv(type='float',shape=(QN,QN,4)),actions=tv(SLTP_pips=tv(type='int',num_actions=tR(Qd)),start_order_type=tv(type='int',num_actions=tR(QP)),max_level_limit=tv(type='int',num_actions=tR(Qw))),network=Qc))
 if not QS.exists("save_model/%s/trades"%Qt):
  Qx("save_model/%s/trades"%Qt)
 QY=[]
 for Qi in Qz(100+1,ascii=tH):
  Qq=[]
  Qm=[]
  QA=0
  QV=0
  QB=tI
  QK=12
  QR.reset()
  QH.reset()
  Qv.reset(start_index=QN)
  Qj=tqdm()
  while(Qv.next()):
   Qj.update(1)
   QH.orders_check()
   Qu,QE=QI.status_check()
   QO=Qv.get_ohlc(size=QN)
   Qf=Qv.get_indicators(size=QN)
   O,H,L,C=gaf_encode(QO['Open']),gaf_encode(QO['High']), gaf_encode(QO['Low']),gaf_encode(QO['Close'])
   Qh=Qs((O,H,L,C),axis=-1)
   if Qu=='TRADE_OVER':
    if Qv.get_current_index()>QN:
     QJ=(QR.get_net_profit()-Qq[-1])/Qv.get_pip()
     Qr=1.0-0.1*tR(QE)
     if QJ>0:
      Qa=QJ*Qr
     else:
      if tR(QE)==0:
       Qa=0
      else:
       Qa=-QM(QE[0]['TP']-QE[0]['price'])/Qv.get_pip()
     if Qv.get_current_index()>=Qv.get_data_length()-QK*Qw[-1]:
      QB=tH
     QF.observe(reward=Qa,terminal=QB)
     Qm.append(Qa)
     if QB==tH:
      if Qi%100==0:
       QT='save_model/%s/%04d'%(Qt,Qi)
       if not QS.exists(QT):
        Qx(QT)
       QF.save_model(QT+'/model')
      Qj.close()
      QY.append(Qm)
      with tX('save_model/%s/trades/episode_%04d.pkl'%(Qt,Qi),'wb')as f:
       tQ(QR.get_history(),f,protocol=-1)
      break
    QG=QF.act(Qh)
    Qe=Qd[QG['SLTP_pips']]*2
    Qy=Qd[QG['SLTP_pips']]
    QI.set_max_level(Qw[QG['max_level_limit']])
    Qk=QP[QG['start_order_type']]
    QI.new_trade(SL_pip=Qe,TP_pip=Qy,start_order_type=Qk)
    QV+=1
    QA=0
    Qb("NewTradeStarted: current net profit=%f (price@%f)"%(QR.get_net_profit(),Qv.get_market_price()))
   elif Qu=='ADD_ORDER':
    QW=QI.get_orders_detail()[-1]
    if QW['order_type']=='BUY':
     Qn=QW['price']-Qv.get_pip(Qy)
    elif QW['order_type']=='SELL':
     Qn=QW['price']+Qv.get_pip(Qy)
    QI.add_reverse_order(price=Qn,SL_pip=Qe,TP_pip=Qy)
    QA=0
   elif Qu=='ERROR':
    Qp("SureFireError: order issues...")
   elif Qu=='NONE':
    QA+=1
    if QA>=QK:
     QJ=(QR.get_net_profit()-Qq[-1])/Qv.get_pip()
     Qr=1.0-0.1*tR(QE)
     if QJ>0:
      Qa=QJ*Qr
     else:
      if tR(QE)==0:
       Qa=0
      else:
       Qa=-QM(QE[0]['TP']-QE[0]['price'])/Qv.get_pip()
     if Qv.get_current_index()>=Qv.get_data_length()-QK*Qw[-1]:
      QB=tH
     QF.observe(reward=Qa,terminal=QB)
     Qm.append(Qa)
     if QB==tH:
      if Qi%100==0:
       QT='save_model/%s/%04d'%(Qt,Qi)
       if not QS.exists(QT):
        Qx(QT)
       QF.save_model(QT+'/model')
      Qj.close()
      QY.append(Qm)
      with tX('save_model/%s/trades/episode_%04d.pkl'%(Qt,Qi),'wb')as f:
       tQ(QR.get_history(),f,protocol=-1)
      break
     QG=QF.act(Qh)
     Qe=Qd[QG['SLTP_pips']]*2
     Qy=Qd[QG['SLTP_pips']]
     QI.set_max_level(Qw[QG['max_level_limit']])
     Qk=QP[QG['start_order_type']]
     QI.new_trade(SL_pip=Qe,TP_pip=Qy,start_order_type=Qk)
     QA=0
     Qb("NewTradeStarted: current net profit=%f (price@%f)"%(QR.get_net_profit(),Qv.get_market_price()))
   Qq.append(QR.get_net_profit())
 with tX('save_model/%s/trades/reward_history.pkl'%Qt,'wb')as f:
  tQ(QY,f,protocol=-1)
if __name__=="__main__":
 Ql()