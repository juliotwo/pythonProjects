
from tauros_api import TaurosAPI
# Staging
# api_key = '757ce670402a6d74ef2a2e67122a89592eca2356'
# api_secret = 'OWEwNjQ5YzJlYWJkMWFmMDU5Y2YwZjg3NzYzYzIwNGU1MTRhZTYyMGViN2M4NGM2NWMxYjFmMmU1NzdlNTc4OA=='
# Master

api_key = ''
api_secret = ''


# api_key=input("Pon tu api\n")
# api_secret=input("Pon tu api\n")
tauros = TaurosAPI(api_key, api_secret, staging=False) # default staging=False

def get_order_market(coin,currency,side,amount=None,value=None):
    path = '/otc/v1/spot-trade/quote'
    data = {
        "market": coin + "-" + currency,
        "side":side,
    }
    
    
    if (amount): 
        data["amount"] = str(amount) 
    else: 
        data["value"] =  str(value) 
    try:
        print(data)
        response = tauros.post(path, data)
        print("response")
        print(response.body)
    except NameError:
        print(NameError)

     

def putOrderLimit(price, amount,side,coin):
    path = '/api/v1/trading/placeorder/'
    data = {
        "market": coin+"-MXN",
        "amount": str(amount),
        "side": side,
        "type": "LIMIT",
        "price": str(price)
    }
    response = tauros.post(path, data)
    status=response.body
    print("STATUS")
    print(status)
    return
   
 
def getOrders(coin,side):
    path="/api/v1/trading/myopenorders/"
    response=tauros.get(path)
    body = response.body
    data= body["data"]
    filter_data=list(filter(lambda x: x["left_coin"] ==coin, data))
    filter_by_side=list(filter(lambda x: x["side"] ==side, filter_data))
    return filter_by_side

def getAllOrders():
    path="/api/v1/trading/myopenorders/"
    response=tauros.get(path)
    body = response.body
    data= body["data"]
    return data

def closeOrder(id):
    path="/api/v1/trading/closeorder/"
   
    data = {
        "id": int(id),
    }
    response=tauros.post(path,data)
    return response.status_code


    
def TaurosTransfer(amount,email,coin):
    path="/api/v3/wallets/inner-transfer/"
    data = {
        "coin":coin,
        "amount": amount,
        "nip":"331215",
        "recipient": email,
        "description": "TRansferencia API",
    }
    response=tauros.post(path,data)
    print(response)
    return response.status_code


def closeAllOrders(orders):
    for order in orders:
        idOrder=order["order_id"]
        closeOrder(idOrder)

if __name__ == "__main__":
   get_order_market("BTC","USDC","BUY",None,5)