import json
from schemas.rates import rates_schema

f_name = "conversion_rates.json"
try:
    with open(f_name) as f:
        data = json.load(f)
        if not isinstance(data, list):
            data = [data]
        rates_data = rates_schema.load(data)
except IOError:
    print("Could not read file:", f_name)
