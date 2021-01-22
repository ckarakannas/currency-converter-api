class CurrencyModel():
    def __init__(self, currency="", amount=0):
        self.currency = currency
        self.amount = amount

    def json(self):
        return {'currency': self.currency,
                'amount': self.amount}
