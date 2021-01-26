class RatesModel:
    def __init__(self, base: dict, rates: dict, date="", **kwargs):
        self.date = date
        self.base = base
        self.rates = rates

    @classmethod
    def create_dict(cls, *data):
        rates_dict = {}
        for item in data:
            rates_dict[item['base']] = cls(**item)
        return rates_dict
