

from bitcoin import MyClass
if __name__ == '__main__':

    moneda = input("Moneda\n")
    spreedVenta= input("Spreed venta\n")
    spreedCompra= input("Spreed compra\n")
    varBTC = MyClass(moneda, spreedCompra,spreedVenta,10,True,True)
