import json
import time
import websocket
from websocket import create_connection
import requests
from ApiTauros import getOrders, putOrderLimit,closeAllOrders
# bids compra// asks venta
coin="BTC"
limitPercentageSell=5
limitPercentageBuy=6
amountToBuy="0.002"
buyAvailable=True
sellAvailable=True

def validOrderExistsSell(priceToPut):
    orders = getOrders(coin)
    filterOrders=list(filter(lambda x: x["side"] =="SELL", orders))
    exists = False
    try:
        for order in filterOrders:
            if float(order["price"]) <= float(priceToPut):
                exists= order["price"]    
    except:
        print("An exception occurred")
  
    return exists

def validOrderExistsBuy(priceToPut,orders):
  
    exists = False
    try:
        for order in orders:
            if float(order["price"]) >= float(priceToPut):
                exists= order["price"]    
    except:
        print("An exception occurred")
    
    return exists
    



def putOrder(asks,bids):
    firstAsk= asks[0]
    priceAsk=firstAsk["p"]
    firstbid= bids[0]
    priceBid=firstbid["p"]
    url="https://api.bitso.com/v3/ticker/?book="+coin.lower()+"_mxn"
    print(url)
    r = requests.get(url)
    data= json.loads(r.text)
    payload=data["payload"]
    lastPrice= payload["last"]
    print("Last Price bitso",lastPrice)
    # lastPrice= 1190000
    priceToPutSell=float(firstAsk["p"])-1
    sellExists = validOrderExistsSell(firstAsk["p"])


    percentageSell= ((float(priceToPutSell)/float(lastPrice))-1)*100

    print("Percentage: "+ str(percentageSell))
    print("Sell position", str(priceToPutSell))
    print("Exist Order",sellExists)

    orders = getOrders(coin)
    filterOrdersSell=list(filter(lambda x: x["side"] =="SELL", orders))
    if sellExists==False and priceToPutSell > float(lastPrice) and percentageSell>limitPercentageSell :
        print("Orden")
        closeAllOrders(filterOrdersSell)
        if sellAvailable:
            status=putOrderLimit(priceToPutSell,amountToBuy,"SELL",coin)
            print(status)
    else:
        try:
            percentageToClose= ((float(sellExists)/float(lastPrice))-1)*100
            if percentageToClose<limitPercentageSell:
                closeAllOrders(filterOrdersSell)
        except:
            print("NO EXISTE")
        
        
    
    
    priceToPutBuy=float(firstbid["p"])+1
    filterOrdersBuy=list(filter(lambda x: x["side"] =="BUY", orders))
    buyExists = validOrderExistsBuy(firstbid["p"],filterOrdersBuy)
    percentageBuy= ((float(lastPrice)/float(priceToPutBuy))-1)*100
    print("Buy Percentage: "+ str(percentageBuy))
    print("Buy position", str(priceToPutBuy))
    print("Buy Exist Order",buyExists)
    if buyExists==False and priceToPutBuy < float(lastPrice) and percentageBuy>limitPercentageBuy :
        closeAllOrders(filterOrdersBuy)
        if buyAvailable:
            status=putOrderLimit(priceToPutBuy,amountToBuy,"BUY",coin)
            print("STATUS")
            print(status)
    else :
        try:
            percentageToClose= ((float(lastPrice)/float(buyExists))-1)*100
            if percentageToClose<limitPercentageBuy:
                closeAllOrders(filterOrdersBuy)
        except:
            print("No existe")
        
    
    



def on_message(wsapp, message):
    print("-------------------")
    data = json.loads(message)
    value = data.get("data")
    if value:
        asks=value["asks"]
        bids=value["bids"]
        putOrder(asks,bids)
   



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
    