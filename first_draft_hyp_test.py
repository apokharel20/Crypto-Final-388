

    

from googlefinance.client import get_price_data
import statistics

# Collect prices per month from a given market
def collect_market(stock, years=10):
    param = {}
    param['q'] = stock
    param['i'] = '86400'
    param['p'] = str(years) + 'Y'
    df = get_price_data(param)
    #df['date'] = df.index.map(lambda x: x.strftime('%Y-%m'))
    #df = df.groupby('date').mean()
    return df.loc[:, df.columns != 'Volume']  

def get_mean_std_dev (df1, df2, time1, time2):
    '''
    get duration from times
    get day by day prices from dfs via time
    get mean and standard deviation of both df prices

    RETURN
    tuple of tuple of (mean, std_dev) for df1 and df2 across time
    '''
    pass

def fluxs(time):
    flux = []
    tech_prices = collect_market('NDAQ', time)

    first_entry = True
    prev_close = -1
    curr_close = -1
    for price in tech_prices['Close']:
    	if first_entry:
    		prev_close = price
    		first_entry = False
    		continue
    	curr_close = price
    	diff = curr_close - prev_close
    	flux.append(diff)
    	prev_close = curr_close

    return flux  

tech_init_flux = fluxs(2)

def get_mean(l):
	return sum(l)/len(l)

tech_init_mean = get_mean(tech_init_flux)

def get_std_dev(l):
	sum_sq_dev = sum((x - get_mean(l))**2 for x in l)
	var = sum_sq_dev/len(l)
	return var**.5

tech_init_stddev = get_std_dev(tech_init_flux)

print(tech_init_mean, tech_init_stddev)

# Technology market
tech_prices = collect_market('NDAQ')
#print(tech_prices, 2)

# Renewable energy market
energy_prices = collect_market('OSPTX')

# Real state market
state_prices = collect_market('DJUSRE')

# Oil market
oil_prices = collect_market('CL1')

# Gold market
gold_prices = collect_market('HUI')