from datetime import datetime, timedelta
import numpy as np


def compute_volume_delta(table, date, total_V):
    """[(total_V - old_data.total_V) / old_data.total_V] * 100 (%)"""
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(1, 50):
        new_date_obj = date_obj - timedelta(days=i)
        
        if new_date_obj.weekday() < 5:
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = table.getData(date=new_date)
        
            if old_data:
                return round(((total_V - old_data.total_V) / old_data.total_V) * 100, 2)
    return None
        

def compute_upside_day(advancing_V, declining_V):
    """[advancing_volume / (advancing_volume + declining_volumne)] * 100 (%)"""
    if (advancing_V + declining_V) == 0:
        raise ZeroDivisionError('The sum of advancing volume and declining volume is zero.')
    
    return round((advancing_V / (advancing_V + declining_V)) * 100, 2)


def compute_downside_day(advancing_V, declining_V):
    """[declining_V / (advancing_V + declining_V)] * 100 (%)"""
    if (advancing_V + declining_V) == 0:
        raise ZeroDivisionError('The sum of advancing volume and declining volume is zero.')
    
    return round((declining_V / (advancing_V + declining_V)) * 100, 2)


def compute_net_advance_decline(advances, declines):
    """advances - declines"""
    return round(advances - declines, 2)


def compute_td_breakaway_momentum(table, date, advances, declines):
    """(sum of advances in 10 days) / (sum of declines in 10 days)"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(40):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append((old_data.advances, old_data.declines))

        if len(data) == 9:        
            A = (advances + np.sum(np.array(data)[:, 0]))
            D = (declines + np.sum(np.array(data)[:, 1]))

            if D == 0:
                raise ZeroDivisionError('10-Day sum of declines is 0. Cannot calculate 10-Day Breakaway Momentum.')
            return round(A / D, 2)
    return None
    
    
def compute_Td_breakaway_momentum(table, date, advances, declines):
    """(sum of advances in 20 days) / (sum of declines in 20 days)"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(50):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append((old_data.advances, old_data.declines))

        if len(data) == 19:
            A = (advances + np.sum(np.array(data)[:, 0]))
            D = (declines + np.sum(np.array(data)[:, 1]))

            if D == 0:
                raise ZeroDivisionError('20-Day sum of declines is 0. Cannot calculate 20-Day Breakaway Momentum.')
            return round(A / D, 2)
    return None
    

def compute_advance_decline_ratio(advances, declines):
    """advances / declines"""
    if declines == 0:
        raise ZeroDivisionError('Declines is 0. Cannot calculate Advances/Declines Ratio.')
    
    return round(advances / declines, 2)


def compute_advance_decline_thrust(advances, declines):
    """[advances / (advances + declines)] * 100 (%)"""
    if (advances + declines) == 0:
        raise ZeroDivisionError('Declines + advances is 0. Cannot calculate Advances/Declines Thrust percentage.')
    
    return round((advances / (advances + declines)) * 100, 2)


def compute_fd_advance_decline_thrust(table, date, advances, declines):
    """[(sum of advances in 5 days) / ((sum of advances in 5 days) + (sum of advances in 5 days))] * 100 (%)"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(30):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append((old_data.advances, old_data.declines))
        
        if len(data) == 4:
            A = (advances + np.sum(np.array(data)[:, 0]))
            D = (declines + np.sum(np.array(data)[:, 1]))

            if (A + D) == 0:
                raise ZeroDivisionError('5-Day sum of advances and declines is 0. Cannot calculate 5-Day Whaley Breadth percentage.')
            return round((A / (A + D)) * 100, 2)
    return None
    
    
def compute_fd_up_down_volume(table, date, advancing_V, declining_V):
    """[(sum of advancing_volume in 5 days) / ((sum of advancing_volume in 5 days) + (sum of declining_volume in 5 days))] * 100 (%)"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(30):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append((old_data.advancing_V, old_data.declining_V))

        if len(data) == 4:
            A = (advancing_V + np.sum(np.array(data)[:, 0]))
            D = (declining_V + np.sum(np.array(data)[:, 1]))

            if (A + D) == 0:
                raise ZeroDivisionError('5-Day sum of advanceing volume and declining volumn is 0.' + 
                                        'Cannot calculate 5-Day Up/Down Volume Thrust percentage.')
            return round((A / (A + D)) * 100, 2)
    return None
    
    
