from models.currency import CurrencyModel


class ExchangeModel():
    def __init__(self, base: CurrencyModel, target: CurrencyModel):
        self.base_currency = base
        self.target_currency = target

    def json(self):
        pass

    @staticmethod
    def convert(base_amount: float, target_currency: str):
        rate = 2.00
        return CurrencyModel(target_currency, base_amount * rate)
