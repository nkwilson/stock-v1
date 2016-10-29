// ; -*- mode: c; tab-width: 4; -*-
// Time-stamp: <2016-10-29 22:59:54 nkyubin>
//+------------------------------------------------------------------+
//| stock-v1.mq4 |
//| Copyright 2016, MetaQuotes Software Corp. |
//| https://www.mql5.com |
//+------------------------------------------------------------------+

#property copyright "Copyright 2016, MetaQuotes Software Corp."
#property link "https://www.mql5.com"
#property version "1.48"
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

int force_period=13;

int k_period = 5;
int d_period = 3;
int kdj_slowing=3;

int rsi_period=5;

int ema_period=7;
//  int ema_period = 3;

int macd_fast=12;
int macd_slow=26;
int macd_signal=9;

int bands_period=20;
int bands_devia=2;
int bands_shift=0;

int global_tendency=0;

int order_margin = 50;

double viabality_percent = 0.01;  // 1% 

double profit_rate = 2.0;

int total_orders = 2;

int prev_orders = 0;
double next_lots = 0.01;
double max_lots = 0.64;
double next_min_lots=0.01;
double balance1, balance2;
int increase_lots_on_loss = 1;

double budget;

int no_stoploss = 0;


//+------------------------------------------------------------------+
//| Calculate open positions |
//+------------------------------------------------------------------+
int CalculateCurrentOrders(string symbol,int ordertype)
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
  //if(buys>0) return(buys);
  //else return(-sells);
  if(ordertype == OP_BUY) return buys;
  else return (-sells);
}
//+------------------------------------------------------------------+
//| Check for close order conditions |
//+------------------------------------------------------------------+
void CheckForClose(int ordertype,int force)
{
  //---
  for(int i=0;i<OrdersTotal();i++)
    {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
      if(OrderSymbol()!=Symbol()) continue;

      //--- check order type
      if(ordertype==OP_BUY && OrderType()==ordertype && (force || OrderOpenPrice()<Bid))
        {
	  printf("ticket %d buy open %f %sclose at %f",
		 OrderTicket(), OrderOpenPrice(), force ? "forced " : "" , Bid);

	  if(!OrderClose(OrderTicket(),OrderLots(),Bid,30,White))
            Print("OrderClose error ",GetLastError());
        }
      else if(ordertype==OP_SELL && OrderType()==ordertype && (force || OrderOpenPrice()>Ask))
        {
	  printf("ticket %d sell open %f %sclose at %f",
		 OrderTicket(), OrderOpenPrice(), force ? "forced " : "" , Ask);

	  if(!OrderClose(OrderTicket(),OrderLots(),Ask,30,White))
            Print("OrderClose error ",GetLastError());
        }
    }
  //---
}

//+------------------------------------------------------------------+
//| Close all orders |
//+------------------------------------------------------------------+
void CloseAll(int ordertype)
{
  int res;
  for (int i=0;i<OrdersTotal();i++) {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
      if(OrderSymbol()!=Symbol()) continue;

      //--- check order type
      if(OrderType()==OP_BUY && ordertype==OP_BUY)
		res=OrderClose(OrderTicket(), OrderLots(),Bid,30,White);
	  else if (OrderType()==OP_SELL && ordertype==OP_SELL)
		res=OrderClose(OrderTicket(), OrderLots(),Ask,30,White);
  }
}
  
//+------------------------------------------------------------------+
//| Send opposite orders to stop loss |
//+------------------------------------------------------------------+
void CheckForCloseWithProfit(int ordertype)
{
  double buy_profit, sell_profit;
  double buys, sells;
  
  buy_profit = sell_profit = 0;
  buys=sells=0;
  
  for (int i=0;i<OrdersTotal();i++) {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
      if(OrderSymbol()!=Symbol()) continue;

      //--- check order type
      if(OrderType()==OP_BUY) {
		buy_profit += OrderProfit();
		buys += OrderLots();
	  } else if (OrderType()==OP_SELL) {
		sell_profit += OrderProfit();
		sells += OrderLots();
	  }

	  if (buy_profit + sell_profit > 0.0) {
		CloseAll(OP_BUY);
		CloseAll(OP_SELL);
	  } else {
		CloseAll(ordertype);
	  }
  }
}

