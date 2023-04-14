from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy as sqla
from datetime import datetime


Base = declarative_base()
db_filename = 'DBControls/database.db'


def createSession():
    """Every interaction with the database will be done through a Session object. 
    So this function will be called to begin a new interaction.\n
    """
    try:
        # Open a editor session with the database
        engine = sqla.create_engine(f'sqlite:///{db_filename}', )
        Session = sessionmaker(bind=engine)
        return Session()
    except:
        raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")


class Hedgeye(Base):
    __tablename__ = 'Hedgeye'
    ID = sqla.Column('ID', sqla.Integer, primary_key=True)
    date = sqla.Column('Date', sqla.Text)
    ticker = sqla.Column('Ticker', sqla.Text)
    description = sqla.Column('Description', sqla.Text)
    buy = sqla.Column('Buy', sqla.Float)
    sell = sqla.Column('Sell', sqla.Float)
    close = sqla.Column('Close', sqla.Float)
    delta_ww = sqla.Column('Delta W/W', sqla.Float)
    od_delta = sqla.Column('1D Delta (%)', sqla.Float)
    ow_delta = sqla.Column('1W Delta (%)', sqla.Float)
    om_delta = sqla.Column('1M Delta (%)', sqla.Float)
    tm_delta = sqla.Column('3M Delta (%)', sqla.Float)
    sm_delta = sqla.Column('6M Delta (%)', sqla.Float)
    oy_delta = sqla.Column('1Y Delta (%)', sqla.Float)
    ra_buy = sqla.Column('Range Asymmetry Buy (%)', sqla.Float)
    ra_sell = sqla.Column('Range Asymmetry Sell (%)', sqla.Float)
        

    def getData(date=None, ticker=None, most_recent=False):
        """
        Gets data from database.\n
        Args:\n
            date (string, optional): yyyy-mm-dd. Defaults to None.\n
            ticker (string, optional): Form ABC...Z. Defaults to None.\n
            most_recent (bool, optional): If true, grabs the most recent results from database. Defaults to False.\n
        Returns:\n
            list: If passing only a date, ticker, or most_recent=True. If most_recent=True, date and ticker == None.\n
            Query Object: If passing date and ticker.\n
        """
        with createSession() as session:
            if date == '' or ticker == '':
                raise ValueError('Date or ticker is an empty string.\n')
            
            if isinstance(date, str):
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except:
                    raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
            
            if date and not ticker:
                result = session.query(Hedgeye).\
                    filter(Hedgeye.date == date).\
                    order_by(sqla.asc(Hedgeye.date)).all()
                return result
            
            elif ticker and not date:
                result = session.query(Hedgeye).\
                    filter(Hedgeye.ticker == ticker).\
                    order_by(sqla.asc(Hedgeye.date)).all()
                return result
            
            elif date and ticker:
                result = session.query(Hedgeye).\
                    filter(Hedgeye.date == date).\
                    filter(Hedgeye.ticker == ticker).first()
                return result
            
            elif not date and not ticker and most_recent:
                most_recent_date = session.query(sqla.func.max(Hedgeye.date)).scalar()
                result = session.query(Hedgeye).\
                    filter(Hedgeye.date == most_recent_date).\
                    order_by(sqla.asc(Hedgeye.date)).all()
                return result
            
            else:
                raise ValueError("""Need either date, ticker, or both to complete data lookup. 
                                 Cannot pass date or ticker when setting most_recent=True.\n""")
        
    
    def getAllDates():
        """Returns a list of all unique dates in database in ascending order.\n"""
        with createSession() as session:
            result = session.query(Hedgeye.date).\
                distinct().\
                order_by(sqla.asc(Hedgeye.date)).all()
                
        dates = []
        for r in result:
            dates.append(r[0])
            
        return dates
        
        
    def writeData(date, ticker, description, buy, sell, close, delta_ww, od_delta, 
                   ow_delta, om_delta, tm_delta, sm_delta, oy_delta, ra_buy, ra_sell):
        """
        Writes given data to database.\n
        Args:\n
            date (string): 'yyyy-mm-dd'\n
            ticker (string): 'ABC...Z'\n
            description (string): Ticker name.\n
            buy (float): Buy price.\n
            sell (float): Sell price.\n
            close (float): Close price.\n
            delta_ww (float): Week over week delta.\n
            od_delta (float): 1-Day delta.\n
            ow_delta (float): 1-Week delta.\n
            om_delta (float): 1-Month delta.\n
            tm_delta (float): 3-Month delta.\n
            sm_delta (float): 6-Month delta.\n
            oy_delta (float): 1-Year delta.\n
            ra_buy (float): Range asymmetry buy.\n
            ra_sell (float): Range asymmetry sell.\n
        """
        with createSession() as session:
            try:
                new_row = Hedgeye(date=date, ticker=ticker, description=description, buy=buy, 
                                        sell=sell, close=close, delta_ww=delta_ww, od_delta=od_delta, 
                                        ow_delta=ow_delta, om_delta=om_delta, tm_delta=tm_delta, 
                                        sm_delta=sm_delta, oy_delta=oy_delta, ra_buy=ra_buy, ra_sell=ra_sell)
                session.add(new_row)
            except:
                session.rollback()
                raise RuntimeError('Cannot add new data to Hedgeye table.\n')
            
            session.commit()
            

