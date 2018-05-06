import os
#os.system('pip install git+git://github.com/guptarohit/cryptoCMD.git')
from cryptocmd import CmcScraper

crypto_name = os.sys.argv[1]
scraper = CmcScraper(crypto_name)

headers, data = scraper.get_data()

scraper.export_csv(crypto_name+'_all_time.csv')