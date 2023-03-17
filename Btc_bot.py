import json
import time
import websocket
from websocket import create_connection
import requests
from ApiTauros import getOrders, putOrderLimit,closeAllOrders
from enum import Enum
class Sides(Enum):
    BUY = "BUY"
    SELL = "SELL"
# bids compra// asks venta
coin="BTC"
limitPercentageSell=8
limitPercentageBuy=8
amountToBuy="0.0007"
buyAvailable=True
sellAvailable=True
url_bitso = "https://api.bitso.com/v3/ticker/?book="+coin.lower()+"_mxn"


def valid_if_order_exists(price,orders,side):
    exists = None
    for order in orders:
        if(side==Sides.SELL):
            if(float(order["price"]) <= float(price)):
                exists= order["price"]    
        else:    
            if float(order["price"]) >= float(price):
                exists= order["price"]       
    return exists    

def print_value(title, value):
    print(title,str(value))


def get_price_market(url):
    r = requests.get(url)
    data= json.loads(r.text)
    payload=data["payload"]
    last_price_market= payload["last"]
    print_value("Last Price MARKET",last_price_market)
    return last_price_market


def get_spreed_by_prices(price, price_market,side):
    spreed = None
    if(side==Sides.SELL):
        spreed= ((float(price)/float(price_market))-1)*100
    else:
        spreed = ((float(price_market)/float(price))-1)*100
    print_value("Spreed",spreed)
    return spreed
 
def order_no_exists_and_greater(exist,spreed,side,available):
    limit_percentage =  side==Sides.BUY if limitPercentageBuy else limitPercentageSell
    return  exist==False and spreed>limit_percentage and available


def create_order(asks,bids):
    sell_orders= getOrders(coin,Sides.SELL)
    first_ask= asks[0]    
    first_bid= bids[0]
    price_market= get_price_market(url_bitso)
    price_to_sell=float(first_ask["p"])-1
    sell_exists = valid_if_order_exists(first_ask["p"],sell_orders,Sides.SELL)
    spreed_sell= get_spreed_by_prices(price_market,price_to_sell,Sides.SELL)  
    
    print("Percentage: "+ str(spreed_sell))
    print("Sell position", str(price_to_sell))
    print("Exist Order",sell_exists)

    if order_no_exists_and_greater(sell_exists,spreed_sell,Sides.SELL,sellAvailable):
        closeAllOrders(sell_orders)
        putOrderLimit(price_to_sell,amountToBuy,"SELL",coin)
    else:
        try:
            percentage_to_close= ((float(sell_exists)/float(price_market))-1)*100
            if percentage_to_close<limitPercentageSell:
                closeAllOrders(sell_orders)
        except:
            print("NO EXISTE")
            raise    
    
    price_to_buy=float(first_bid["p"])+1
    buy_orders=getOrders(coin,Sides.BUY)
    buy_exists = valid_if_order_exists(first_bid["p"],buy_orders,Sides.BUY)
    spreed_buy= get_spreed_by_prices(price_to_buy,price_market,Sides.BUY)
    print("Buy Percentage: "+ str(spreed_buy))
    print("Buy position", str(price_to_buy))
    print("Buy Exist Order",buy_exists)
    if order_no_exists_and_greater(buy_exists,spreed_buy,Sides.BUY,buyAvailable):
        closeAllOrders(buy_orders)
        putOrderLimit(price_to_buy,amountToBuy,"BUY",coin)
    else :
        try:
            percentage_to_close= ((float(price_market)/float(buy_exists))-1)*100
            if percentage_to_close<limitPercentageBuy:
                closeAllOrders(buy_orders)
        except:
            print("No existe")
            raise
        
    
def on_message(wsapp, message):
    print("-------------------")
    data = json.loads(message)
    value = data.get("data")
    if value:
        asks=value["asks"]
        bids=value["bids"]
        create_order(asks,bids)
   



sendOption=json.dumps({ 
        "action": 'subscribe',
          "market": coin + "-MXN",
          "channel": 'orderbook'})


websocket.enableTrace(True)




def on_open(wsapp):
    wsapp.send(sendOption)


def on_close(wsapp, close_status_code, close_msg):
    # Because on_close was triggered, we know the opcode = 8
    print("Close")
def on_ping():
    print("Ping")
   
urlSocket="wss://wsv2.tauros.io"

wsapp = websocket.WebSocketApp(urlSocket, on_open=on_open,on_message=on_message,on_close=on_close,on_ping=on_ping,keep_running=True)



if __name__ == "__main__":
    while True:
        try:
            websocket.enableTrace(False)
            loop =websocket.WebSocketApp(urlSocket, on_open=on_open,on_message=on_message,on_close=on_close,on_ping=on_ping,keep_running=True)
            loop.run_forever(skip_utf8_validation=True,ping_interval=10,ping_timeout=8)
        except Exception as e:
            time.sleep(5) 
    