//+------------------------------------------------------------------+
//| Adjust loss and profit for all orders |
//+------------------------------------------------------------------+
void AdjustOrder(int ordertype)
{
  //--- go trading only for first tiks of new bar
  if(Volume[0]>1) return;
  //---
  double stoplevel= MarketInfo(Symbol(),MODE_STOPLEVEL);
  
  for(int i=0;i<OrdersTotal();i++)
    {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
      if(OrderSymbol()!=Symbol()) continue;
      //--- check order type
      if(ordertype==OP_BUY && OrderType()==ordertype)
        {
		  double base_stoploss = NormalizeDouble(Bid-stoplevel * Point,Digits);
	  double stoploss = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1) - stoplevel * Point;
	  // double bands = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1);
	  // double ema = iMA(NULL,0,ema_period,0,MODE_EMA,PRICE_CLOSE,1);
	  //	  double takeprofit = NormalizeDouble(Ask + 2 * stoplevel * Point,Digits);
	  double takeprofit = NormalizeDouble(Ask + profit_rate * stoplevel * Point,Digits);

	  printf("ticket %d buy open %f should adjust to loss %f (base %f) profit %f",
			 OrderTicket(), OrderOpenPrice(), stoploss, base_stoploss, takeprofit);

	  // adjust stop loss to open price     
	  //	  if ((OrderOpenPrice() + order_margin * Point) < iClose(NULL, 0, 0))
	  //  stoploss = OrderOpenPrice();

	  if (OrderTakeProfit() != 0.0)
		stoploss = base_stoploss;
	  else
		takeprofit = 0;
	  
	  if(OrderStopLoss() < stoploss && stoploss <= base_stoploss && !OrderModify(OrderTicket(),OrderOpenPrice(),stoploss, takeprofit, 0, Blue))
//	  if(!OrderModify(OrderTicket(),OrderOpenPrice(),stoploss, 0, 0, Blue))
	    Print("OrderModify error ",GetLastError());
        }
      else if(ordertype==OP_SELL && OrderType()==ordertype)
        {
		  double base_stoploss = NormalizeDouble(Ask+stoplevel * Point,Digits);
	  double stoploss = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1) + stoplevel * Point;
	  // double bands = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1);
	  //	  double ema = iMA(NULL,0,ema_period,0,MODE_EMA,PRICE_CLOSE,1);

	  //	  double takeprofit = NormalizeDouble(Bid - 2 * stoplevel * Point,Digits);
	  double takeprofit = NormalizeDouble(Bid - profit_rate * stoplevel * Point,Digits);

	  printf("ticket %d sell open %f should adjust to loss %f (base %f) profit %f",
			 OrderTicket(), OrderOpenPrice(), stoploss, base_stoploss, takeprofit);
	  
	  //if ((OrderOpenPrice() - order_margin * Point()) > iClose(NULL, 0, 0))
	  //  stoploss = OrderOpenPrice();

	  if (OrderTakeProfit() != 0.0)
		stoploss = base_stoploss;
	  else
		takeprofit = 0;
	  
	  if(OrderStopLoss() > stoploss && stoploss >= base_stoploss && !OrderModify(OrderTicket(),OrderOpenPrice(),stoploss, takeprofit, 0, Red))
//	  if(!OrderModify(OrderTicket(),OrderOpenPrice(),stoploss, 0, 0, Red))
	    Print("OrderModify error ",GetLastError());
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

  double current_force,current_kdj,current_ema,current_rsi, current_macd, current_bands;
  double last_force,last_kdj,last_ema,last_rsi, last_macd, last_bands;
  double force_s,kdj_s,rsi_s,ema_s,close_s, macd_s, bands_s;
  int buy_s,sell_s;
  int new_global_tendency;
  int below_bands_up = 0; // only open buy when blow bands up 
  double stoplevel= MarketInfo(Symbol(),MODE_STOPLEVEL);
  int aggressive_lots = 0;
  
  printf("Bars %d %f %f %f", Bars, budget, AccountBalance(), AccountProfit());
  
  //---
  if(Bars<13 || IsTradeAllowed()==false)
    {
      Print("bars less than 100");
      return;
    }

  // iForce()
  current_force=iForce(NULL,0,force_period,MODE_SMA,PRICE_CLOSE,1);
  last_force=iForce(NULL,0,force_period,MODE_SMA,PRICE_CLOSE,2);
  force_s = current_force - last_force;

  // iStochastic()
  current_kdj=iStochastic(NULL,0,k_period,d_period,kdj_slowing,MODE_SMA,1,MODE_MAIN,1);
  last_kdj=iStochastic(NULL,0,k_period,d_period,kdj_slowing,MODE_SMA,1,MODE_MAIN,2);
  kdj_s= current_kdj-last_kdj;

  // iRSI()
  current_rsi=iRSI(NULL,0,rsi_period,PRICE_CLOSE,1);
  last_rsi=iRSI(NULL,0,rsi_period,PRICE_CLOSE,2);
  rsi_s= current_rsi-last_rsi;

  // iMA()
  current_ema=iMA(NULL,0,ema_period,0,MODE_EMA,PRICE_CLOSE,1);
  last_ema=iMA(NULL,0,ema_period,0,MODE_EMA,PRICE_CLOSE,2);
  ema_s=current_ema-last_ema;

  // iMACD()
  current_macd=iMACD(NULL, 0, macd_fast, macd_slow, macd_signal, PRICE_CLOSE, MODE_SIGNAL, 1);
  last_macd=iMACD(NULL, 0, macd_fast, macd_slow, macd_signal, PRICE_CLOSE, MODE_SIGNAL, 2);
  macd_s=current_macd-last_macd;

  // iBand()
  current_bands = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1);
  last_bands = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 2);
  bands_s = current_bands-last_bands;
  
  close_s=iClose(NULL,0,1)-iClose(NULL,0,2);

  buy_s=0;
  sell_s=0;

  // save balance if orders is zero
  if (OrdersTotal() == 0 && balance1 == 0) {
	balance1 = AccountBalance();
	balance2 = balance1;

	budget = balance1;
  }
  
  // orders changed, check balance
  if (OrdersTotal() == 0) {
	if (balance2 != AccountBalance()) {
	  balance2 = AccountBalance();

	  if (increase_lots_on_loss) {
		if (balance1 >= balance2)
		  next_lots += next_min_lots;
		else if (next_lots > next_min_lots)
		  next_lots -= 2 * next_min_lots;

		if (next_lots < next_min_lots)
		  next_lots = next_min_lots;
	  } else
		next_lots = next_min_lots;
	  
	  balance1 = balance2;

	  // positive profit
	  if (budget < balance1) {
		next_lots = next_min_lots;

		budget = balance1;
	  }
	}
  }
  
  new_global_tendency = 0; 
  if(force_s > 0 && kdj_s > 0 && rsi_s>0 && close_s>0 && macd_s>0 && bands_s>0) {
	new_global_tendency=1;
  } else if(force_s < 0 && kdj_s < 0 && rsi_s<0 && close_s<0 && macd_s<0 && bands_s<0) {
    new_global_tendency=-1;
  } else if (global_tendency > 0) {
	if (bands_s > 0 && macd_s > 0)  // bands_s is more bold for tendency
	  new_global_tendency = 1;
  } else if (global_tendency < 0) {
	if (bands_s < 0 && macd_s < 0)
	  new_global_tendency = -1;
  }else 
    new_global_tendency = 0;

  printf("force %f->%f kdj %f->%f rsi %f->%f macd %f->%f bands %f->%f", last_force, current_force,
  		last_kdj, current_kdj,
		last_rsi, current_rsi,
		last_macd, current_macd,
		last_bands, current_bands);
  printf("ema_s %f close_s %f global_tendency %d new_global_tendency %d",
		 ema_s, close_s, global_tendency, new_global_tendency);

  if (OrdersTotal() >= total_orders) {
	if (AccountProfit() > (OrdersTotal() * stoplevel * Point))
	  //	  aggressive_lots = 1;
	  ;
  }
  
  if (new_global_tendency > 0 && global_tendency > 0 && (OrdersTotal() < total_orders || aggressive_lots)) {
    int buy_policy = 0; 
    int stoploss_policy = 1;
	  double stoploss = 0.0;
	  double base_stoploss;
	  double takeprofit = NormalizeDouble(Ask + profit_rate * stoplevel * Point,Digits);

	  base_stoploss = NormalizeDouble(Bid-stoplevel * Point,Digits);
	  if (stoploss_policy == 1) {
		stoploss = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1) - stoplevel * Point;
	  } else 	    
		stoploss = base_stoploss;

	  if (stoploss > base_stoploss)
		stoploss = base_stoploss;

	  // conditional buy
	  if (buy_policy >= 1) {
	    if (Ask >= iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_UPPER, 1)) {
		  stoploss = 0.0;
		}

		if (buy_policy == 2) { // close_s should not be too bigger
		  if (fabs(close_s) > 0.2)
			stoploss = 0.0;
		}else if (buy_policy == 3) { // open and close should not be too bigger
		  if (fabs(iClose(NULL, 0, 1) - iOpen(NULL, 0, 1)) > 0.2)
			stoploss = 0.0;
		}
	  }

	  if (aggressive_lots == 0) // limitted orders
		takeprofit = 0;
	  else if (close_s >= 0) {// only buy if negative
		takeprofit = 0;
		stoploss = 0;
	  }
	  
	  // if need takeprofit then use limitted stoploss
	  if (takeprofit > 0)
		stoploss = base_stoploss;

	  if (no_stoploss) {
	    printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);
	    res=OrderSend(Symbol(),OP_BUY,next_lots,Ask,3,0,0,"",0,0,Blue);
	  } else if (stoploss != 0.0) {
	    printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);
	    res=OrderSend(Symbol(),OP_BUY,next_lots,Ask,3,stoploss,takeprofit,"",0,0,Blue);
	  }
  }
  else if (new_global_tendency < 0 && global_tendency < 0 && (OrdersTotal() < total_orders || aggressive_lots)) {
	int sell_policy = 0;
    int stoploss_policy = 1;
	  double stoploss = 0.0;
	  double base_stoploss;
	  double takeprofit = NormalizeDouble(Bid - profit_rate * stoplevel * Point,Digits);

	  base_stoploss = NormalizeDouble(Ask+stoplevel * Point,Digits);
	  if (stoploss_policy == 1) {
		stoploss = iBands(NULL, 0, bands_period, bands_devia, bands_shift, PRICE_CLOSE, MODE_MAIN, 1) + stoplevel * Point;	    
	  } else
		stoploss = base_stoploss;

	  if (stoploss < base_stoploss)
		stoploss = base_stoploss;
	  
	  // conditional sell
	  if (sell_policy >= 1) {
		if (sell_policy == 2) { // close_s should not be too bigger
		  if (fabs(close_s) > 0.2)
			stoploss = 0.0;
		} else if (sell_policy == 3) { // open and close should not be too bigger
		  if (fabs(iClose(NULL, 0, 1) - iOpen(NULL, 0, 1)) > 0.2)
			stoploss = 0.0;
		}
	  }

	  if (aggressive_lots == 0) // limitted orders
		takeprofit = 0;
	  else if (close_s <= 0) {// only sell if positive
		takeprofit = 0;
		stoploss = 0;
	  }
	  
	  // if need takeprofit then use limitted stoploss
	  if (takeprofit > 0)
		stoploss = base_stoploss;
	  
	  if (no_stoploss) {
	    printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);
	    res=OrderSend(Symbol(),OP_SELL,next_lots,Bid,3,0,0,"",0,0,Red);
	  } else if (stoploss != 0.0) {
	    printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);
		res=OrderSend(Symbol(),OP_SELL,next_lots,Bid,3,stoploss,takeprofit,"",0,0,Red);
	  }
  }else if(global_tendency > 0) {
	if (no_stoploss) {
	  if (bands_s <= 0)
		CheckForCloseWithProfit(OP_BUY);
	  else
		AdjustOrder(OP_BUY);
	} else {
	  if (bands_s <= 0)
		CheckForClose(OP_BUY, 1);
	  else
		AdjustOrder(OP_BUY);
	}
  }else if(global_tendency < 0) {
	if (no_stoploss) {
	  if (bands_s >=0)
		CheckForCloseWithProfit(OP_SELL);
	  else
		AdjustOrder(OP_SELL);
	} else {
	  if (bands_s >= 0)
		CheckForClose(OP_SELL, 1);
	  else
		AdjustOrder(OP_SELL);
	}
  }else if (bands_s < 0) {
	if (no_stoploss) 
	  ;
	else
	  AdjustOrder(OP_SELL);
  } else if(bands_s > 0) {
	if (no_stoploss)
	  ;
	else
	  AdjustOrder(OP_BUY);
  }
  
  global_tendency = new_global_tendency;
  
  return ;
  
  if(global_tendency>0) 
    {
      
//      if(force_s < 0.0)
//	buy_s=1;
      if(close_s < 0.0)
	buy_s=1;

//      printf("buy_s %d", buy_s);

      if (close_s > 0)
	
      
      //    if(buy_s > 0 && (AccountProfit() > -30)) {

      if(AccountProfit() >=0)
        {
		  //	  double stoplevel= MarketInfo(Symbol(),MODE_STOPLEVEL);
	  double stoploss = NormalizeDouble(Bid-stoplevel * Point,Digits);
	  double takeprofit = NormalizeDouble(Ask + 2 * stoplevel * Point,Digits);

	  printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);

	  res=OrderSend(Symbol(),OP_BUY,0.01,Ask,3,stoploss,0,"",0,0,Blue);
        }
      //      else
      //         CheckForClose(OP_BUY,0);
    }

  if(global_tendency<0) 
    {
//      if(force_s > 0.0)
//	sell_s=1;
//      if(close_s > 0.0)
//	sell_s=1;

//      printf("sell_s %d", sell_s);

      if (close_s < 0)
	AdjustOrder(OP_SELL);
      else
	CheckForClose(OP_SELL, 1);
		
      if(AccountProfit() >= 0)
        {
		  //	  double stoplevel= MarketInfo(Symbol(),MODE_STOPLEVEL);
	  double stoploss = NormalizeDouble(Ask+stoplevel * Point,Digits);
	  double takeprofit = NormalizeDouble(Bid - 2 * stoplevel * Point,Digits);

	  printf("orders %d->%d", OrdersTotal(), OrdersTotal()+1);

	  res=OrderSend(Symbol(),OP_SELL,0.01,Bid,3,stoploss,0,"",0,0,Red);
        }
      //      else
      //         CheckForClose(OP_SELL,0);

    }
  // if (sell_s)
  // res = OrderSend(Symbol(),OP_SELL,0.01,Bid,3,0,0,"",0,0,Red);

  // tendency shift to down
  if(new_global_tendency>0 && global_tendency<0) 
    {
      //   if (AccountProfit() < -50) {
      int buys,sells;

      Print("do force close for buy orders");
      
      CheckForClose(OP_BUY,1);

      buys=CalculateCurrentOrders(Symbol(),OP_BUY);
      sells=CalculateCurrentOrders(Symbol(),OP_SELL);
      //    if ((buys+sells) > 0)
      //      res=OrderSend(Symbol(),OP_SELL,0.01*(buys+sells),Bid,3,0,0,"",0,0,Red);
    }

  //  Print("FreeMargin: ", AccountFreeMargin());  
  //  Print("Margin: ", AccountMargin());
  //  Print("Profit: ", AccountProfit());

  // tendency shift to up 
  if(new_global_tendency<0 && global_tendency>0) 
    {
	Print("do force close for sell orders");
      CheckForClose(OP_SELL,1);
    }

}
//+------------------------------------------------------------------+
