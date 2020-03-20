class MP(Me):
Me=object
Mh=True
Mm=print
Mn=round
Mz=max
MT=range
MC=len
 def __init__(Mf):
  Mf.MN()
 def MN(Mf):
  Mf.trades={'win':0,'lose':0}
  Mf.quantity={'buy':0,'sell':0}
  Mf.points={'buy':0,'sell':0,'loss':0,'profit':0}
  Mf.history_order=[]
 def MO(Mf,MF):
  if MF['activated']==Mh:
   if MF['profit']<=0:
    Mf.trades['lose']+=1
    Mf.points['loss']+=MF['profit']
   elif MF['profit']>0:
    Mf.trades['win']+=1
    Mf.points['profit']+=MF['profit']
   if MF['order_type']=='BUY':
    Mf.quantity['sell']+=MF['quantity']
    Mf.points['sell']+=MF['quantity']*MF['end_price']
   elif MF['order_type']=='SELL':
    Mf.quantity['buy']+=MF['quantity']
    Mf.points['buy']+=MF['quantity']*MF['end_price']
  Mf.history_order.append(MF)
 def MB(Mf,MF):
  Mf.quantity[MF['order_type'].lower()]+=MF['quantity']
  Mf.points[MF['order_type'].lower()]+=MF['quantity']*MF['price']
 def MK(Mf):
  Mm('Total Trades: %d'%(Mf.trades['win']+Mf.trades['lose']))
  Mm('Win Trades : Lose Trades = %d : %d'%(Mf.trades['win'],Mf.trades['lose']))
  pf='--- (loss=0)' if Mf.points['loss']==0 else "%.2f"%(Mf.points['profit']/-Mf.points['loss'])
  Mm('Profit Factor: %s'%pf)
  Mm('Net Profit: %f'%(Mf.points['profit']+Mf.points['loss']))
  Mw=0.0
  MH=0.0
  MW=0.0
  for Mp in Mf.history_order:
   if Mp['activated']:
    MV=Mn(Mp['profit'],5)
    Mw+=MV
    if MV<0:
     Mx=MH-Mw
     MW=Mz(Mx,MW)
    else:
     MH=Mw if Mw>MH else MH
  Mm('Max Drawdown: %f%%'%((MW/Mw)*100))
  return{'total_trades':Mf.trades['win']+Mf.trades['lose'],'win_trades':Mf.trades['win'],'lose_trades':Mf.trades['lose'],'profit_factor':pf,'net_profit':Mf.points['profit']+Mf.points['loss'],'max_drawdown':MW}
 def MG(Mf):
  return Mf.points['profit']+Mf.points['loss']
 def Mb(Mf,look_back=0):
  pf=2.0
  if look_back==0:
   pf=pf if Mf.points['loss']==0 else Mf.points['profit']/-Mf.points['loss']
  else:
   MS=0.0
   MA=0.0
   for i in MT(MC(Mf.history_order)-1,-1,-1):
    if Mf.history_order[i]['activated']:
     ML=Mf.history_order[i]['profit']
     if ML<0:
      MA+=ML
     else:
      MS+=ML
    look_back-=1
    if look_back<=0:
     break
   pf=pf if MA==0 else MS/-MA
  return pf
 def MJ(Mf,amount=-1):
  if amount<=0 or amount>=MC(Mf.history_order):
   return Mf.history_order.copy()
  else:
   return Mf.history_order[MC(Mf.history_order)-amount:].copy()