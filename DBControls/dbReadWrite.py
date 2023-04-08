from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Float, Text, Integer, func, asc
from datetime import datetime


Base = declarative_base()
db_filename = 'DBControls/database.db'


class Hedgeye(Base):
    __tablename__ = 'Hedgeye'
    id = Column(Integer, name='ID', primary_key=True)
    date = Column(Text, name='Date')
    ticker = Column(Text, name='Ticker')
    description = Column(Text, name='Description')
    buy = Column(Float, name='Buy')
    sell = Column(Float, name='Sell')
    close = Column(Float, name='Close')
    delta_ww = Column(Float, name='Delta W/W')
    od_delta = Column(Float, name='1D Delta (%)')
    ow_delta = Column(Float, name='1W Delta (%)')
    om_delta = Column(Float, name='1M Delta (%)')
    tm_delta = Column(Float, name='3M Delta (%)')
    sm_delta = Column(Float, name='6M Delta (%)')
    oy_delta = Column(Float, name='1Y Delta (%)')
    ra_buy = Column(Float, name='Range Asymmetry Buy (%)')
    ra_sell = Column(Float, name='Range Asymmetry Sell (%)')
        

    def getData(date=None, ticker=None, most_recent=False):
        """
        Queries database for data based on request specified by specific date, ticker, date and ticker, or most recent date.\n
        Args:\n
            date (string, optional): 'yyyy-mm-dd'. Defaults to None.\n
            ticker (string, optional): 'ABC...Z'. Defaults to None.\n
            most_recent (bool, optional): True = gets data associated with the most recent date in the database. Defaults to False.\n
        Returns:\n
            list: If call is getData(ticker='ABC'), getData(most_recent=True), or getData(date='yyyy-mm-dd')
            dict: If call is getData(date='yyyy-mm-dd', ticker='ABC')
            
        """
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")

        if date == '' or ticker == '':
            session.close()
            raise ValueError('Date or ticker is an empty string.\n')
        
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except:
                session.close()
                raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
        
        if date and not ticker:
            # List of Hedgeye results ordered by date
            result = session.query(Hedgeye).filter(Hedgeye.date == date).order_by(asc(Hedgeye.date)).all()
            session.close()
            return result
        
        elif ticker and not date:
            # List of Hedgeye results ordered by date
            result = session.query(Hedgeye).filter(Hedgeye.ticker == ticker).order_by(asc(Hedgeye.date)).all()
            session.close()
            return result
        
        elif date and ticker:
            # Single Hedgeye result
            result = session.query(Hedgeye).filter(Hedgeye.date == date, Hedgeye.ticker == ticker).first()
            session.close()
            return result
        
        elif not date and most_recent:
            most_recent_date = session.query(func.max(Hedgeye.date)).scalar()
            
            # List of Hedgeye results ordered by date
            result = session.query(Hedgeye).filter(Hedgeye.date == most_recent_date).order_by(asc(Hedgeye.date)).all()
            session.close()
            return result
        
        else:
            session.close()
            raise ValueError('Need either date, ticker, or both to complete data lookup.\n')
        
        
    def writeData(date, ticker, description, buy, sell, close, delta_ww, od_delta, 
                   ow_delta, om_delta, tm_delta, sm_delta, oy_delta, ra_buy, ra_sell):
        """
        Writes data according to each row in the database.\n
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
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")
        
        try:
            new_row = Hedgeye(date=date, ticker=ticker, description=description, 
                            buy=buy, sell=sell, close=close, delta_ww=delta_ww, 
                            od_delta=od_delta, ow_delta=ow_delta, om_delta=om_delta, 
                            tm_delta=tm_delta, sm_delta=sm_delta, oy_delta=oy_delta, 
                            ra_buy=ra_buy, ra_sell=ra_sell)
            
            session.add(new_row)
            session.commit()
        except:
            raise RuntimeError('Cannot add new data to Hedgeye table.\n')
        finally:
            session.close()
            

# ---------------------------------------------------------------------------------------------


class NASDAQ(Base):
    __tablename__ = 'NASDAQ'
    date = Column(Text, name='Date', primary_key=True)
    advancing_V = Column(Float, name='Advancing Volume')
    declining_V = Column(Float, name='Declining Volume')
    total_V = Column(Float, name='Total Volume')
    delta_V = Column(Float, name='Change in Volume (%)')
    close = Column(Float, name='Close (%)')
    upside_day = Column(Float, name='Upside Day (%)')
    downside_day = Column(Float, name='Downside Day (%)')
    advances = Column(Float, name='Advances')
    declines = Column(Float, name='Declines')
    net_ad = Column(Float, name='Net (Advances/Declines)')
    td_breakaway = Column(Float, name='10-Day Breakaway Momentum')
    Td_breakaway = Column(Float, name='20-Day Breakaway Momentum')
    ad_ratio = Column(Float, name='Advance/Decline Ratio')
    ad_thrust = Column(Float, name='Advance/Decline Thrust (%)')
    fd_ad_thrust = Column(Float, name='5-Day Advance/Decline Thrust (%)')
    fd_ud_V_thrust = Column(Float, name='5-Day Up/Down Volume Thrust (%)')
    new_highs = Column(Float, name='New Highs')
    new_lows = Column(Float, name='New Lows')
    net_hl = Column(Float, name='Net (Highs/Lows)')
    tod_avg = Column(Float, name='21-Day Average (Highs/Lows)')
    std_avg = Column(Float, name='63-Day Average (Highs/Lows)')
        

    def getData(date, most_recent=False):
        """
        Queries database for data based on request specified by specific date or most recent date.\n
        Args:\n
            date (string): 'yyyy-mm-dd'.\n
            most_recent (bool, optional): True = Gets data that is the most recent. Defaults to False.\n
        Returns:\n
            dict: Data.\n
        """
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")
            
        if date == '':
            session.close()
            raise ValueError('Date is an empty string.\n')
        
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except:
                session.close()
                raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
        
        if date:
            result = session.query(NASDAQ).filter(NASDAQ.date == date).first()
            session.close()
            return result
        
        elif not date and most_recent:
            most_recent_date = session.query(func.max(NASDAQ.date)).scalar()
            result = session.query(NASDAQ).filter(NASDAQ.date == most_recent_date).first()
            session.close()
            return result
        
        else:
            session.close()
            raise ValueError('Need date to complete data lookup.\n')
        

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
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")
        
        try:
            new_row = NASDAQ(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, 
                           delta_V=delta_V, close=close, upside_day=upside_day, downside_day=downside_day, 
                           advances=advances, declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, 
                           Td_breakaway=Td_breakaway, ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust,
                           fd_ud_V_thrust=fd_ud_V_thrust, new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, 
                           tod_avg=tod_avg, std_avg=std_avg)
            
            session.add(new_row)
            session.commit()
        except:
            raise RuntimeError('Cannot add new data to NASDAQ table.\n')
        finally:
            session.close()


# ---------------------------------------------------------------------------------------------


class NYSE(Base):
    __tablename__ = 'NYSE'
    date = Column(Text, name='Date', primary_key=True)
    advancing_V = Column(Float, name='Advancing Volume')
    declining_V = Column(Float, name='Declining Volume')
    total_V = Column(Float, name='Total Volume')
    delta_V = Column(Float, name='Change in Volume (%)')
    close = Column(Float, name='Close (%)')
    upside_day = Column(Float, name='Upside Day (%)')
    downside_day = Column(Float, name='Downside Day (%)')
    advances = Column(Float, name='Advances')
    declines = Column(Float, name='Declines')
    net_ad = Column(Float, name='Net (Advances/Declines)')
    td_breakaway = Column(Float, name='10-Day Breakaway Momentum')
    Td_breakaway = Column(Float, name='20-Day Breakaway Momentum')
    ad_ratio = Column(Float, name='Advance/Decline Ratio')
    ad_thrust = Column(Float, name='Advance/Decline Thrust (%)')
    fd_ad_thrust = Column(Float, name='5-Day Advance/Decline Thrust (%)')
    fd_ud_V_thrust = Column(Float, name='5-Day Up/Down Volume Thrust (%)')
    new_highs = Column(Float, name='New Highs')
    new_lows = Column(Float, name='New Lows')
    net_hl = Column(Float, name='Net (Highs/Lows)')
    tod_avg = Column(Float, name='21-Day Average (Highs/Lows)')
    std_avg = Column(Float, name='63-Day Average (Highs/Lows)')
        

    def getData(date, most_recent=False):
        """
        Queries database for data based on request specified by specific date or most recent date.\n
        Args:\n
            date (string): 'yyyy-mm-dd'.\n
            most_recent (bool, optional): True = Gets data that is the most recent. Defaults to False.\n
        Returns:\n
            dict: Data.\n
        """
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")
            
        if date == '':
            session.close()
            raise ValueError('Date is an empty string.\n')
        
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except:
                session.close()
                raise ValueError('Date needs to be in the format yyyy-mm-dd.\n')
        
        if date:
            result = session.query(NYSE).filter(NYSE.date == date).first()
            session.close()
            return result
        
        elif not date and most_recent:
            most_recent_date = session.query(func.max(NYSE.date)).scalar()
            result = session.query(NYSE).filter(NYSE.date == most_recent_date).first()
            session.close()
            return result
        
        else:
            session.close()
            raise ValueError('Need date to complete data lookup.\n')


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
        
        try:
            # Open a editor session with the database
            engine = create_engine(f'sqlite:///{db_filename}', )
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            raise ConnectionError(f"Cannot create an engine or make a session for {db_filename}.\n")
        
        try:
            new_row = NYSE(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, 
                           delta_V=delta_V, close=close, upside_day=upside_day, downside_day=downside_day, 
                           advances=advances, declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, 
                           Td_breakaway=Td_breakaway, ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust,
                           fd_ud_V_thrust=fd_ud_V_thrust, new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, 
                           tod_avg=tod_avg, std_avg=std_avg)
            
            session.add(new_row)
            session.commit()
        except:
            raise RuntimeError('Cannot add new data to NYSE table.\n')
        finally:
            session.close()