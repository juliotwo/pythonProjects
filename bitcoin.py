import json
import time
import websocket
from websocket import create_connection
import requests
from ApiTauros import getOrders, putOrderLimit,closeAllOrders
urlSocket="wss://wsv2.tauros.io"

class MyClass:
# bids compra // asks venta   
    def __init__(self,coin,limitSell,limitBuy,amountToBuy,buyAvailable,sellAvailable):
        self.coin = coin
        self.limitSell= int(limitSell)
        self.limitBuy=int(limitBuy)
        self.amountToBuy= amountToBuy
        self.buyAvailable= buyAvailable
        self.sellAvailable = sellAvailable
        while True:
            try:
                websocket.enableTrace(False)
                loop =websocket.WebSocketApp(urlSocket, on_open=self.on_open,on_message=self.on_message,on_close=self.on_close,on_ping=self.on_ping,keep_running=True)
                loop.run_forever(skip_utf8_validation=True,ping_interval=10,ping_timeout=8)
            except Exception as e:
                time.sleep(5) 
    
    def validOrderExistsSell(self,priceToPut):
        orders = getOrders(self.coin)
        filterOrders=list(filter(lambda x: x["side"] =="SELL", orders))
        exists = False
        try:
            for order in filterOrders:
                if float(order["price"]) <= float(priceToPut):
                    exists= order["price"]    
        except:
            print("An exception occurred")
    
        return exists

    def validOrderExistsBuy(self,priceToPut,orders):
        exists = False
        try:
            for order in orders:
                if float(order["price"]) >= float(priceToPut):
                    exists= order["price"]    
        except:
            print("An exception occurred")
        return exists
    



    def putOrder(self,asks,bids):
        firstAsk= asks[0]
        priceAsk=firstAsk["p"]
        firstbid= bids[0]
        priceBid=firstbid["p"]
        url="https://api.bitso.com/v3/ticker/?book="+self.coin.lower()+"_mxn"
        print(url)
        r = requests.get(url)
        data= json.loads(r.text)
        payload=data["payload"]
        lastPrice= payload["last"]
        print("Last Price bitso",lastPrice)
        # lastPrice= 1190000
        priceToPutSell=float(firstAsk["p"])-0.01
        sellExists = self.validOrderExistsSell(firstAsk["p"])
        print("venta")
        print(firstAsk["p"])
        percentageSell= ((float(priceToPutSell)/float(lastPrice))-1)*100

        print("Percentage: "+ str(percentageSell))
        print("Sell position", str(priceToPutSell))
        print("Exist Order",sellExists)

        orders = getOrders(self.coin)
        filterOrdersSell=list(filter(lambda x: x["side"] =="SELL", orders))
        if sellExists==False and priceToPutSell > float(lastPrice) and percentageSell>self.limitSell :
            print("Orden")
            closeAllOrders(filterOrdersSell)
            if self.sellAvailable:
                status=putOrderLimit(priceToPutSell,self.amountToBuy,"SELL",self.coin)
                print(status)
        else:
            try:
                percentageToClose= ((float(sellExists)/float(lastPrice))-1)*100
                if percentageToClose<self.limitSell:
                    closeAllOrders(filterOrdersSell)
            except:
                print("NO EXISTE")
            
            
        
        print("Buy init....")
        priceToPutBuy=float(firstbid["p"])+0.01
        print("Buy init....1")
        
        filterOrdersBuy=list(filter(lambda x: x["side"] =="BUY", orders))
       
        print("Buy init....2")
        buyExists =self.validOrderExistsBuy(firstbid["p"],filterOrdersBuy)
        print("Buy init....3")
        print(priceToPutBuy)
        percentageBuy= ((float(lastPrice)/float(priceToPutBuy))-1)*100
        print("Buy Percentage: "+ str(percentageBuy))
        print("Buy position", str(priceToPutBuy))
        print("Buy Exist Order",buyExists)
        if buyExists==False and priceToPutBuy < float(lastPrice) and percentageBuy>self.limitBuy :
            closeAllOrders(filterOrdersBuy)
            if self.buyAvailable:
                status=putOrderLimit(priceToPutBuy,self.amountToBuy,"BUY",self.coin)
                print("STATUS")
                print(status)
        else :
            try:
                percentageToClose= ((float(lastPrice)/float(buyExists))-1)*100
                if percentageToClose<self.limitBuy:
                    closeAllOrders(filterOrdersBuy)
            except:
                print("No existe")
        
    
    



    def on_message(self,wasps, message):
        print("-------------------")
        data = json.loads(message)
        value = data.get("data")
        if value:
            asks=value["asks"]
            bids=value["bids"]
            self.putOrder(asks,bids)
   






    def on_open(self,wasps):
        sendOption=json.dumps({ 
                "action": 'subscribe',
                "market": self.coin + "-MXN",
                "channel": 'orderbook'})
        wasps.send(sendOption)

    def on_close(wasps, close_status_code, close_msg):
        # Because on_close was triggered, we know the opcode = 8
        print("Close")
    def on_ping():
        print("Ping")
   
 


    