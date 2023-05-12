from DBControls.db_read_write import Hedgeye
from datetime import datetime, timedelta


def compute_delta_ww(date, ticker, today_buy, today_sell):
    """
    (today_buy - today_sell) - (past_week_buy - past_week_sell)
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(7, 30):
        new_date_obj = date_obj - timedelta(days=i) # Go back i days
        
        if new_date_obj.weekday() < 5: # Only make calculation on weekday
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
            if old_data:
                return round((today_buy - today_sell) - (old_data[0].buy - old_data[0].sell), 2)
    return None # Cannot find data to make calculation
    
        
def compute_od_delta(date, ticker, close):
    """
    [(today_close - yesterday_close) / yesterday_close] * 100 (%)
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(1, 30):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous day close value is 0. Cannot complete 1-Day Delta calculation.')     
    return None
       
        
def compute_ow_delta(date, ticker, close):
    """
    [(today_close - 7_days_ago_close) / 7_days_ago_close] * 100 (%)
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(7, 30):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous week close value is 0. Cannot complete 1-Week Delta calculation.')
    return None        
        
        
def compute_om_delta(date, ticker, close):
    """
    [(today_close - 1_month_ago_close) / 1_month_ago_close] * 100 (%)
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(30, 50):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
        
            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous month close value is 0. Cannot complete 1-Month Delta calculation.')
    return None
        

def compute_tm_delta(date, ticker, close):
    """
    [(today_close - 3_month_ago_close) / 3_month_ago_close] * 100 (%)
    """   
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(90, 120):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
            
            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous third month close value is 0. Cannot complete 3-Month Delta calculation.')
    return None
        
        
def compute_sm_delta(date, ticker, close):
    """
    [(today_close - 6_month_ago_close) / 6_month_ago_close] * 100 (%)
    """   
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(180, 210):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)
            
            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous sixth month close value is 0. Cannot complete 6-Month Delta calculation.')
    return None
        

def compute_oy_delta(date, ticker, close):
    """
    [(today_close - 1_year_ago_close) / 1_year_ago_close] * 100 (%)
    """   
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(365, 400):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = Hedgeye.getData(date=new_date, ticker=ticker)

            if old_data:
                try:
                    return round(((close - old_data[0].close) / old_data[0].close) * 100, 2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('Previous year close value is 0. Cannot complete 1-Year Delta calculation.')
    return None
        

def compute_ra_buy(buy, close):
    """
    [(today_buy - today_close) / today_close] * 100 (%)
    """
    if close == 0:
        raise ZeroDivisionError('Close value is 0. Cannot complete Range Asymmetry Buy calculation.')
    
    return round(((buy - close) / close) * 100, 2)


def compute_ra_sell(sell, close):
    """
    [(today_sell - today_close) / today_close] * 100 (%)
    """
    if close == 0:
        raise ZeroDivisionError('Close value is 0. Cannot complete Range Asymmetry Sell calculation.')
    
    return round(((sell - close) / close) * 100, 2)
        

def add_row(date, ticker, description, buy, sell, close):
    """
    Add a new row to the Hedgeye table with the given input parameters and calculated performance metrics.
    This function validates input types, checks date format, and computes various performance deltas and relative
    advantages for buy and sell prices. Finally, it writes the data to the Hedgeye table.\n
    Args:\n
        date (str): The date of the entry in the format yyyy-mm-dd.\n
        ticker (str): The stock ticker symbol.\n
        description (str): A brief description of the stock.\n
        buy (int or float): The buy price of the stock.\n
        sell (int or float): The sell price of the stock.\n
        close (int or float): The closing price of the stock.\n
    Raises:\n
        TypeError: If date, ticker, or description is not a string, or if buy, sell, or close is not an int or float.\n
        ValueError: If the date is not in the correct format yyyy-mm-dd.\n
        ZeroDivisionError: If the close value is 0, which would cause future errors.
    """
    if type(date) != str or type(ticker) != str or type(description) != str:
        raise TypeError('Date, ticker, or description has a non-string type.')
    
    if not isinstance(buy, (int, float)) or not isinstance(sell, (int, float)) or not isinstance(close, (int, float)):
        raise TypeError('Buy, sell, or close has a non-float or non-integer type.')
    
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            ValueError('Date is not in the correct formate of yyyy-mm-dd.\n')
            
    if close == 0: # Prevents future errors
        raise ZeroDivisionError('Close value is 0. Cannot add new row to Hedgeye table.\n')
    
    weekweek = compute_delta_ww(date, ticker, buy, sell)
    oneday = compute_od_delta(date, ticker, close)
    oneweek = compute_ow_delta(date, ticker, close)
    onemonth = compute_om_delta(date, ticker, close)
    threemonth = compute_tm_delta(date, ticker, close)
    sixmonth = compute_sm_delta(date, ticker, close)
    oneyear = compute_oy_delta(date, ticker, close)
    rab = compute_ra_buy(buy, close)
    ras = compute_ra_sell(sell, close)
    
    Hedgeye.writeData(date, ticker, description, buy, sell, close, weekweek, oneday, oneweek, onemonth, threemonth, sixmonth, oneyear, rab, ras)