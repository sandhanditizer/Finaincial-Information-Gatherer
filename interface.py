from DataCollection.websiteControllers import HedgeyeWebController, CompositesWebController
from DBControls.hedgeyePrep import add_row as addHedgeyeRow
from DBControls.nasdaqPrep import add_row as addNasdaqRow
from DBControls.nysePrep import add_row as addNyseRow
from DBControls.dbReadWrite import Hedgeye, NASDAQ, NYSE
from socket import create_connection
from threading import Thread
from tzlocal import get_localzone
from datetime import datetime, timedelta
import json


# ------------------------------------------------------------------------------
# Functions called while starting up the app or pressing the `Reload` button

def updateHedgeyeTable():
    """
    Grabs data from Hedgeye's website and stores new data in the database.\n
    Returns:\n
        str: Error.\n
        0: If success
    """
    wc = HedgeyeWebController()
    data = wc.scrapeData()
    
    if type(data) == str:
        return data # Error
    else:
        try:
            date = data.pop() # Removes date information
            for d in data:
                addHedgeyeRow(date=date, ticker=d['Ticker'], description=d['Description'], 
                        buy=d['Buy'], sell=d['Sell'], close=d['Close'])
        except:
            return 'Cannot load newest Hedgeye data into database.'
        
    return 0 # Successful
        
            
def updateNasdaqNyseTables():
    """
    Grabs data from the Wallstreet Journal Market Diaries and Yahoo websites and stores new data in the database.\n
    Returns:\n
        str: Error.\n
        0: If success
    """
    wc = CompositesWebController()
    data = wc.scrapeData()
    
    if type(data) == str:
        return data # Error
    else:
        try:
            date = data['Date']
            addNasdaqRow(date=date, 
                    advancing_V=data['NASDAQ Advancing Volume'], declining_V=data['NASDAQ Declining Volume'],
                    close=data['NASDAQ Close'], advances=data['NASDAQ Advances'], declines=data['NASDAQ Declines'], 
                    new_highs=data['NASDAQ New Highs'], new_lows=data['NASDAQ New Lows'])
                
            addNyseRow(date=date, 
                    advancing_V=data['NYSE Advancing Volume'], declining_V=data['NYSE Declining Volume'],
                    close=data['NYSE Close'], advances=data['NYSE Advances'], declines=data['NYSE Declines'], 
                    new_highs=data['NYSE New Highs'], new_lows=data['NYSE New Lows'])
        except:
            return 'Cannot load newest NYSE or NASDAQ data into database.'
        
    return 0 # Successful