# ---------------------------------------------------------------------------------------------


class NASDAQ(Base):
    __tablename__ = 'NASDAQ'
    date = sqla.Column('Date', sqla.Text, primary_key=True)
    advancing_V = sqla.Column('Advancing Volume', sqla.Float)
    declining_V = sqla.Column('Declining Volume', sqla.Float)
    total_V = sqla.Column('Total Volume', sqla.Float)
    delta_V = sqla.Column('Change in Volume (%)', sqla.Float)
    close = sqla.Column('Close (%)', sqla.Float)
    upside_day = sqla.Column('Upside Day (%)')
    downside_day = sqla.Column('Downside Day (%)', sqla.Float)
    advances = sqla.Column('Advances', sqla.Float)
    declines = sqla.Column('Declines', sqla.Float)
    net_ad = sqla.Column('Net (Advances/Declines)', sqla.Float)
    td_breakaway = sqla.Column('10-Day Breakaway Momentum', sqla.Float)
    Td_breakaway = sqla.Column('20-Day Breakaway Momentum', sqla.Float)
    ad_ratio = sqla.Column('Advance/Decline Ratio', sqla.Float)
    ad_thrust = sqla.Column('Advance/Decline Thrust (%)', sqla.Float)
    fd_ad_thrust = sqla.Column('5-Day Advance/Decline Thrust (%)', sqla.Float)
    fd_ud_V_thrust = sqla.Column('5-Day Up/Down Volume Thrust (%)', sqla.Float)
    new_highs = sqla.Column('New Highs', sqla.Float)
    new_lows = sqla.Column('New Lows', sqla.Float)
    net_hl = sqla.Column('Net (Highs/Lows)', sqla.Float)
    tod_avg = sqla.Column('21-Day Average (Highs/Lows)', sqla.Float)
    std_avg = sqla.Column('63-Day Average (Highs/Lows)', sqla.Float)
        

    def getData(date, most_recent=False):
        """
        Gets data from database.\n
        Args:\n
            date (string): yyyy-mm-dd.\n
            most_recent (bool, optional): If true gets a list of most recent data in database. Defaults to False.\n
        Returns:\n
            Query Object: Row from databse.\n
        """
        with createSession() as session:  
            if date == '':
                raise ValueError('Date is an empty string.\n')
            
            if isinstance(date, str):
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except:
                    raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
            
            if date:
                result = session.query(NASDAQ).\
                    filter(NASDAQ.date == date).first()
                return result
            
            elif not date and most_recent:
                most_recent_date = session.query(sqla.func.max(NASDAQ.date)).scalar()
                result = session.query(NASDAQ).\
                    filter(NASDAQ.date == most_recent_date).first()
                return result
            
            else:
                raise ValueError('Need date to complete data lookup.\n')
        
        
    def getAllDates():
        """Returns a list of all unique dates in database in ascending order.\n"""
        with createSession() as session:        
            result = session.query(NASDAQ.date).\
                distinct().\
                order_by(sqla.asc(NASDAQ.date)).all()
                
        dates = []
        for r in result:
            dates.append(r[0])
            
        return dates
        

    def writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, downside_day, 
                   advances, declines, net_ad, td_breakaway, Td_breakaway, ad_ratio, ad_thrust, 
                   fd_ad_thrust, fd_ud_V_thrust, new_highs, new_lows, net_hl, tod_avg, std_avg):
        """
        Writes data to database.\n
        Args:\n
            date (string): 'yyyy-mm-dd'.\n
            advancing_V (float): Advancing Volume.\n
            declining_V (float): Declining Volume.\n
            total_V (float): Total Volume.\n
            delta_V (float): Change in Volume (%).\n
            close (float): Close (%).\n
            upside_day (float): Upside Day (%).\n
            downside_day (float): Downside Day (%).\n
            advances (float): Advances.\n
            declines (float): Declines.\n
            net_ad (float): Net (Advances/Declines).\n
            td_breakaway (float): 10-Day Breakaway Momentum.\n
            Td_breakaway (float): 20-Day Breakaway Momentum.\n
            ad_ratio (float): Advance/Decline Ratio.\n
            ad_thrust (float): Advance/Decline Thrust (%).\n
            fd_ad_thrust (float): 5-Day Advance/Decline Thrust (%).\n
            fd_ud_V_thrust (float): 5-Day Up/Down Volume Thrust (%).\n
            new_highs (float): New Highs.\n
            new_lows (float): New Lows.\n
            net_hl (float): Net (Highs/Lows).\n
            tod_avg (float): 21-Day Average.\n
            std_avg (float): 63-Day Average.\n
        """
        with createSession() as session:
            try:
                new_row = NASDAQ(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, delta_V=delta_V, 
                                    close=close, upside_day=upside_day, downside_day=downside_day, advances=advances, 
                                    declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, Td_breakaway=Td_breakaway, 
                                    ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust, fd_ud_V_thrust=fd_ud_V_thrust, 
                                    new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, tod_avg=tod_avg, std_avg=std_avg)
                session.add(new_row)
            except:
                session.rollback()
                raise RuntimeError('Cannot add new data to NASDAQ table.\n')
            
            session.commit()


