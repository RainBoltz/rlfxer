class CO(CF):
CF=object
Cs=len
CG=super
Ck=int
Ci=range
CT=sorted
CX=True
 def __init__(CP,Ca):
  CP.orderManager=Ca
 def Cm(CP,quantity=1,price=0,order_type='BUY',SL_pip=0,TP_pip=0,price_diff=0):
  SN=CP.orderManager.create_order(quantity=quantity,price=price,order_type=order_type,SL_pip=SL_pip,TP_pip=TP_pip,price_diff=price_diff)
  return SN
 def Ce(CP):
  if Cs(CP.orderManager.get_orders_SN())>0:
   CP.orderManager.clear_orders()
 def CW(CP):
  Cy=[]
  for sn in CP.orderManager.get_orders_SN():
   CV=CP.orderManager.get_order_detail(sn)
   Cy.append(CV)
  return Cy
class Cv(CO):
 def __init__(CP,Ca):
  CG().__init__(Ca)
  CP.quantity_level=[1,3,6,12,24,48,96]
  CP.max_level=7
  CP.current_level=0
 def CS(CP,SL_pip,TP_pip,start_order_type):
  CP.Ce()
  CP.current_level=0
  CP.Cm(quantity=CP.quantity_level[0],order_type=start_order_type,SL_pip=SL_pip,TP_pip=TP_pip)
  CP.CD(price_diff=Ck(SL_pip/2),SL_pip=SL_pip,TP_pip=TP_pip)
 def Co(CP):
  Cd='NONE'
  CR=[]
  Cp=CP.orderManager.get_orders_SN()
  if Cs(Cp)==0:
   Cd='TRADE_OVER'
   CR=CP.orderManager.get_history_order(amount=6)
   if Cs(CR)>0:
    CN=[]
    for i in Ci(Cs(CR)):
     if not CR[i]['activated']:
      CN.append(i)
    for i in CT(CN,reverse=CX):
     CR.pop(i)
    for i in Ci(Cs(CR)-1,-1,-1):
     if CR[i]['quantity']==1:
      CR=CR[i:]
      break
  elif Cs(Cp)==1:
   CB=Cp[0]
   CV=CP.orderManager.get_order_detail(CB)
   if not CV['activated']:
    Cd='TRADE_OVER'
    CR=CP.orderManager.get_history_order(amount=6)
    CN=[]
    for i in Ci(Cs(CR)):
     if not CR[i]['activated']:
      CN.append(i)
    for i in CT(CN,reverse=CX):
     CR.pop(i)
    for i in Ci(Cs(CR)-1,-1,-1):
     if CR[i]['quantity']==1:
      CR=CR[i:]
      break
   else:
    Cd='TRADE_OVER'
    CR=CP.orderManager.get_history_order(amount=6)
    CN=[]
    for i in Ci(Cs(CR)):
     if not CR[i]['activated']:
      CN.append(i)
    for i in CT(CN,reverse=CX):
     CR.pop(i)
    for i in Ci(Cs(CR)-1,-1,-1):
     if CR[i]['quantity']==1:
      CR=CR[i:]
      break
  else:
   CB=Cp[-1]
   CV=CP.orderManager.get_order_detail(CB)
   if CV['activated']==CX and CP.current_level<=CP.max_level:
    Cd='ADD_ORDER'
  return Cd,CR
 def CD(CP,SL_pip,TP_pip,price=0,price_diff=0):
  CL=CP.orderManager.get_orders_SN()
  if Cs(CL)==0:
   return
  elif CP.orderManager.get_order_detail(CL[-1])['order_type']=='BUY':
   CJ='SELL'
   price_diff=-price_diff
  else:
   CJ='BUY'
  CP.current_level+=1
  CP.Cm(quantity=CP.quantity_level[CP.current_level],order_type=CJ,price=price,SL_pip=SL_pip,TP_pip=TP_pip,price_diff=price_diff)
 def Cn(CP,Cj):
  CP.max_level=Cj