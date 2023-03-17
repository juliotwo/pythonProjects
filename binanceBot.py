
#importar librerías
from enum import Enum
from urllib.parse import urlencode
import time
from telegram_bot import send_message


from dotenv import dotenv_values, load_dotenv

load_dotenv()

config = dotenv_values(".env")

#key y secret
api_key = config["API_KEY_BINANCE"]
api_secret = config["API_SECRET_BINANCE"]

from binance.spot import Spot

client = Spot()

# Get server timestamp


# API key/secret are required for user data endpoints
client = Spot(api_key, api_secret)

# Get account and balance information

coinPrincipal="BTC"
symbolPrincipal = "BTCUSDT"
percentageToTrade = 2.5
percentageToTrade24h = -3.5

class TYPE_SIDES(Enum):
    SELL = "SELL"
    BUY = "BUY"



def get_balance_to_trade(coin):
    params = {
    'asset': coin
    }
    asset = client.user_asset(**params)   
    try:
        free = float(asset[0]["free"])
        if free>100:
            return 100
        if coin == "BTC":
            return round((free / 2),8)
    except Exception:
        return 0


def get_data_by_last_trade(trades):   
    last_trade_price =  trades[0]
    return last_trade_price["isBuyer"],last_trade_price["price"]

def get_last_trades(symbol):
    params = {
    'limit': 1
    }
    trades=client.my_trades(symbol,**params)
    return trades


def get_exchange_info(symbol):
    params = {
    'symbol': symbol
    }
    coin_info =client.ticker_24hr(**params)
    return coin_info

def get_last_price(symbol):
    last_price =client.ticker_price(symbol)
    return last_price["price"]

def get_trade_side(is_buyer):
    if is_buyer==True:
        return TYPE_SIDES.SELL
    else:
        return TYPE_SIDES.BUY
    
def get_side_by_last_trade(is_buyer):
    if is_buyer==True:
        return TYPE_SIDES.BUY
    else:
        return TYPE_SIDES.SELL




def create_market_order(symbol,side):
    # Post a new order
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
    }
    
    if side==TYPE_SIDES.BUY:
        quantity = get_balance_to_trade("USDT") 
        params["quoteOrderQty"] = quantity
    else:
        quantity = get_balance_to_trade("BTC") 
        params["quantity"] = float(quantity)

    try:
        response = client.new_order(**params)
        print(response)
        send_message("Se ejecuto una orden, detalle")
        send_message(str(response))
    except Exception:
        print("Error")

## el monto 1 debe ser mayor para dar positivo
def get_difference_percentage(monto_1, monto_2):
    diferencia = float(monto_1) - float(monto_2)
    porcentaje = (diferencia / float(monto_2)) * 100
    return porcentaje

def can_execute_trade(price_last_trade, current_price, side_last_trade):
    if side_last_trade == TYPE_SIDES.BUY:
        is_hight = float(current_price) > float(price_last_trade)
        percentage = get_difference_percentage(current_price,price_last_trade)
        print("percentage to sell")
        print(percentage)
        if is_hight and percentage > percentageToTrade:
            print("Approve to sell")
            return True
        else:
            return False
    else:
        is_lower = float(current_price) < float(price_last_trade)
        percentage = get_difference_percentage(price_last_trade,current_price)
        print("percentage to buy")
        print(percentage)
        if is_lower and percentage > percentageToTrade:
            print("Approve to buy")
            return True
        else:
            return False
def can_execute_trade_24h():
    amount_usdt = get_balance_to_trade("USDT")
    if amount_usdt > 20:
        percentage = float(get_exchange_info(symbolPrincipal)["priceChangePercent"])
        if percentage < percentageToTrade24h:
            print("Approve to BUY 24h")
            create_market_order(symbolPrincipal,TYPE_SIDES.BUY.value)
            return True

def principal_bot():
    trades = get_last_trades(symbolPrincipal)
    is_buyer,price_last_trade = get_data_by_last_trade(trades)
    current_price = get_last_price(symbolPrincipal)
    side_last_trade = get_side_by_last_trade(is_buyer)
    can_execute = can_execute_trade(price_last_trade,current_price,side_last_trade)
    side_to_trade = get_trade_side(is_buyer)

    if can_execute:
        create_market_order(symbolPrincipal,side_to_trade.value)
    else:
        can_execute_trade_24h()
        # logica para tradiar con base en ultimas 24h
    


while True:
    print("Bot init")
    principal_bot()
    # Esperar 10 segundos antes de repetir la consulta
    time.sleep(10)