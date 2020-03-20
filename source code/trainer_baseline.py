from lib.Market import Market
Og=dict
OQ=len
OY=False
OU=True
OV=open
from lib.Record import Record
from lib.OrderManager import OrderManager
from lib.Trader import SureFireTrader
from lib.Series2GAF import gaf_encode
from tensorforce.agents.constant_agent import ConstantAgent
from tqdm import tqdm,trange
import matplotlib.pyplot as plt
import numpy as np
Ow=np.abs
On=np.stack
import logging
Ox=logging.warning
Ot=logging.info
import json
import os
Op=os.makedirs
Ol=os.path
import pickle
ON=pickle.dump
plt.style.use('ggplot')
Om='EURUSD'
def OF():
 OI=Market(data_path="data/%s_Candlestick_4_Hour_BID_01.08.2018-30.11.2018.csv"%Om)
 Oa=Record()
 Oo=OrderManager(market=OI,record=Oa)
 OS=SureFireTrader(orderManager=Oo)
 OP=[20,25,30]
 OH=['BUY','SELL']
 Oy=[2,3,4]
 Oc=12
 OR=ConstantAgent(states=Og(type='float',shape=(Oc,Oc,4)),actions=Og(SLTP_pips=Og(type='int',num_actions=OQ(OP)),start_order_type=Og(type='int',num_actions=OQ(OH)),max_level_limit=Og(type='int',num_actions=OQ(Oy))),action_values={'SLTP_pips':0,'max_level_limit':0,'start_order_type':0})
 if not Ol.exists("save_model/constant/trades"):
  Op("save_model/constant/trades")
 if not Ol.exists('save_model/constant/0000'):
  Op('save_model/constant/0000')
 OR.save_model('save_model/constant/0000/model')
 OM=[]
 OW=[]
 OL=[]
 Os=0
 OX=0
 OB=OY
 OK=12
 Oa.reset()
 Oo.reset()
 OI.reset(start_index=Oc)
 OD=tqdm()
 while(OI.next()):
  OD.update(1)
  Oo.orders_check()
  OJ,Oz=OS.status_check()
  Oj=OI.get_ohlc(size=Oc)
  Ok=OI.get_indicators(size=Oc)
  O,H,L,C=gaf_encode(Oj['Open']),gaf_encode(Oj['High']), gaf_encode(Oj['Low']),gaf_encode(Oj['Close'])
  Or=On((O,H,L,C),axis=-1)
  if OJ=='TRADE_OVER':
   if OI.get_current_index()>Oc:
    Of=(Oa.get_net_profit()-OW[-1])/OI.get_pip()
    Ov=1.0-0.1*OQ(Oz)
    if Of>0:
     Ou=Of*Ov
    else:
     if OQ(Oz)==0:
      Ou=0
     else:
      Ou=-Ow(Oz[0]['TP']-Oz[0]['price'])/OI.get_pip()
    if OI.get_current_index()>=OI.get_data_length()-OK*Oy[-1]:
     OB=OU
    OR.observe(reward=Ou,terminal=OB)
    OL.append(Ou)
    if OB==OU:
     OD.close()
     OM.append(OL)
     break
   OT=OR.act(Or)
   OE=OP[OT['SLTP_pips']]*2
   OG=OP[OT['SLTP_pips']]
   OS.set_max_level(Oy[OT['max_level_limit']])
   Oq=OH[OT['start_order_type']]
   OS.new_trade(SL_pip=OE,TP_pip=OG,start_order_type=Oq)
   OX+=1
   Os=0
   Ot("NewTradeStarted: current net profit=%f (price@%f)"%(Oa.get_net_profit(),OI.get_market_price()))
  elif OJ=='ADD_ORDER':
   OA=OS.get_orders_detail()[-1]
   if OA['order_type']=='BUY':
    Oi=OA['price']-OI.get_pip(OG)
   elif OA['order_type']=='SELL':
    Oi=OA['price']+OI.get_pip(OG)
   OS.add_reverse_order(price=Oi,SL_pip=OE,TP_pip=OG)
   Os=0
  elif OJ=='ERROR':
   Ox("SureFireError: order issues...")
  elif OJ=='NONE':
   Os+=1
   if Os>=OK:
    Of=(Oa.get_net_profit()-OW[-1])/OI.get_pip()
    Ov=1.0-0.1*OQ(Oz)
    if Of>0:
     Ou=Of*Ov
    else:
     if OQ(Oz)==0:
      Ou=0
     else:
      Ou=-Ow(Oz[0]['TP']-Oz[0]['price'])/OI.get_pip()
    if OI.get_current_index()>=OI.get_data_length()-OK*Oy[-1]:
     OB=OU
    OR.observe(reward=Ou,terminal=OB)
    OL.append(Ou)
    if OB==OU:
     OD.close()
     OM.append(OL)
     break
    OT=OR.act(Or)
    OE=OP[OT['SLTP_pips']]*2
    OG=OP[OT['SLTP_pips']]
    OS.set_max_level(Oy[OT['max_level_limit']])
    Oq=OH[OT['start_order_type']]
    OS.new_trade(SL_pip=OE,TP_pip=OG,start_order_type=Oq)
    Os=0
    Ot("NewTradeStarted: current net profit=%f (price@%f)"%(Oa.get_net_profit(),OI.get_market_price()))
  OW.append(Oa.get_net_profit())
 with OV('save_model/constant/trades/episode_0000.pkl','wb')as f:
  ON(Oa.get_history(),f,protocol=-1)
 with OV('save_model/constant/trades/profit_history.pkl','wb')as f:
  ON(OW,f,protocol=-1)
 with OV('save_model/constant/trades/reward_history.pkl','wb')as f:
  ON(OM,f,protocol=-1)
 Oa.show_details()
if __name__=="__main__":
 OF()