from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.format import cleanData, reformatData, reformatDate
from contextlib import contextmanager
import json


@contextmanager
def getDriver():
    """
    Creates a Selenium driver based on the available browser options (Edge, Firefox, and Chrome only).\n
    Returns:\n
        selenium.webdriver
    """
    browsers_supported = {
        'firefox': {
            'driver': webdriver.Firefox,
            'options': webdriver.FirefoxOptions,
            'headless': '-headless'
        },
        'edge': {
            'driver': webdriver.Edge,
            'options': webdriver.EdgeOptions,
            'headless': '--headless=new'
        },
        'chrome': {
            'driver': webdriver.Chrome,
            'options': webdriver.ChromeOptions,
            'headless': '--headless=new'
        }
    }

    driver = None
    for _, browser_options in browsers_supported.items():
        try:
            options = browser_options['options']()
            options.add_argument(browser_options['headless']) # Prevents browser pop-up
            driver = browser_options['driver'](options=options)
            break # Stop after the first successful driver creation
        except:
            pass

    if driver is None:
        raise ValueError('Available webdriver browsers are Edge, Firefox, and Chrome.')

    try:
        yield driver
    finally:
        driver.quit()


def createWaitDriver(driver):
    """
    Creates a driver that waits a maximum of 10 seconds, then moves forward to next operation. 
    For ensuring the website loads correctly.
    """
    return WebDriverWait(driver, 10)


# -------------------------------------------------------------------------------------------------
# Hedgeye wbsite controller functions
    
def login(driver, RISK_RANGE_SIGNALS_URL):
    """
    Attempts to log into the Hedgeye website.\n
    Args:\n
        driver (webdriver): Browser driver to be logged into.\n
        RISK_RANGE_SIGNALS_URL (str): URL to goto after login.\n
    Returns:\n
        selenium.webdriver: If success, returns logged in webdriver.\n
        string: If failure, returns appropriate error message.
    """
    driver.get('https://accounts.hedgeye.com/users/sign_in') # Goto login webpage
    
    with open('DataCollection/config.json', 'r') as f:
        login_payload = json.load(f)

    try:
        email_field = driver.find_element(By.ID, 'user_email') # Finds email field on website
        email_field.send_keys(login_payload['Payload'][0]['username']) # Puts email address into field

        password_field = driver.find_element(By.ID, 'user_password') # Finds password field on website
        password_field.send_keys(login_payload['Payload'][0]['password']) # Puts password into field

        password_field.send_keys(Keys.RETURN) # Submits the login form
    except:
        return 'An error occured while trying to enter Hedgeye credentials into user fields. Contact your son for support.'
    
    if RISK_RANGE_SIGNALS_URL.find('hedgeye') == -1:
        return 'Not a Hedgeye URL. Please backlog with a proper Hedgeye risk range signals URL. All archived risk range signal data can be found here:\n\nhttps://app.hedgeye.com/research_archives?with_category=33-risk-range-signals'
    
    if RISK_RANGE_SIGNALS_URL.find('feed_items') == -1:
        return 'Invalid risk range signals URL. Please visit:\n\nhttps://app.hedgeye.com/research_archives?with_category=33-risk-range-signals\n\nand select a risk range signals data page by what date you desire to backlog.'
    
    driver.get(RISK_RANGE_SIGNALS_URL) # Goto webpage that has the data we want
    
    if driver.current_url != RISK_RANGE_SIGNALS_URL:
        return "Couldn't navigate to risk range signals page. Go into settings and make sure that your credentials are correct, then press `Reload Data`."

    return driver


def fetchHedgeyeData(RISK_RANGE_SIGNALS_URL):
    """
    Requests newest data from Hedgeye website and returns the data clean and formatted.\n
    Args:\n
        RISK_RANGE_SIGNALS_URL (str): URL to goto after login.\n
    Returns:\n
        list(dict): A list of dictionaries that holds information about each ticker in the risk range signals table.
    """
    with getDriver() as driver:
        logged_in_driver = login(driver, RISK_RANGE_SIGNALS_URL)
        if isinstance(logged_in_driver, str):
            return logged_in_driver # Return error message from login()

        try:                
            wait_driver = createWaitDriver(logged_in_driver)
            raw_date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "teaser_feed_item_")]/div[1]/time/span[2]'))).get_attribute('textContent')
            raw_table_data = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mid-col"]/div/div[1]/div/article/div/div[2]/table'))).get_attribute('textContent')
        except:
            return "Hedgeye's main page changed, you will have to backlog today's data. Please visit:\n\nhttps://app.hedgeye.com/research_archives?with_category=33-risk-range-signals\n\nand select a risk range signals data page by what date you desire to backlog."

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
    """
    Requests newest WSJ market diary data for the NASDAQ and NYSE.\n
    Args:\n
        driver (webdriver): Webdriver used to navigate to page and collect data.\n
    Returns:\n
        dict: Raw data.
    """
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
    """
    Fetches the newest close data for either NYSE or NASDAQ.\n
    Args:
        driver (webdriver): Webdriver used to navigate to page and collect data.\n
        current_date (str): Date in format yyyy-mm-dd that is needed for calculation the correct close.\n
        target_url (str): URL for what website to get close data from (yahoo finance).\n
        market_name (str): Either NASDAQ or NYSE.\n
    Returns:\n
        dict: Raw data.
    """
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
    """
    Fetches market diary and close data, cleans the raw data, and returns a dictionary of data.\n
    Returns:\n
        dict: Clean data.\n
        str: Error message.
    """
    with getDriver() as driver:
        md_raw_data = fetchMarketDiaryData(driver)
        if isinstance(md_raw_data, str):
            return md_raw_data
        
        nasdaq_close_raw_data = fetchCloseData(driver, md_raw_data['Date'], 'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC', 'NASDAQ')
        if isinstance(nasdaq_close_raw_data, str):
            return nasdaq_close_raw_data
        
        nyse_close_raw_data = fetchCloseData(driver, md_raw_data['Date'], 'https://finance.yahoo.com/quote/%5ENYA/history?p=%5ENYA', 'NYSE')
        if isinstance(nyse_close_raw_data, str):
            return nyse_close_raw_data
    
    consolidated_raw_data = {**md_raw_data, **nasdaq_close_raw_data, **nyse_close_raw_data} # Merge dictionaries
    
    try:
        return cleanData(consolidated_raw_data)
    except:
        return 'Cannot properly clean Market Diary and Yahoo Finance data. Contact your son for support.'