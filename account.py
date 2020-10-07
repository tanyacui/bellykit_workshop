class Hold():
    def __init__(self, symbol, price, share, adj_price):
        self.symbol = symbol
        self.price = price
        self.share = share
        self.adj_price = adj_price
        self.cost = price * share

    def __str__(self):
        return f'Stock[{self.symbol}]'

    def __bool__(self):
        if self.share:
            return True
        else:
            return False


class Account():
    def __init__(self, equity=1000000):
        self.equity = equity

        self.hold = None
        self.to_buy = None
        self.to_sell = None

        self.__row = None

    def buy(self, symbol, over=False):
        print('預計隔天買進', symbol)
        self.to_buy = symbol

    def sell(self):
        if self.is_empty():
            print('nothing to sell')
        else:
            print('預計隔天賣出', self.hold)
            self.to_sell = True

    def is_empty(self):
        if self.hold:
            return False
        else:
            return True

    def handle_order(self, row):
        self.__row = row

        if self.to_sell:
            print(f'{self.hold.symbol} 賣出成交')
            row = self.__row
            price = row[self.hold.symbol, 'open']
            adj_price = row[self.hold.symbol, 'adj_open']
            share = self.hold.share
            realized_equity = int(self.hold.cost * adj_price / self.hold.adj_price)

            self.equity += realized_equity

            print('entry/ exit price:', self.hold.price, price)
            print('share:', share, 'cost:', self.hold.cost)
            print('realized_equity:', realized_equity)
            print('equity change:', realized_equity - self.hold.cost)

            self.hold = None
            self.to_sell = False


        if self.to_buy:
            print(f'{self.to_buy} 買進成交')
            symbol = self.to_buy
            share = int(self.equity / row[symbol, 'open'])
            cost = share * row[symbol, 'open']
            new_hold = Hold(symbol = symbol,
                        price = row[symbol, 'open'],
                        share = share,
                        adj_price = row[symbol, 'adj_open'])


            self.hold = new_hold
            self.equity -= cost
            self.to_buy = None
