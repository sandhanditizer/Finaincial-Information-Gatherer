from DBControls.dbReadWrite import Hedgeye
from datetime import datetime, timedelta


def compute_delta_ww(date, ticker, today_buy, today_sell):
    """
    Calculates the week over week delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        today_buy (float): Price.\n
        today_sell (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(7, 50):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data:
            return round((today_buy - today_sell) - (old_data.buy - old_data.sell), 2)
        
        if old_data == None and i == 49:
            return None
    
        
def compute_od_delta(date, ticker, close):
    """
    Calculates 1-day delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(1, 50):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 1-Day Delta calculation.\n')
        
        if old_data == None and i == 49: 
            return None
       
        
def compute_ow_delta(date, ticker, close):
    """
    Calculates 1-week delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(7, 50):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 1-Week Delta calculation.\n')
        
        if old_data == None and i == 49:
            return None
        
        
def compute_om_delta(date, ticker, close):
    """
    Calculates 1-month delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """    

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(30, 50):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 1-Month Delta calculation.\n')
        
        if old_data == None and i == 49:
            return None
        

def compute_tm_delta(date, ticker, close):
    """
    Calculates 3-month delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(90, 150):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 3-Month Delta calculation.\n')
        
        if old_data == None and i == 149:
            return None
        
        
def compute_sm_delta(date, ticker, close):
    """
    Calculates 6-month delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(180, 250):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 6-Month Delta calculation.\n')
        
        if old_data == None and i == 249:
            return None
        

def compute_oy_delta(date, ticker, close):
    """
    Calculates 1-year delta.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        close (float): Price.\n
    Returns:\n
        float: If calculation can be performed.\n
        None: If calculation cannot be performed.\n
    """
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(365, 400):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
        if old_data and old_data.close != 0:
            return round(((close - old_data.close) / old_data.close) * 100, 2)
        
        if old_data and old_data.close == 0:
            raise ZeroDivisionError('Close value is 0. Cannot complete 1-Year Delta calculation.\n')
        
        if old_data == None and i == 399:
            return None
        

def compute_ra_buy(buy, close):
    """
    Calculates range asymmetry buy.\n
    Args:\n
        buy (float): Price.\n
        close (float): Price.\n
    Returns:\n
        float: Result.\n
    """
    
    if close == 0:
        raise ZeroDivisionError('Close value is 0. Cannot complete Range Asymmetry Buy calculation.\n')
    
    return round(((buy - close) / close) * 100, 2)


def compute_ra_sell(sell, close):
    """
    Calculates range asymmetry sell.\n
    Args:\n
        sell (float): Price.\n
        close (float): Price.\n
    Returns:\n
        float: Result.\n
    """
    
    if close == 0:
        raise ZeroDivisionError('Close value is 0. Cannot complete Range Asymmetry Sell calculation.\n')
    
    return round(((sell - close) / close) * 100, 2)
        

def add_row(date, ticker, description, buy, sell, close):
    """
    Given the data from the Hedgeye website, makes a few different calculations and then adds them to the database.\n
    Args:\n
        date (string): 'yyyy-mm-dd'.\n
        ticker (string): 'ABC...Z'.\n
        description (string): Description of ticker name.\n
        buy (float): Price.\n
        sell (float): Price.\n
        close (float): Price.\n
    Returns:\n
        int: 0 = success, 1 = failure.\n
    """
    
    if type(date) != str or type(ticker) != str or type(description) != str:
        raise TypeError('Date, ticker, or description has a non-string type.\n')
    
    if not isinstance(buy, (int, float)) or not isinstance(sell, (int, float)) or not isinstance(close, (int, float)):
        raise TypeError('Buy, sell, or close has a non-float or integer type.\n')
    
    if date == '' or ticker == '' or description == '':
        raise TypeError('Date, ticker, or description is an empty string.\n')
    
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            ValueError('Date is not in the correct formate of yyyy-mm-dd.\n')
            
    if close == 0: # Prevents future errors
        raise ZeroDivisionError('Close value is 0. Cannot add new row to Hedgeye table.\n')
    
    
    if Hedgeye.getData(date=date, ticker=ticker) == None: # Prevents duplicating data
        weekweek = compute_delta_ww(date, ticker, buy, sell)
        oneday = compute_od_delta(date, ticker, close)
        oneweek = compute_ow_delta(date, ticker, close)
        onemonth = compute_om_delta(date, ticker, close)
        threemonth = compute_tm_delta(date, ticker, close)
        sixmonth = compute_sm_delta(date, ticker, close)
        oneyear = compute_oy_delta(date, ticker, close)
        rab = compute_ra_buy(buy, close)
        ras = compute_ra_sell(sell, close)
        
        Hedgeye.writeData(date, ticker, description, buy, sell, close, weekweek, oneday, 
                        oneweek, onemonth, threemonth, sixmonth, oneyear, rab, ras)