# ---------------------------------------------------------------------------------------------


class NYSE(Base):
    __tablename__ = 'NYSE'
    date = sqla.Column('Date', sqla.Text, primary_key=True)
    advancing_V = sqla.Column('Advancing Volume', sqla.Float)
    declining_V = sqla.Column('Declining Volume', sqla.Float)
    total_V = sqla.Column('Total Volume', sqla.Float)
    delta_V = sqla.Column('Change in Volume (%)', sqla.Float)
    close = sqla.Column('Close (%)', sqla.Float)
    upside_day = sqla.Column('Upside Day (%)', sqla.Float)
    downside_day = sqla.Column('Downside Day (%)', sqla.Float)
    advances = sqla.Column('Advances', sqla.Float)
    declines = sqla.Column('Declines', sqla.Float)
    net_ad = sqla.Column('Net (Advances/Declines)', sqla.Float)
    td_breakaway = sqla.Column('10-Day Breakaway Momentum', sqla.Float)
    Td_breakaway = sqla.Column('20-Day Breakaway Momentum', sqla.Float)
    ad_ratio = sqla.Column('Advance/Decline Ratio', sqla.Float)
    ad_thrust = sqla.Column('Advance/Decline Thrust (%)', sqla.Float)
    fd_ad_thrust = sqla.Column('5-Day Advance/Decline Thrust (%)', sqla.Float)
    fd_ud_V_thrust = sqla.Column('5-Day Up/Down Volume Thrust (%)', sqla.Float)
    new_highs = sqla.Column('New Highs', sqla.Float)
    new_lows = sqla.Column('New Lows', sqla.Float)
    net_hl = sqla.Column('Net (Highs/Lows)', sqla.Float)
    tod_avg = sqla.Column('21-Day Average (Highs/Lows)', sqla.Float)
    std_avg = sqla.Column('63-Day Average (Highs/Lows)', sqla.Float)
        

    def getData(date, most_recent=False):
        """
        Gets data from database.\n
        Args:\n
            date (string): yyyy-mm-dd.\n
            most_recent (bool, optional): If true gets a list of most recent data in database. Defaults to False.\n
        Returns:\n
            Query Object: Row from databse.\n
        """
        with createSession() as session:    
            if date == '':
                raise ValueError('Date is an empty string.\n')
            
            if isinstance(date, str):
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except:
                    raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
            
            if date:
                result = session.query(NYSE).\
                    filter(NYSE.date == date).first()
                return result
            
            elif not date and most_recent:
                most_recent_date = session.query(sqla.func.max(NYSE.date)).scalar()
                result = session.query(NYSE).\
                    filter(NYSE.date == most_recent_date).first()
                return result
            
            else:
                raise ValueError('Need date to complete data lookup.\n')
        

    def getAllDates():
        """Returns a list of all unique dates in database in ascending order.\n"""
        with createSession() as session:        
            result = session.query(NYSE.date).\
                distinct().\
                order_by(sqla.asc(NYSE.date)).all()

        dates = []
        for r in result:
            dates.append(r[0])
            
        return dates


    def writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, downside_day, 
                   advances, declines, net_ad, td_breakaway, Td_breakaway, ad_ratio, ad_thrust, 
                   fd_ad_thrust, fd_ud_V_thrust, new_highs, new_lows, net_hl, tod_avg, std_avg):
        """
        Writes data to database.\n
        Args:\n
            date (string): 'yyyy-mm-dd'.\n
            advancing_V (float): Advancing Volume.\n
            declining_V (float): Declining Volume.\n
            total_V (float): Total Volume.\n
            delta_V (float): Change in Volume (%).\n
            close (float): Close (%).\n
            upside_day (float): Upside Day (%).\n
            downside_day (float): Downside Day (%).\n
            advances (float): Advances.\n
            declines (float): Declines.\n
            net_ad (float): Net (Advances/Declines).\n
            td_breakaway (float): 10-Day Breakaway Momentum.\n
            Td_breakaway (float): 20-Day Breakaway Momentum.\n
            ad_ratio (float): Advance/Decline Ratio.\n
            ad_thrust (float): Advance/Decline Thrust (%).\n
            fd_ad_thrust (float): 5-Day Advance/Decline Thrust (%).\n
            fd_ud_V_thrust (float): 5-Day Up/Down Volume Thrust (%).\n
            new_highs (float): New Highs.\n
            new_lows (float): New Lows.\n
            net_hl (float): Net (Highs/Lows).\n
            tod_avg (float): 21-Day Average.\n
            std_avg (float): 63-Day Average.\n
        """
        with createSession() as session:
            try:
                new_row = NYSE(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, 
                            delta_V=delta_V, close=close, upside_day=upside_day, downside_day=downside_day, 
                            advances=advances, declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, 
                            Td_breakaway=Td_breakaway, ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust,
                            fd_ud_V_thrust=fd_ud_V_thrust, new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, 
                            tod_avg=tod_avg, std_avg=std_avg)
                
                session.add(new_row)
            except:
                session.rollback()
                raise RuntimeError('Cannot add new data to NYSE table.\n')
                
            session.commit()