

from bitcoin import MyClass
if __name__ == '__main__':

    moneda = input("Moneda\n")
    spreedVenta= input("Spreed venta\n")
    spreedCompra= input("Spreed compra\n")
    amountBuy= input("Monto compra\n")
    varBTC = MyClass(moneda, spreedCompra,spreedVenta,amountBuy,True,True)
