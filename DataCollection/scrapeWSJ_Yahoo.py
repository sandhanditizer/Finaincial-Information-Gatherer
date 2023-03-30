from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.helperFunctions import getDriver, clean, formatDate


def newestNasdaqNyseData():
    data = {}
    
    try:
        TARGET_URL = 'https://www.wsj.com/market-data/stocks/marketsdiary'
        
        try:
            WSJ_driver = getDriver('Firefox')
        except:
            WSJ_driver = getDriver('Edge')
            
        WSJ_driver.get(TARGET_URL) # No login needed
        
        # Waits a maximum of 30 sec for the website to load correctly
        wait = WebDriverWait(WSJ_driver, 30) 
        
        date = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[1]/h3/span[2]'))).get_attribute('textContent')
        data['Date'] = formatDate(date)
        
        data['NYSE Advancing Volume'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[12]/td[2]'))).get_attribute('textContent')
        data['NYSE Declining Volume'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[13]/td[2]'))).get_attribute('textContent')
        data['NYSE Advances'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]'))).get_attribute('textContent')
        data['NYSE Declines'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]'))).get_attribute('textContent')
        data['NYSE New Highs'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[5]/td[2]'))).get_attribute('textContent')
        data['NYSE New Lows'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[1]/tr[6]/td[2]'))).get_attribute('textContent')
        
        data['NASDAQ Advancing Volume'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[9]/td[2]'))).get_attribute('textContent')
        data['NASDAQ Declining Volume'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[10]/td[2]'))).get_attribute('textContent')
        data['NASDAQ Advances'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]'))).get_attribute('textContent')
        data['NASDAQ Declines'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]'))).get_attribute('textContent')
        data['NASDAQ New Highs'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[5]/td[2]'))).get_attribute('textContent')
        data['NASDAQ New Lows'] = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/table/tbody[2]/tr[6]/td[2]'))).get_attribute('textContent')
    except:
        return 'Cannot scrape NASDAQ or NYSE data from WSJ Market Diary page.'
    finally:
        WSJ_driver.quit()
        
    try:
        try:
            close_driver = getDriver('Firefox')
        except:
            close_driver = getDriver('Edge')
        
        # Waits a maximum of 30 sec for the website to load correctly
        wait = WebDriverWait(close_driver, 30) 
        
        NYSE_CLOSE_TARGET_URL = 'https://finance.yahoo.com/quote/%5ENYA/history?p=%5ENYA'
        close_driver.get(NYSE_CLOSE_TARGET_URL)
               
        row = 1
        while True: # Search for the correct close data given the date from the WSJ market diaries page
            xpath = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[1]/span'
            date = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath))).get_attribute('textContent')
            if formatDate(date) != data['Date']:
                row += 1
            else:
                break
        
        xpath_new_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[5]/span'
        new_close = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_new_close))).get_attribute('textContent')
        
        xpath_old_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row + 1}]/td[5]/span'
        old_close = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_old_close))).get_attribute('textContent')
        
        data['NYSE Close'] = round(((float(new_close.replace(',', '')) - float(old_close.replace(',', ''))) / float(old_close.replace(',', ''))) * 100, 2)
        
        # -------------------------

        NASDAQ_CLOSE_TARGET_URL = 'https://finance.yahoo.com/quote/%5EIXIC/history?p=%5EIXIC'
        close_driver.get(NASDAQ_CLOSE_TARGET_URL)
        
        row = 1
        while True: # Search for the correct close data given the date from the WSJ market diaries page
            xpath = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[1]/span'
            date = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath))).get_attribute('textContent')
            if formatDate(date) != data['Date']:
                row += 1
            else:
                break
        
        xpath_new_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row}]/td[5]/span'
        new_close = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_new_close))).get_attribute('textContent')
        
        xpath_old_close = f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{row + 1}]/td[5]/span'
        old_close = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_old_close))).get_attribute('textContent')
        
        data['NASDAQ Close'] = round(((float(new_close.replace(',', '')) - float(old_close.replace(',', ''))) / float(old_close.replace(',', ''))) * 100, 2)
        
    except:
        return 'Cannot scrape NASDAQ or NYSE close data from Yahoo Finance Quote pages.'
    finally: 
        close_driver.quit()
        
    try:
        datafinal = clean(data) # Formats data how I want it
    except:
        return 'Cannot properly clean WSJ/Yahoo data.'
        
    return datafinal