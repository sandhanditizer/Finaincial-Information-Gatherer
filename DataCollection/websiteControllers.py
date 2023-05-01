from selenium.webdriver import FirefoxOptions, Firefox, ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.format import clean, extract, formatDate
import json


def getDriver():
    """
    Creates a selenium driver based on what browser you have. Availible drivers are Firefox and Chrome only.\n
    Returns:\n
        Webdriver
    """
    try:
        options = FirefoxOptions()
        options.add_argument('-headless') # Prevents browser pop-up
        return Firefox(options=options)
    except:
        pass
    
    try:
        options = ChromeOptions()
        options.add_argument('-headless') # Prevents browser pop-up
        return Chrome(options=options)
    except:
        # If user doesnt have either three, throw error
        raise ValueError('Available webdriver browsers are Firefox and Chrome.')


class HedgeyeWebController:
    def __init__(self):
        self._driver = getDriver()
        self._logged_in_driver = self._login()
        
    
    def _createWaitDriver(self, driver):
        """Creates a driver that waits a maximum of 10 seconds for the website to load correctly."""
        return WebDriverWait(driver, 10) 
        
        
    def _login(self):
        """
        Attemps to logs into the Hedgeye website.\n
        Returns:\n
            selenium.webdriver: If success.\n
            string: If failure.
        """
        try:
            LOGIN_URL = 'https://accounts.hedgeye.com/users/sign_in'
            self._driver.get(LOGIN_URL)
            
            with open('DataCollection/config.json', 'r') as f:
                login_payload = json.load(f)

            # Finds the email and password fields, and enter login credentials
            email_field = self._driver.find_element(By.ID, 'user_email')
            email_field.send_keys(login_payload['Payload'][0]['username'])

            password_field = self._driver.find_element(By.ID, 'user_password')
            password_field.send_keys(login_payload['Payload'][0]['password'])

            # Submits the login form
            password_field.send_keys(Keys.RETURN)
            
            return self._driver
        except:
            return "Cannot log into Hedgeye's website. Contact your son for support."
        

    def scrapeData(self):
        """
        Requests newest data from Hedgeye website and returns the data clean and formated.\n
        Returns:\n
            list: Data.
        """
        if type(self._logged_in_driver) == str:
            self._driver.quit()
            return self._logged_in_driver

        try:
            RISK_RANGE_SIGNALS_URL = 'https://app.hedgeye.com/feed_items/all?page=1&with_category=33-risk-range-signals'
            self._logged_in_driver.get(RISK_RANGE_SIGNALS_URL)
            
            # Make second request in case of error
            if self._logged_in_driver.current_url != RISK_RANGE_SIGNALS_URL:
                self._logged_in_driver.get(RISK_RANGE_SIGNALS_URL)
                
            wait_driver = self._createWaitDriver(self._logged_in_driver)

            rrs_table = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mid-col"]/div/div[1]/div/article/div/div[2]/table'))).get_attribute('textContent')
            date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "teaser_feed_item_")]/div[1]/time/span[2]'))).get_attribute('textContent')
        except:
            return "Cannot grab risk range data from Hedgeye's website. Website page has changed to something unrecognizable."
        finally:
            self._logged_in_driver.quit()
            
        try:
            data = extract(rrs_table) # Formats data returns a list of dictionaries
        except:
            return "Cannot properly extract Hedgeye's table data. Contact your son for support."
        
        try:
            formated_date = formatDate(date)
        except:
            return "Cannot properly format Hedgeye's date data. Contact your son for support."
            
        data.append(formated_date)
        return data
    
    
# -------------------------------------------------------------------------------------------------


