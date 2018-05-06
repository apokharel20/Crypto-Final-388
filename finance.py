#!/usr/bin/env python3

from googlefinance.client import get_price_data

# Collect prices per month from a given market
def collect_market(stock, years=10):
    param = {}
    param['q'] = stock
    param['i'] = '86400'
    param['p'] = str(years) + 'Y'
    df = get_price_data(param)
    df['date'] = df.index.map(lambda x: x.strftime('%Y-%m'))
    df = df.groupby('date').mean()
    return df.loc[:, df.columns != 'Volume']    

# Technology market
tech_prices = collect_market('NDAQ')

# Renewable energy market
energy_prices = collect_market('OSPTX')

# Real state market
state_prices = collect_market('DJUSRE')

# Oil market
oil_prices = collect_market('CL1')

# Gold market
gold_prices = collect_market('HUI')
print(gold_prices)
