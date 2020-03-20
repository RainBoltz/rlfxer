import logging
ib=object
iW=None
im=len
ip=False
iQ=True
iU=range
iM=sorted
iJ=logging.info
iz=logging.warning
class iK(ib):
 def __init__(iB,ih,iG):
  iB.market=ih
  iB.record=iG
  iB.orders=[]
  iB.SerialNumber=0
 def io(iB,new_record=iW):
  if new_record!=iW:
   iB.record=new_record
  iB.iY()
  iB.SerialNumber=0
 def iY(iB):
  if im(iB.orders)>0:
   for il in iB.orders:
    iB.it(il)
  iB.orders=[]
 def iy(iB,quantity,price=0,order_type='BUY',SL_pip=0,TP_pip=0,price_diff=0):
  if price==0:
   price=iB.market.get_market_price()+iB.market.get_pip()*price_diff
  if order_type=='BUY':
   SL=-1e9 if SL_pip==0 else-SL_pip*iB.market.get_pip()+price
   TP=1e9 if TP_pip==0 else price+TP_pip*iB.market.get_pip()
  elif order_type=='SELL':
   SL=1e9 if SL_pip==0 else price+SL_pip*iB.market.get_pip()
   TP=-1e9 if TP_pip==0 else-TP_pip*iB.market.get_pip()+price
  iO={'SN':iB.SerialNumber,'order_type':order_type,'quantity':quantity,'price':price,'SL':SL,'TP':TP,'activated':ip,'create_time':iB.market.get_datetime()}
  iB.SerialNumber+=1
  iB.iv(iO)
  return iO['SN']
 def iv(iB,iO):
  if iB.ig(iO)and iB.iL(iO)and iB.ij(iO)and iB.iS(iO):
   iB.orders.append(iO)
 def ig(iB,iO):
  for il in iB.orders:
   if il['SN']==iO['SN']:
    return ip
  return iQ
 def iL(iB,iO):
  if iO['price']<=0:
   iz('OrderUnvalid: price must be greater than zero')
   return ip
  else:
   return iQ
 def ij(iB,iO):
  if iO['order_type']=='BUY':
   if iO['SL']>=iO['price']-iB.market.get_pip(2):
    iz('OrderUnvalid: stop loss must be 2 pips less than buy price')
    return ip
  elif iO['order_type']=='SELL':
   if iO['SL']<=iO['price']+iB.market.get_pip(2):
    iz('OrderUnvalid: stop loss must be 2 pips greater than buy price')
    return ip
  return iQ
 def iS(iB,iO):
  if iO['order_type']=='BUY':
   if iO['TP']<=iO['price']+iB.market.get_pip(2):
    iz('OrderUnvalid: take profit must be 2 pips greater than buy price')
    return ip
  elif iO['order_type']=='SELL':
   if iO['TP']>=iO['price']-iB.market.get_pip(2):
    iz('OrderUnvalid: take profit must be 2 pips less than buy price')
    return ip
  return iQ
 def iD(iB):
  ic=[]
  for i in iU(im(iB.orders)):
   iO=iB.orders[i]
   if iB.market.activate_check(iO):
    iB.orders[i]['activate_time']=iB.market.get_datetime()
    iB.orders[i]['activated']=iQ
    iB.record.order_activated(iB.orders[i])
    iJ('OrderActivated#%04d: %s@%f (TP=%f,SL=%f)'%(iB.orders[i]['SN'],iB.orders[i]['order_type'],iB.orders[i]['price'],iB.orders[i]['TP'],iB.orders[i]['SL']))
   iq=iB.market.SLTP_check(iO)
   if iq=='TP' or iq=='SL':
    iB.it(iO,iq)
    ic.append(i)
  if im(ic)>0:
   for i in iM(ic,reverse=iQ):
    iB.orders.pop(i)
 def it(iB,iO,status='X'):
  if status=='TP':
   iO['end_price']=iO['TP']
   if iO['order_type']=='BUY':
    iO['profit']=(iO['TP']-iO['price'])*iO['quantity']
    iJ('OrderTakeProfit#%04d: win %f'%(iO['SN'],iO['profit']))
   elif iO['order_type']=='SELL':
    iO['profit']=(iO['price']-iO['TP'])*iO['quantity']
    iJ('OrderTakeProfit#%04d: win %f'%(iO['SN'],iO['profit']))
  elif status=='SL':
   iO['end_price']=iO['SL']
   if iO['order_type']=='BUY':
    iO['profit']=(iO['SL']-iO['price'])*iO['quantity']
    iJ('OrderStopLoss#%04d: lose %f'%(iO['SN'],iO['profit']))
   elif iO['order_type']=='SELL':
    iO['profit']=(iO['price']-iO['SL'])*iO['quantity']
    iJ('OrderStopLoss#%04d: lose %f'%(iO['SN'],iO['profit']))
  elif status=='X':
   if iO['activated']==iQ:
    iO['end_time']=iB.market.get_datetime()
    iO['end_price']=iB.market.get_market_price()
    if iO['order_type']=='BUY':
     iO['profit']=(iO['end_price']-iO['price'])*iO['quantity']
     iJ('OrderClosed#%04d: (%f-%f)*%d=%f'%(iO['SN'],iO['end_price'],iO['price'],iO['quantity'],iO['profit']))
    elif iO['order_type']=='SELL':
     iO['profit']=(iO['price']-iO['end_price'])*iO['quantity']
     iJ('OrderClosed#%04d: (%f-%f)*%d=%f'%(iO['SN'],iO['price'],iO['end_price'],iO['quantity'],iO['profit']))
   else:
    iJ('OrderCancelled#%04d: %s@%f'%(iO['SN'],iO['order_type'],iO['price']))
  iO['end_time']=iB.market.get_datetime()
  iB.record.to_history(iO)
 def iN(iB,SN):
  for i in iU(im(iB.orders)):
   if iB.orders[i]['SN']==SN:
    if iB.orders[i]['activated']==iQ:
     iB.orders[i]['end_time']=iB.market.get_datetime()
     iB.orders[i]['end_price']=iB.market.get_market_price()
     if iB.orders[i]['order_type']=='BUY':
      iB.orders[i]['profit']=(iB.orders[i]['end_price']-iB.orders[i]['price'])*iB.orders[i]['quantity']
      iJ('OrderClosed#%04d: %f-%f=%f'%(iB.orders[i]['SN'],iB.orders[i]['end_price'],iB.orders[i]['price'],iB.orders[i]['profit']))
     elif iB.orders[i]['order_type']=='SELL':
      iB.orders[i]['profit']=(iB.orders[i]['price']-iB.orders[i]['end_price'])*iB.orders[i]['quantity']
      iJ('OrderClosed#%04d: %f-%f=%f'%(iB.orders[i]['SN'],iB.orders[i]['price'],iB.orders[i]['end_price'],iB.orders[i]['profit']))
    iB.record.to_history(iB.orders[i])
    iB.orders.pop(i)
    break
 def iw(iB):
  return[il['SN']for il in iB.orders]
 def iC(iB,SN):
  for i in iU(im(iB.orders)):
   if iB.orders[i]['SN']==SN:
    return iB.orders[i]
 def iT(iB,amount=1):
  return iB.record.get_history(amount=amount)