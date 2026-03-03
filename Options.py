import math

class Option:
    def __init__(self, daysToExpiration = 5, strike = 100, rate = 4 / 100, vol = 100 / 100, underlyingPrice = 100):
        self.daysToExpiration = daysToExpiration
        self.strike = strike
        self.rate = rate
        self.vol = vol
        self.underlyingPrice = underlyingPrice
        
        self.timeToExpiration = self.daysToExpiration / 365
        self.discountFactor = math.exp(-self.rate * self.timeToExpiration)

        strikeGrowth = math.log(self.underlyingPrice / self.strike)
        otherGrowth = (self.rate - self.vol**2/2) * self.timeToExpiration
        standardDeviation = self.vol * math.sqrt(self.timeToExpiration)
        self.d2 = (strikeGrowth + otherGrowth) / standardDeviation
        self.d1 = self.d2 + standardDeviation

    def CDF(self, x):
        return 1/2 + (x - x**3/6 + x**5/40 - x**7/336) / math.sqrt(2*math.pi)
    
    def call(self):
        valueAboveStrike = self.underlyingPrice * self.CDF(self.d1)
        costOfStrike = self.strike * self.CDF(self.d2) * self.discountFactor
        return valueAboveStrike - costOfStrike

contract = Option(
    daysToExpiration = 1.75,
    strike = 180,
    rate = 4 / 100,
    vol = 54 / 100,
    underlyingPrice = 182.48
    )

print(contract.call())