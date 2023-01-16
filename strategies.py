import indicators as ind
import random as rand

class Portfolio:
    def __init__(self, cash, assets):
        self.cash = cash
        self.assets = assets

    def buyAssets(self, cash_for_buying, price, print=False):
        self.cash -= cash_for_buying
        self.assets += cash_for_buying/price
        if print:
            print("Bought", cash_for_buying, "cash worth of assets at a price of", price)
        return [-cash_for_buying, cash_for_buying/price]

    def sellAssets(self, assets_to_sell, price, print = False):
        self.cash += assets_to_sell * price
        self.assets -= assets_to_sell
        if print:
            print("Sold", assets_to_sell, "assets at the price of", price)
        return [assets_to_sell*price, -assets_to_sell]

    def value(self, price):
        return self.cash + self.assets*price

class Position:
    def __init__(self, kind, amount, target, stopLoss, timeExit):
        self.kind = kind            # "Long" or "Short"
        self.amount = amount        # Acquired assets if Long, acquired cash if Short
        self.target = target
        self.stopLoss = stopLoss
        self.timeExit = timeExit

    def check(self, currentPrice, time):
        if self.kind == "Long":
            if (currentPrice > self.target or currentPrice < self.stopLoss or time > self.timeExit):
                return True
        if self.kind == "Short":
            if (currentPrice < self.target or currentPrice > self.stopLoss or time > self.timeExit):
                return True
        return False

def hold(price):
    """Just hold the assets."""
    pf = Portfolio(cash=1000, assets=0)
    pf.buyAssets(pf.cash, price[0])
    return pf.value(price.iloc[-1])

def random(price):
    """Randomly trade assets."""
    pf = Portfolio(cash=1000, assets=0)
    for i in range(len(price)):
        if rand.randint(0, 1) == 0:
            pf.buyAssets(0.1*pf.cash, price[i])
        elif pf.assets > 0:
            pf.sellAssets(pf.assets, price[i])
    return pf.value(price.iloc[-1])

def simple_sma(price, n=10, m=1.1):
    """Buy or sell depending on moving average."""
    pf = Portfolio(cash=1000, assets=0)
    sma = ind.sma(price, n)
    for i in range(n, len(price)):
        if price[i] >  m * sma[i]:
            pf.buyAssets(0.1*pf.cash, price[i])
        elif (price[i] < sma[i] / m and pf.assets > 0):
            pf.sellAssets(pf.assets, price[i])
    return pf.value(price.iloc[-1])

def simple_sma_positions(price, n=10, m=1.1):
    """Take long or short positions depending on moving average."""
    pf = Portfolio(cash=1000, assets=0)
    positions = []
    sma = ind.sma(price, n)
    for i in range(n, len(price)):
        if price[i] >  m * sma[i]:
            pf.buyAssets(0.1*pf.cash, price[i])
            positions.append(Position("Long", 0.1*pf.cash/price[i], price[i]*1.2, price[i]*0.8, 15))
        elif (price[i] < sma[i] / m and pf.assets > 0):
            pf.sellAssets(pf.assets, price[i])
            positions.append(Position("Short", pf.assets*price[i], price[i]*0.8, price[i]*1.2, 15))
        if positions != []:
            for pos in positions:
                if pos.check(price[i], i):
                    if pos.kind == "Long":
                        pf.sellAssets(pos.amount, price[i])
                    elif pos.kind == "Short":
                        pf.buyAssets(pos.amount, price[i])
                    positions.remove(pos)
    if positions != []:
        for pos in positions:
            if pos.kind == "Long":
                pf.sellAssets(pos.amount, price[i])
            elif pos.kind == "Short":
                pf.buyAssets(pos.amount, price[i])
            positions.remove(pos)
    return pf.cash + pf.assets*price.iloc[-1]

def sma_rsi(price, high, low):
    """Takes positions if sma and rsi agree."""
    pf = Portfolio(cash=1000, assets=0)
    n_sma, m, n_rsi = 5, 1.1, 5
    sma = ind.sma(price, n_sma)
    rsi = ind.rsi(high, low, n_rsi)
    positions = []
    for i in range(len(price)):
        if (price[i] >  m * sma[i] and rsi[i] > 70):
            pf.buyAssets(0.1*pf.cash, price[i])
            positions.append(Position("Long", 0.1*pf.cash/price[i], price[i]*1.2, price[i]*0.8, 15))
        elif (price[i] < sma[i] / m and rsi[i] <30 and pf.assets > 0):
            pf.sellAssets(pf.assets, price[i])
            positions.append(Position("Short", pf.assets*price[i], price[i]*0.8, price[i]*1.2, 15))
        if positions != []:
            for pos in positions:
                if pos.check(price[i], i):
                    if pos.kind == "Long":
                        pf.sellAssets(pos.amount, price[i])
                    elif pos.kind == "Short":
                        pf.buyAssets(pos.amount, price[i])
                    positions.remove(pos)
    if positions != []:
        for pos in positions:
            if pos.kind == "Long":
                pf.sellAssets(pos.amount, price[i])
            elif pos.kind == "Short":
                pf.buyAssets(pos.amount, price[i])
            positions.remove(pos)
    return pf.cash + pf.assets*price.iloc[-1]