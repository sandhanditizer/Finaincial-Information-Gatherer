from DBControls.dbReadWrite import NYSE
from datetime import datetime, timedelta
import numpy as np


# Functions are identical to that in the `nasdaqPrep.py` file. Functionality comments are located there.


def compute_total_volume(advancing_V, declining_V):
    return advancing_V + declining_V


def compute_delta_volume(date, total_V):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for i in range(1, 50):
        new_date_obj = date_obj - timedelta(days=i)
        new_date = new_date_obj.strftime('%Y-%m-%d')
        old_data = NYSE.getData(date=new_date)
        
        if old_data:
            return round(((total_V - old_data.total_V) / old_data.total_V) * 100, 2)
        
        if old_data == None and i == 49:
            return None
        

def compute_upside_day(advancing_V, declining_V):
    if (advancing_V + declining_V) == 0:
        raise ZeroDivisionError('The sum of advancing volume and declining volume is zero.\n')
    
    return round((advancing_V / (advancing_V + declining_V)) * 100, 2)


def compute_downside_day(advancing_V, declining_V):
    if (advancing_V + declining_V) == 0:
        raise ZeroDivisionError('The sum of advancing volume and declining volume is zero.\n')
    
    return round((declining_V / (advancing_V + declining_V)) * 100, 2)


def compute_net_advance_decline(advances, declines):
    return round(advances - declines, 2)


def compute_td_breakaway_momentum(date, advances, declines):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 9:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = NYSE.getData(date=new_date)
            
            if old_data:
                data.append((old_data.advances, old_data.declines))
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    A = (advances + np.sum(np.array(data)[:, 0]))
    D = (declines + np.sum(np.array(data)[:, 1]))

    if D == 0:
        raise ZeroDivisionError('10-Day sum of declines is 0. Cannot calculate 10-Day Breakaway Momentum.\n')
    else:
        return round(A / D, 2)
    
    
def compute_Td_breakaway_momentum(date, advances, declines):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 19:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            
            old_data = NYSE.getData(date=new_date)
            if old_data:
                data.append((old_data.advances, old_data.declines))
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    A = (advances + np.sum(np.array(data)[:, 0]))
    D = (declines + np.sum(np.array(data)[:, 1]))

    if D == 0:
        raise ZeroDivisionError('20-Day sum of declines is 0. Cannot calculate 20-Day Breakaway Momentum.\n')
    else:
        return round(A / D, 2)
    

def compute_advance_decline_ratio(advances, declines):
    if declines == 0:
        raise ZeroDivisionError('Declines is 0. Cannot calculate Advances/Declines Ratio.\n')
    
    return round(advances / declines, 2)


def compute_advance_decline_thrust(advances, declines):
    if (advances + declines) == 0:
        raise ZeroDivisionError('Declines + advances is 0. Cannot calculate Advances/Declines Thrust percentage.\n')
    
    return round((advances / (advances + declines)) * 100, 2)


def compute_fd_advance_decline_thrust(date, advances, declines):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 4:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = NYSE.getData(date=new_date)
            
            if old_data:
                data.append((old_data.advances, old_data.declines))
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    A = (advances + np.sum(np.array(data)[:, 0]))
    D = (declines + np.sum(np.array(data)[:, 1]))

    if (A + D) == 0:
        raise ZeroDivisionError('5-Day sum of advances and declines is 0. Cannot calculate 5-Day Whaley Breadth percentage.\n')
    else:
        return round((A / (A + D)) * 100, 2)
    
    
def compute_fd_up_down_volume(date, advancing_V, declining_V):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 4:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = NYSE.getData(date=new_date)
            
            if old_data:
                data.append((old_data.advancing_V, old_data.declining_V))
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    A = (advancing_V + np.sum(np.array(data)[:, 0]))
    D = (declining_V + np.sum(np.array(data)[:, 1]))

    if (A + D) == 0:
        raise ZeroDivisionError('5-Day sum of advanceing volume and declining volumn is 0.' + 
                                'Cannot calculate 5-Day Up/Down Volume Thrust percentage.\n')
    else:
        return round((A / (A + D)) * 100, 2)
    
    
def compute_net_highs_lows(new_highs, new_lows):
    return round(new_highs - new_lows, 2)


def compute_tod_avg_highs_lows(date, today_net_hl):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 20:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = NYSE.getData(date=new_date)
            
            if old_data:
                data.append(old_data.net_hl)
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    net_sum = (today_net_hl + np.sum(np.array(data)))
    return round(net_sum / 21, 2)


def compute_std_avg_highs_lows(date, today_net_hl):
    data = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    while len(data) < 62:
        for i in range(1, 50):
            new_date_obj = date_obj - timedelta(days=i)
            new_date = new_date_obj.strftime('%Y-%m-%d')
            old_data = NYSE.getData(date=new_date)
            
            if old_data:
                data.append(old_data.net_hl)
                date_obj = datetime.strptime(new_date, '%Y-%m-%d')
                break
            
            if old_data == None and i == 49:
                return None

    net_sum = (today_net_hl + np.sum(np.array(data)))
    return round(net_sum / 63, 2)


def add_row(date, advancing_V, declining_V, close, advances, declines, new_highs, new_lows):
    if not isinstance(date, str):
        raise TypeError('Date has a non-string type.\n')
    
    if date == '':
        raise ValueError('Date cannot be an empty string.\n')
    
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            ValueError('Date is not in the correct formate of yyyy-mm-dd.\n')
            
    if not isinstance((advancing_V), (int, float)) or not isinstance(declining_V, (int, float)) or not isinstance(close, (int, float)):
        raise TypeError('Advancing volume, declining volume, or close has a non-float or integer type.\n')
    
    if not isinstance(advances, (int, float)) or not isinstance(declines, (int, float)) or not isinstance(new_highs, (int, float)) or not isinstance(new_lows, (int, float)):
        raise TypeError('Advances, declines, new highs, or new lows has a non-float or integer type.\n')
    
    if declines == 0: # Prevents future errors
        raise ZeroDivisionError('Declines value is 0. Cannot add new row to NYSE table.\n')
    
    if NYSE.getData(date=date) == None:
        total_V = compute_total_volume(advancing_V, declining_V)
        delta_V = compute_delta_volume(date, total_V)
        upside_day = compute_upside_day(advancing_V, declining_V)
        downside_day = compute_downside_day(advancing_V, declining_V)
        net_ad = compute_net_advance_decline(advances, declines)
        td_breakaway = compute_td_breakaway_momentum(date, advances, declines)
        Td_breakaway = compute_Td_breakaway_momentum(date, advances, declines)
        ad_ratio = compute_advance_decline_ratio(advances, declines)
        ad_thrust = compute_advance_decline_thrust(advances, declines)
        fd_ad_thrust = compute_fd_advance_decline_thrust(date, advances, declines)
        fd_ud_volume = compute_fd_up_down_volume(date, advancing_V, declining_V)
        net_hl = compute_net_highs_lows(new_highs, new_lows)
        tod_avg_hl = compute_tod_avg_highs_lows(date, net_hl)
        std_avg_hl = compute_std_avg_highs_lows(date, net_hl)
        
        NYSE.writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, 
                        downside_day, advances, declines, net_ad, td_breakaway, Td_breakaway,
                        ad_ratio, ad_thrust, fd_ad_thrust, fd_ud_volume, new_highs, new_lows, 
                        net_hl, tod_avg_hl, std_avg_hl)