class CompositesWebController:
    def __init__(self):
        self._driver = getDriver()
        self._data = {}
    
    
    def _createWaitDriver(self, driver):
        """Creates a driver that waits a maximum of 10 seconds for the website to load correctly.\n"""
        return WebDriverWait(driver, 10) 
    
    
    def _getMarketDiaryData(self):   
        try:                
            MARKET_DIARY_URL = 'https://www.wsj.com/market-data/stocks/marketsdiary'
            self._driver.get(MARKET_DIARY_URL) # No login needed
            
            wait_driver = self._createWaitDriver(self._driver)

            date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[1]/h3/span[2]'))).get_attribute('textContent')
            self._data['Date'] = formatDate(date)
            
            self._data['NYSE Advancing Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[12]/td[2]'))).get_attribute('textContent')
            self._data['NYSE Declining Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[13]/td[2]'))).get_attribute('textContent')
            self._data['NYSE Advances'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]'))).get_attribute('textContent')
            self._data['NYSE Declines'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]'))).get_attribute('textContent')
            self._data['NYSE New Highs'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[5]/td[2]'))).get_attribute('textContent')
            self._data['NYSE New Lows'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[6]/td[2]'))).get_attribute('textContent')
            
            self._data['NASDAQ Advancing Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[9]/td[2]'))).get_attribute('textContent')
            self._data['NASDAQ Declining Volume'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[10]/td[2]'))).get_attribute('textContent')
            self._data['NASDAQ Advances'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]'))).get_attribute('textContent')
            self._data['NASDAQ Declines'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]'))).get_attribute('textContent')
            self._data['NASDAQ New Highs'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[5]/td[2]'))).get_attribute('textContent')
            self._data['NASDAQ New Lows'] = wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[6]/td[2]'))).get_attribute('textContent')
        except:
            return 'Cannot scrape NASDAQ or NYSE composite data from WSJ Market Diary page. Website page has changed to something unrecognizable.'
            
            
    def _getCloseData(self): 
        try:           
            NYSE_CLOSE_URL = 'https://finance.yahoo.com/quote/%5ENYA/history?p=%5ENYA'
            self._driver.get(NYSE_CLOSE_URL)
            
            wait_driver = self._createWaitDriver(self._driver)
                
            row = 1
            while row != 4: # Search for the correct close data given the date from the WSJ market diaries page
                xpath = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[1]/span'
                date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute('textContent')
                if formatDate(date) != self._data['Date']:
                    row += 1
                else:
                    break
            
            xpath_new_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[5]/span'
            new_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_new_close))).get_attribute('textContent')
            
            xpath_old_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row + 1}]/td[5]/span'
            old_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_old_close))).get_attribute('textContent')
            
            self._data['NYSE Close'] = round(((float(new_close.replace(',', '')) - float(old_close.replace(',', ''))) / float(old_close.replace(',', ''))) * 100, 2)
            
            # -------------------------

            NASDAQ_CLOSE_URL = 'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC'
            self._driver.get(NASDAQ_CLOSE_URL)
            
            wait_driver = self._createWaitDriver(self._driver)
            
            row = 1
            while row != 4: # Search for the correct close data given the date from the WSJ market diaries page
                xpath = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[1]/span'
                date = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute('textContent')
                if formatDate(date) != self._data['Date']:
                    row += 1
                else:
                    break
            
            xpath_new_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[5]/span'
            new_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_new_close))).get_attribute('textContent')
            
            xpath_old_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row + 1}]/td[5]/span'
            old_close = wait_driver.until(EC.visibility_of_element_located((By.XPATH, xpath_old_close))).get_attribute('textContent')
            
            self._data['NASDAQ Close'] = round(((float(new_close.replace(',', '')) - float(old_close.replace(',', ''))) / float(old_close.replace(',', ''))) * 100, 2)
            
        except:
            return 'Cannot scrape NASDAQ or NYSE composite close data from Yahoo Finance Quote pages. Website page has changed to something unrecognizable.'
            
            
    def scrapeData(self):
        ans1 = self._getMarketDiaryData()
        ans2 = self._getCloseData()
        self._driver.quit()
        
        if ans1:
            return ans1
        elif ans2:
            return ans2
        
        try:
            formated_data = clean(self._data) # Formats data how I want it
        except:
            return 'Cannot properly clean Market Diary and Yahoo data. Contact your son for support.'
            
        return formated_data