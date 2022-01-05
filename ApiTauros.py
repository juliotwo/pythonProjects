
from tauros_api import TaurosAPI
# Staging
# api_key = '757ce670402a6d74ef2a2e67122a89592eca2356'
# api_secret = 'OWEwNjQ5YzJlYWJkMWFmMDU5Y2YwZjg3NzYzYzIwNGU1MTRhZTYyMGViN2M4NGM2NWMxYjFmMmU1NzdlNTc4OA=='
# Master

# api_key = '003d3a5499214d8d80e2a96ed8af59133ac8e456'
# api_secret = 'NTZkZDBjYjEzMWUyMTU0YjZkODgzNTU0M2UzYTM2YTFhNTY3YjI5OTJkYzRlZjIzZWI4MGI5ODhlNGU4YjYxYQ=='


api_key=input("Pon tu api\n")
api_secret=input("Pon tu api\n")
tauros = TaurosAPI(api_key, api_secret, staging=False) # default staging=False

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
    return status
   
 
def getOrders(coin):
    path="/api/v1/trading/myopenorders/"
    response=tauros.get(path)
    body = response.body
    data= body["data"]
    filterData=list(filter(lambda x: x["left_coin"] ==coin, data))
    return filterData
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

# if __name__ == "__main__":
#    TaurosTransfer("300","lizehtalejandra@gmail.com","MXN")