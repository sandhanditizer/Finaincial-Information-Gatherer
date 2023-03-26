from DataCollection.scrapeHedgeye import newestHedgeyeData
from DataCollection.scrapeWSJ_Yahoo import newestNasdaqNyseData
from DBControls.hedgeyePrep import add_row as addHedgeye
from DBControls.nasdaqPrep import add_row as addNasdaq
from DBControls.nysePrep import add_row as addNyse
from DBControls.dbReadWrite import Hedgeye, NASDAQ, NYSE
from socket import create_connection
from threading import Thread


# ------------------------------------------------------------------------------
# Functions called while starting up the app or pressing the `Reload` button

def updateHedgeyeTable():
    """
    Grabs data from Hedgeye's website and stores new data in the database.\n
    Returns:\n
        string: Error.\n
        0: If success\n
    """
    
    data = newestHedgeyeData()
    
    if type(data) == str:
        return data # Error
    else:
        try:
            date = data.pop() # Removes date information
            if Hedgeye.getData(date=date) == []: # No data in database for this date - add new data
                for d in data:
                    addHedgeye(date=date, 
                            ticker=d['Ticker'], 
                            description=d['Description'], 
                            buy=d['Buy'], 
                            sell=d['Sell'],
                            close=d['Close']
                            )
        except:
            return 'Cannot load newest Hedgeye data into database.'
        
    return 0 # Successful
        
            
def updateNasdaqNyseTables():
    """
    Grabs data from the Wallstreet Journal Market Diaries and Yahoo websites and stores new data in the database.\n
    Returns:\n
        string: Error.\n
        0: If success\n
    """
    
    data = newestNasdaqNyseData()
    
    if type(data) == str:
        return data # Error
    else:
        try:
            date = data['Date']
            if NASDAQ.getData(date=date) == None: # No data in database for this date - add new data
                addNasdaq(date=date, 
                        advancing_V=data['NASDAQ Advancing Volume'], 
                        declining_V=data['NASDAQ Declining Volume'],
                        close=data['NASDAQ Close'],
                        advances=data['NASDAQ Advances'],
                        declines=data['NASDAQ Declines'], 
                        new_highs=data['NASDAQ New Highs'],
                        new_lows=data['NASDAQ New Lows']
                        )
                
            if NYSE.getData(date=date) == None: # No data in database for this date - add new data
                addNyse(date=date, 
                        advancing_V=data['NYSE Advancing Volume'], 
                        declining_V=data['NYSE Declining Volume'],
                        close=data['NYSE Close'],
                        advances=data['NYSE Advances'],
                        declines=data['NYSE Declines'], 
                        new_highs=data['NYSE New Highs'],
                        new_lows=data['NYSE New Lows']
                        )
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
        
        
def checkWiFiConnection():
    """
    Checks WiFi connection.\n
    Returns:\n
        bool: True = WiFi connected.\n
    """
    try:
        with create_connection(("www.google.com", 80)) as _:
            return True
    except OSError:
        return False
    

def updateDatabase():
    if checkWiFiConnection():
        thread1 = ThreadUpdate(target=updateHedgeyeTable)
        thread2 = ThreadUpdate(target=updateNasdaqNyseTables)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return [thread1.result(), thread2.result()]
    else:
        return 'WiFi is down. Please check your connection.'
    

# ------------------------------------------------------------------------------
# Functions called while interacting with the pages

    
def summonHedgeyeData(date=None, ticker=None, most_recent=True):
    """
    Retrieves data from database in accordance with the request.\n
    If date and not ticker, returns all data associated with that date.\n
    If date and ticker, returns data associated with that date and specific ticker.\n
    If not date and ticker, returns all data for that specific ticker.\n
    If not date and not ticker, grabs data associated with the closest dates data.\n
    Args:\n
        date (string, optional): 'yyyy-mm-dd'. Defaults to None.\n
        ticker (string, optional): 'ABC...Z'. Defaults to None.\n
        most_recent (bool, optional): True = Gets most recent data. Defaults to True.\n
    Returns:\n
        list: List of dictionaries that hold data.\n
    """
    
    if date or ticker:
        most_recent = False
        
    data = []
    results = Hedgeye.getData(date=date, ticker=ticker, most_recent=most_recent)
    
    if results != []:
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
                }
            )
            
            if r.ticker == 'UST10Y':
                tens_close = r.close
            elif r.ticker == 'UST2Y':
                twos_close = r.close
                
        # Calculating the 10s/2s spread on the spot instead of storing them in the database
        data.append({'10s/2s Spread (bps)': round((tens_close - twos_close) * 100, 2)})            
    
    return data


def summonNasdaqData(date=None, most_recent=True):
    """
    Retrieves data from database in accordance with the request.\n
    If date, returns data associated with that specified date.\n
    If not date, grabs data associated with the closest dates data.\n
    Args:\n
        date (string, optional): 'yyyy-mm-dd'. Defaults to None.\n
        most_recent (bool, optional): True = Gets most recent data. Defaults to True.\n
    Returns:\n
        dict: Data.\n
    """
    
    if date:
        most_recent=False

    results = NASDAQ.getData(date=date, most_recent=most_recent)
    
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
    

def summonNyseData(date=None, most_recent=True):
    """
    Retrieves data from database in accordance with the request.\n
    If date, returns data associated with that specified date.\n
    If not date, grabs data associated with the closest dates data.\n
    Args:\n
        date (string, optional): 'yyyy-mm-dd'. Defaults to None.\n
        most_recent (bool, optional): True = Gets most recent data. Defaults to True.\n
    Returns:\n
        dict: Data.\n
    """    

    if date:
        most_recent=False
        
    results = NYSE.getData(date=date, most_recent=most_recent)
    
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