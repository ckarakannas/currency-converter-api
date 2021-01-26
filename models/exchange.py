class ExchangeModel:
    def __init__(self, base: str, target: str, amount: float):
        self.base = base
        self.target = target
        self.amount = amount
        self.converted_amount = None
        self.conversion_rate = None

    def convert(self):
        self.converted_amount = round(self.amount * self.conversion_rate, 4)
        return None