def compute_net_highs_lows(new_highs, new_lows):
    """new_highs - new_lows"""
    return round(new_highs - new_lows, 2)


def compute_tod_avg_highs_lows(table, date, today_net_hl):
    """(sum of last 21 new highs and lows) / 21"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(50):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append(old_data.net_hl)

        if len(data) == 20:
            net_sum = (today_net_hl + np.sum(np.array(data)))
            return round(net_sum / 21, 2)
    return None


def compute_std_avg_highs_lows(table, date, today_net_hl):
    """(sum of last 63 new highs and lows) / 63"""
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for _ in range(100):
        new_date_obj = date_obj - timedelta(days=1)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        
        if new_date_obj.weekday() < 5:
            old_data = table.getData(date=new_date)
            if old_data:
                data.append(old_data.net_hl)

        if len(data) == 62:        
            net_sum = (today_net_hl + np.sum(np.array(data)))
            return round(net_sum / 63, 2)
    return None


def add_row(table, date, advancing_V, declining_V, total_V, close, advances, declines, new_highs, new_lows):
    """
    Adds a new row to the given table with the provided market data. It also calculates market performance metrics and stores them in the database.\n
    Args:\n
        table (Table object): The table object where the data will be written.\n
        date (str): The date in the format yyyy-mm-dd.\n
        advancing_V (int, float): The advancing volume for the day.\n
        declining_V (int, float): The declining volume for the day.\n
        close (int, float): The closing price for the day.\n
        advances (int, float): Advancing issues for the day.\n
        declines (int, float): Declining issues for the day.\n
        new_highs (int, float): New highs for the day.\n
        new_lows (int, float): New lows for the day.\n
    Raises:\n
        TypeError: If the date is not a string, or if any of the other input values are not float or integer.\n
        ValueError: If the date is not in the correct format.\n
        ZeroDivisionError: If the declines value is 0.
    """
    if not isinstance(date, str):
        raise TypeError('Date has a non-string type.')
    
    if not isinstance((advancing_V), (int, float)) or not isinstance(declining_V, (int, float)) or not isinstance(close, (int, float)):
        raise TypeError('Advancing volume, declining volume, or close has a non-float or integer type.')
    
    if not isinstance(advances, (int, float)) or not isinstance(declines, (int, float)) or not isinstance(new_highs, (int, float)) or not isinstance(new_lows, (int, float)):
        raise TypeError('Advances, declines, new highs, or new lows has a non-float or integer type.')
    
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            ValueError('Date is not in the correct formate of yyyy-mm-dd.')
            
    if declines == 0: # Prevents future errors
        raise ZeroDivisionError('Declines value is 0. Cannot add new row to table table.')
    
    delta_V = compute_volume_delta(table, date, total_V)
    upside_day = compute_upside_day(advancing_V, declining_V)
    downside_day = compute_downside_day(advancing_V, declining_V)
    net_ad = compute_net_advance_decline(advances, declines)
    td_breakaway = compute_td_breakaway_momentum(table, date, advances, declines)
    Td_breakaway = compute_Td_breakaway_momentum(table, date, advances, declines)
    ad_ratio = compute_advance_decline_ratio(advances, declines)
    ad_thrust = compute_advance_decline_thrust(advances, declines)
    fd_ad_thrust = compute_fd_advance_decline_thrust(table, date, advances, declines)
    fd_ud_volume = compute_fd_up_down_volume(table, date, advancing_V, declining_V)
    net_hl = compute_net_highs_lows(new_highs, new_lows)
    tod_avg_hl = compute_tod_avg_highs_lows(table, date, net_hl)
    std_avg_hl = compute_std_avg_highs_lows(table, date, net_hl)
    
    table.writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, 
                    downside_day, advances, declines, net_ad, td_breakaway, Td_breakaway,
                    ad_ratio, ad_thrust, fd_ad_thrust, fd_ud_volume, new_highs, new_lows, 
                    net_hl, tod_avg_hl, std_avg_hl)