class ThreadUpdate(Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target = target
        self._result = None
        
    def run(self):
        """Runs thread.\n"""
        self._result = self._target()
        
    def result(self):
        """Returns result from threaded function.\n"""
        return self._result
        
        
def WiFiConnection():
    """
    Checks WiFi connection.\n
    Returns:\n
        bool: True = WiFi connected.
    """
    try:
        with create_connection(("www.google.com", 80)) as _:
            return True
    except OSError:
        return False
    

def updateDatabase():
    """
    Requests data from websites and handles errors for backend side.\n
    Returns:\n
        list: If [0,0] total success, if either 0 is a message then that message is an error that will be displayed.
    """
    current_time = datetime.now(get_localzone()) # Gets the time of where the computer is
    todays_date = datetime.strftime(current_time.date(), '%Y-%m-%d')
    yesterdays_date = datetime.strftime(current_time.date() - timedelta(days=1), '%Y-%m-%d')
    j1, j2 = False, False
    
    if WiFiConnection():
        if todays_date != Hedgeye.getAllDates()[-1]:
            thread1 = ThreadUpdate(target=updateHedgeyeTable)
            thread1.start()
            j1 = True

        if NASDAQ.getData(date=yesterdays_date) == None or (current_time.hour > 16 and NASDAQ.getData(date=todays_date) == None):
            thread2 = ThreadUpdate(target=updateNasdaqNyseTables)
            thread2.start()
            j2 = True

        if j1 and j2:
            thread1.join()
            thread2.join()
            return [thread1.result(), thread2.result()]
        elif j1 and not j2:
            thread1.join()
            return [thread1.result(), 0]   
        elif not j1 and j2:
            thread2.join()
            return [0, thread2.result()]   
        else:
            return [0, 0]
        
    else:
        return 'WiFi is down. Please check your connection.'


# ------------------------------------------------------------------------------
# Functions called while interacting with the pages

    
def summonHedgeyeData(date=None, ticker=None, all_dates=False):
    """
    Gets desired data from database and formats it for GUI use.
    Reference the Hedgeye class in dbReadWrite.py for how getData is used.\n
    Args:\n
        date (str, optional): 'yyyy-mm-dd'. Defaults to None.\n
        ticker (str, optional): 'ABC...Z'. Defaults to None.\n
        all_dates (bool, optional): If true, will get all unique dates in database. Defaults to False.\n
    Returns:\n
        list: List of dictionaries with data.
    """
    if all_dates:
        return Hedgeye.getAllDates()
        
    data = []
    results = Hedgeye.getData(date=date, ticker=ticker)
    
    if type(results) == list:
        tens_close = 0
        twos_close = 0
        
        for r in results:
            data.append(
                {'Date': r.date,
                 'Ticker': r.ticker,
                 'Description': r.description,
                 'Buy': r.buy,
                 'Sell': r.sell,
                 'Close': r.close,
                 'W/W Delta': r.delta_ww,
                 '1-Day Delta (%)': r.od_delta,
                 '1-Week Delta (%)': r.ow_delta,
                 '1-Month Delta (%)': r.om_delta,
                 '3-Month Delta (%)': r.tm_delta,
                 '6-Month Delta (%)': r.sm_delta,
                 '1-Year Delta (%)': r.oy_delta,
                 'Range Asym - Buy (%)': r.ra_buy,
                 'Range Asym - Sell (%)': r.ra_sell
                })
            
            if r.ticker == 'UST10Y':
                tens_close = r.close
            elif r.ticker == 'UST2Y':
                twos_close = r.close
                
        # Calculating the 10s/2s spread on the spot instead of storing them in the database
        data.append({'10s/2s Spread (bps)': round((tens_close - twos_close) * 100, 2)})      
    else:
        data.append(
            {'Date': results.date,
                'Ticker': results.ticker,
                'Description': results.description,
                'Buy': results.buy,
                'Sell': results.sell,
                'Close': results.close,
                'W/W Delta': results.delta_ww,
                '1-Day Delta (%)': results.od_delta,
                '1-Week Delta (%)': results.ow_delta,
                '1-Month Delta (%)': results.om_delta,
                '3-Month Delta (%)': results.tm_delta,
                '6-Month Delta (%)': results.sm_delta,
                '1-Year Delta (%)': results.oy_delta,
                'Range Asym - Buy (%)': results.ra_buy,
                'Range Asym - Sell (%)': results.ra_sell
            })              
    
    return data


def summonNasdaqData(date=None, all_dates=False):
    """
    Gets desired data from database and formats it for GUI use.
    Reference the NASDAQ class in dbReadWrite.py for how getData is used.\n
    Args:\n
        date (str, optional): 'yyyy-mm-dd'. Defaults to None.\n
        all_dates (bool, optional): If true, will get all unique dates in database. Defaults to False.\n
    Returns:\n
        dict: Data.
    """
    if all_dates:
        return NASDAQ.getAllDates()

    results = NASDAQ.getData(date=date)
    
    if results:
        return {
            'Date': results.date,
            'Advancing Volume': results.advancing_V,
            'Declining Volume': results.declining_V,
            'Total Volume': results.total_V,
            'Volume Delta (%)': results.delta_V,
            'Close (%)': results.close,
            'Upside Day (%)': results.upside_day,
            'Downside Day (%)': results.downside_day,
            'Advances': results.advances,
            'Declines': results.declines,
            'Net (Advances/Declines)': results.net_ad,
            '10-Day Breakaway Momentum': results.td_breakaway,
            '20-Day Breakaway Momentum': results.Td_breakaway,
            'Advance/Decline Ratio': results.ad_ratio,
            'Advance/Decline Thrust (%)': results.ad_thrust,
            '5-Day Advance/Decline Thrust (%)': results.fd_ad_thrust,
            '5-Day Up/Down Volume Thrust (%)': results.fd_ud_V_thrust,
            'New Highs': results.new_highs,
            'New Lows': results.new_lows,
            'Net (Highs/Lows)': results.net_hl,
            '21-Day Average (Highs/Lows)': results.tod_avg,
            '63-Day Average (Highs/Lows)': results.std_avg
        }
    else:
        return results # Error
    

def summonNyseData(date=None, all_dates=False):
    """
    Gets desired data from database and formats it for GUI use.
    Reference the NYSE class in dbReadWrite.py for how getData is used.\n
    Args:\n
        date (str, optional): 'yyyy-mm-dd'. Defaults to None.\n
        all_dates (bool, optional): If true, will get all unique dates in database. Defaults to False.\n
    Returns:\n
        dict: Data.
    """
    if all_dates:
        return NYSE.getAllDates()
        
    results = NYSE.getData(date=date)
    
    if results:
        return {
            'Date': results.date,
            'Advancing Volume': results.advancing_V,
            'Declining Volume': results.declining_V,
            'Total Volume': results.total_V,
            'Volume Delta (%)': results.delta_V,
            'Close (%)': results.close,
            'Upside Day (%)': results.upside_day,
            'Downside Day (%)': results.downside_day,
            'Advances': results.advances,
            'Declines': results.declines,
            'Net (Advances/Declines)': results.net_ad,
            '10-Day Breakaway Momentum': results.td_breakaway,
            '20-Day Breakaway Momentum': results.Td_breakaway,
            'Advance/Decline Ratio': results.ad_ratio,
            'Advance/Decline Thrust (%)': results.ad_thrust,
            '5-Day Advance/Decline Thrust (%)': results.fd_ad_thrust,
            '5-Day Up/Down Volume Thrust (%)': results.fd_ud_V_thrust,
            'New Highs': results.new_highs,
            'New Lows': results.new_lows,
            'Net (Highs/Lows)': results.net_hl,
            '21-Day Average (Highs/Lows)': results.tod_avg,
            '63-Day Average (Highs/Lows)': results.std_avg
        }
    else:
        return results # Error
    
    
def getCredentials():
    """
    Gets and returns current username and password from config.json.
    """
    with open('DataCollection/config.json', 'r') as f:
        login_payload = json.load(f)
        return [login_payload['Payload'][0]['username'], login_payload['Payload'][0]['password']]


def setCredentials(username=None, password=None):
    """
    Given a username and/or password, will change the credentials inside of config.json.\n
    Args:\n
        username (str, optional):  Defaults to None.\n
        password (str, optional):  Defaults to None.
    """
    # Get
    with open('DataCollection/config.json', 'r') as f:
        login_payload = json.load(f)

    # Change
    if username and password:
        login_payload['Payload'][0]['username'] = username
        login_payload['Payload'][0]['password'] = password
        
    elif username and not password:
        login_payload['Payload'][0]['username'] = username
        
    elif not username and password:
        login_payload['Payload'][0]['password'] = password
       
    # Set 
    with open('DataCollection/config.json', 'w') as f:
        json.dump(login_payload, f)
        