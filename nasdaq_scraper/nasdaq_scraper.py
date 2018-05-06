from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os



def ScrapeOneStock(driver, url, stock, time_stamp, download_dir):
    
    driver.get(url)
    actions = ActionChains(driver)
    # range1D, range5D, range1m

    #print (driver.page_source.encode("utf-8"))
    
    #iframe_list = driver.find_elements_by_tag_name('iframe')
    #print('There are %d iframe in this page: '%(len(iframe_list))) #DEBUG
    
    ## Step 1: click datatype button: 1day, 5days, 1month ... 
    print("Waiting for iframe loading...")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//div[@id="chartholder"]/iframe')))
    target_iframe = driver.find_element_by_xpath('//div[@id="chartholder"]/iframe')
    print("Iframe loaded!")

    driver.switch_to.frame(target_iframe)
    data_type_id = "range5D"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,data_type_id)))
    range_btn = driver.find_element_by_id(data_type_id)

    actions.move_to_element(range_btn).perform()
    
    range_btn.click()
    print("Range option button clicked...")
    ## Check if change data type succeeds
    data_type_xpath = '//li[@id="'+data_type_id+'" and @class="current"]'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,data_type_xpath)))
    print("Iframe corresponds to range option generated!")
    ## step 2: (need to switch to the new iframe) click data table button
    ## Since shown iframe changes after clicking data type button, we should switch to the new iframe
    # driver.switch_to_default_content()
    # new_iframe = driver.find_element_by_xpath('//div[@id="chartholder"]/iframe')
    # driver.switch_to.frame(new_iframe) 

    show_talble_btn = driver.find_element_by_id("dataTableBtn")
    show_talble_btn.click()
    print("Btn found in this frame") #DEBUG

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@id="gridContainer"]//span[contains(text(),"Export To Excel")]')))
    Excel_btn = driver.find_element_by_xpath('//div[@id="gridContainer"]//span[contains(text(),"Export To Excel")]')
    #Excel_btn = driver.find_element_by_xpath('//span[@class="btn"]')
    #actions.move_to_element(Excel_btn).perform()
    Excel_btn.click()
    driver.switch_to_default_content()
    
    ## wait for download to finish 
    file_path = download_dir   + r"\grid.xls"
    while not os.path.exists(file_path):
        time.sleep(1)
    # ## Since setting directory failed and impossible to rename file,
    # ## we rename each file by hand
    command = "ren " + file_path + " " + time_stamp + "_" + stock + ".xls"

    print("Execute command "+ command)
    os.system(command)


if __name__=="__main__":
    time_stamp = time.strftime("%Y-%m-%d", time.gmtime())

    download_dir = r'E:\NASDAQ_test'

    ########### Using Chrome as driver #########
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('test-type')
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    prefs = {
        'download.default_directory': download_dir ,
        "download.prompt_for_download" : False,
    }
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

    #f = open("./NASDQ100.txt", 'r',encoding='utf-8')
    f = open("./failed_list.txt", 'r',encoding='utf-8')
    stock_list = f.read().strip('\n').split(',')

    driver.get("http://www.google.com")
    for stock in stock_list:
        try:
            url = "https://www.nasdaq.com/en/symbol/"+ stock + "/interactive-chart"
            print("Try to GET URL "+ url)
            ScrapeOneStock(driver, url, stock, time_stamp, download_dir)
        except Exception as e:
            print(e)


    driver.quit()  

#except Exception as e:
    #print(e)