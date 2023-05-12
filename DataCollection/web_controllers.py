from selenium.webdriver import FirefoxOptions, Firefox, ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.format import cleanData, reformatData, reformatDate
import json


def getDriver():
    """
    Creates a Selenium driver based on the available browser options (Firefox and Chrome only).\n
    Returns:\n
        selenium.webdriver
    """
    browsers_supported = {
        'firefox': {
            'driver': Firefox,
            'options': FirefoxOptions
        },
        'chrome': {
            'driver': Chrome,
            'options': ChromeOptions
        }
    }

    for _, browser_options in browsers_supported.items():
        try:
            options = browser_options['options']()
            options.add_argument('-headless') # Prevents browser pop-up
            return browser_options['driver'](options=options)
        except:
            pass
    
    raise ValueError('Available webdriver browsers are Firefox and Chrome.') # User does not have either browser


def createWaitDriver(driver):
    """
    Creates a driver that waits a maximum of 10 seconds, then moves forward to next operation. 
    For ensuring the website loads correctly.
    """
    return WebDriverWait(driver, 10)


# -------------------------------------------------------------------------------------------------
# Hedgeye wbsite controller functions
    
def login():
    """
    Attempts to log into the Hedgeye website.\n
    Returns:\n
        selenium.webdriver: If success, returns logged in webdriver.\n
        string: If failure, returns appropriate error message.
    """
    LOGIN_URL = 'https://accounts.hedgeye.com/users/sign_in'
    driver = getDriver()
    driver.get(LOGIN_URL) # Goto login webpage
    
    with open('DataCollection/config.json', 'r') as f:
        login_payload = json.load(f)

    email_field = driver.find_element(By.ID, 'user_email') # Finds email field on website
    email_field.send_keys(login_payload['Payload'][0]['username']) # Puts email address into field

    password_field = driver.find_element(By.ID, 'user_password') # Finds password field on website
    password_field.send_keys(login_payload['Payload'][0]['password']) # Puts password into field

    password_field.send_keys(Keys.RETURN) # Submits the login form
    
    RISK_RANGE_SIGNALS_URL = 'https://app.hedgeye.com/feed_items/all?page=1&with_category=33-risk-range-signals'
    driver.get(RISK_RANGE_SIGNALS_URL) # Goto webpage that has the data we want
    
    if driver.current_url != RISK_RANGE_SIGNALS_URL:
        driver.quit()
        return "Cannot log into Hedgeye's website. Go into settings and make sure that your username and password are correct."

    return driver


def fetchHedgeyeData():
    """
    Requests newest data from Hedgeye website and returns the data clean and formatted.\n
    Returns:\n
        list(dict): A list of dictionaries that holds information about each ticker in the risk range signals table.
    """
    logged_in_driver = login()
    if isinstance(logged_in_driver, str):
        return logged_in_driver # Return error message from login()

    try:                
        wait_driver = createWaitDriver(logged_in_driver)
        raw_date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "teaser_feed_item_")]/div[1]/time/span[2]'))).get_attribute('textContent')
        raw_table_data = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mid-col"]/div/div[1]/div/article/div/div[2]/table'))).get_attribute('textContent')
    except:
        return "Cannot grab date or risk range data from Hedgeye's website. Website page has changed to something unrecognizable."
    finally:
        logged_in_driver.quit()

    hedgeye_data = []
    try:
        hedgeye_data.append(reformatDate(raw_date)) # Ensures data is in format yyyy-mm-dd
    except:
        return "Cannot properly format Hedgeye's date data. Contact your son for support."
    
    try:
        hedgeye_data.append(reformatData(raw_table_data)) # Data transforms from a string to a ordered list of dictionaries
    except:
        return "Cannot properly extract Hedgeye's table data. Contact your son for support."
    
    return hedgeye_data
    
    
# -------------------------------------------------------------------------------------------------
# Composites web controller functions
    
def fetchMarketDiaryData(driver):
    raw_data = {}
    try:         
        MARKET_DIARY_URL = 'https://www.wsj.com/market-data/stocks/marketsdiary'
        driver.get(MARKET_DIARY_URL) # Goto specified webpage
        
        wait_driver = createWaitDriver(driver)

        raw_date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[1]/h3/span[2]'))).get_attribute('textContent')
        raw_data['Date'] = reformatDate(raw_date)
        
        raw_data['NYSE Advancing Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[12]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE Declining Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[13]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE Total Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[14]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE Advances'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE Declines'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE New Highs'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[5]/td[2]'))).get_attribute('textContent')
        raw_data['NYSE New Lows'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[6]/td[2]'))).get_attribute('textContent')
        
        raw_data['NASDAQ Advancing Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[9]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ Declining Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[10]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ Total Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[11]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ Advances'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ Declines'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ New Highs'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[5]/td[2]'))).get_attribute('textContent')
        raw_data['NASDAQ New Lows'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[6]/td[2]'))).get_attribute('textContent')
    except:
        return 'Cannot scrape NASDAQ or NYSE composite data from WSJ Market Diary page. Website page has changed to something unrecognizable.'
    
    return raw_data        


def fetchCloseData(driver, current_date, target_url, market_name):
    raw_data = {}
    try:           
        driver.get(target_url)
        
        wait_driver = createWaitDriver(driver)
            
        row = 1
        while row != 4: # Searches for current_date close and current_day - 1 close info
            xpath = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[1]/span'
            date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute('textContent')
            if reformatDate(date) != current_date:
                row += 1
            else:
                break
        
        xpath_new_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[5]/span'
        new_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_new_close))).get_attribute('textContent')
        
        xpath_old_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row + 1}]/td[5]/span'
        old_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_old_close))).get_attribute('textContent')
        
        raw_data[f'{market_name} Close'] = round(((cleanData(new_close) - cleanData(old_close)) / cleanData(old_close)) * 100, 2)
    except:
        return f'Cannot scrape {market_name} composite close data from Yahoo Finance Quote pages. Website page has changed to something unrecognizable.'
    
    return raw_data


def fetchCompositeData():
    driver = getDriver()
    md_raw_data = fetchMarketDiaryData(driver)
    nasdaq_close_raw_data = fetchCloseData(driver, md_raw_data['Date'], 'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC', 'NASDAQ')
    nyse_close_raw_data = fetchCloseData(driver, md_raw_data['Date'], 'https://finance.yahoo.com/quote/%5ENYA/history?p=%5ENYA', 'NYSE')
    driver.quit()
    
    if type(md_raw_data) == str:
        return md_raw_data
    elif type(nasdaq_close_raw_data) == str:
        return nasdaq_close_raw_data
    elif type(nyse_close_raw_data) == str:
        return nyse_close_raw_data
    
    consolidated_raw_data = {**md_raw_data, **nasdaq_close_raw_data, **nyse_close_raw_data} # Merge dictionaries
    
    try:
        return cleanData(consolidated_raw_data)
    except:
        return 'Cannot properly clean Market Diary and Yahoo Finance data. Contact your son for support.'