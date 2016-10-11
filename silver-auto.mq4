//+------------------------------------------------------------------+
//| stock-v1.mq4 |
//| Copyright 2016, MetaQuotes Software Corp. |
//| https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, MetaQuotes Software Corp."
#property link "https://www.mql5.com"
#property version "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function |
//+------------------------------------------------------------------+
int OnInit()
  {
//---

//---
  return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---

  }

  int force_period = 13;

  int k_period = 5;
  int d_period = 3;
  int kdj_slowing = 3;

  int rsi_period = 5;

  int ema_period = 5;
//  int ema_period = 3;

  int global_tendency = 0;

//+------------------------------------------------------------------+
//| Calculate open positions |
//+------------------------------------------------------------------+
int CalculateCurrentOrders(string symbol)
  {
  int buys=0,sells=0;
//---
  for(int i=0;i<OrdersTotal();i++)
  {
  if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
  if(OrderSymbol()==symbol)
  {
  if(OrderType()==OP_BUY) buys++;
  if(OrderType()==OP_SELL) sells++;
  }
  }
//--- return orders volume
  if(buys>0) return(buys);
  else return(-sells);
  }

//+------------------------------------------------------------------+
//| Check for close order conditions |
//+------------------------------------------------------------------+
void CheckForClose()
  {
//--- go trading only for first tiks of new bar
  if(Volume[0]>1) return;
//---
  for(int i=0;i<OrdersTotal();i++)
  {
  if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
  if(OrderSymbol()!=Symbol()) continue;
  //--- check order type
  if(OrderType()==OP_BUY && OrderOpenPrice() < iClose(NULL, 0, 0))
  {
  if(!OrderClose(OrderTicket(),OrderLots(),Bid,3,White))
  Print("OrderClose error ",GetLastError());
  }
  if(OrderType()==OP_SELL)
  {
  if(!OrderClose(OrderTicket(),OrderLots(),Ask,3,White))
  Print("OrderClose error ",GetLastError());
  }
  }
//---
  }

//+------------------------------------------------------------------+
//| Expert tick function |
//+------------------------------------------------------------------+
void OnTick()
  {
  int res;

  double current_force, current_kdj, current_ema, current_rsi;
  double last_force, last_kdj, last_ema, last_rsi;
  double force_s, kdj_s, rsi_s, ema_s, close_s;
  double buy_s, sell_s;
//---
  if(Bars<100 || IsTradeAllowed()==false)
  {
  Print("bars less than 100");
  return;
  }

  // iForce()
  current_force = iForce(NULL, 0, force_period, MODE_SMA, PRICE_CLOSE, 0);
  last_force = iForce(NULL, 0, force_period, MODE_SMA, PRICE_CLOSE, 1);
  force_s = (current_force > last_force);

  // iStochastic()
  current_kdj = iStochastic(NULL, 0, k_period, d_period, kdj_slowing, MODE_SMA, 1, MODE_SIGNAL, 0);
  last_kdj = iStochastic(NULL, 0, k_period, d_period, kdj_slowing, MODE_SMA, 1, MODE_SIGNAL, 1);
  kdj_s = (current_kdj > last_kdj);

  // iRSI()
  current_rsi = iRSI(NULL, 0, rsi_period, PRICE_CLOSE, 0);
  last_rsi = iRSI(NULL, 0, rsi_period, PRICE_CLOSE, 1);
  rsi_s = (current_rsi > last_rsi);

  // iMA()
  current_ema = iMA(NULL, 0, ema_period, 0, MODE_EMA, PRICE_CLOSE, 0);
  last_ema = iMA(NULL, 0, ema_period, 0, MODE_EMA, PRICE_CLOSE, 1);
  ema_s = (current_ema > last_ema);

  close_s = (iClose(NULL, 0, 0) > iClose(NULL, 0, 1));

  buy_s = 0;
  sell_s = 0;

  if ((force_s + kdj_s + rsi_s) > 2) {
  buy_s = 1;
  global_tendency = 1;
  }else if (global_tendency > 0) {
  if (force_s > 0) {
  ;
  }
// else if (ema_s > 0 || close_s > 0)
  else if (close_s > 0) {
  ;
  }
  else {
  sell_s = 1;
  global_tendency = -1;
  }
  }

  if (buy_s)
  res = OrderSend(Symbol(),OP_BUY,0.01,Ask,3,0,0,"",0,0,Blue);
// if (sell_s)
// res = OrderSend(Symbol(),OP_SELL,0.01,Bid,3,0,0,"",0,0,Red);

  if (buy_s == 0 && global_tendency > 0) {
  CheckForClose(OP_SELL);
  if (close_s < 0 && buy_s == 0)
  res = OrderSend(Symbol(),OP_BUY,0.01,Ask,3,0,0,"",0,0,Blue);
  }
// else if (sell_s == 0 && global_tendency < 0) {
// CheckForClose(OP_BUY);
// if (close_s > 0 && sell_s == 0)
// res = OrderSend(Symbol(),OP_SELL,0.01,Bid,3,0,0,"",0,0,Red);
// }

  }
//+------------------------------------------------------------------+

