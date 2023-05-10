import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from contextlib import contextmanager


Base = declarative_base()
db_filename = 'DBControls/market_data.db'


@contextmanager
def createSession():
    """
    A context manager that creates a new session for interacting with the database. \n
    Returns:\n
        A context manager yielding a new session instance.
    """
    engine = sqla.create_engine(f'sqlite:///{db_filename}', )
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


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

 
    @staticmethod
    def getData(date=None, ticker=None):
        """
        Retrieves data from the database based on the given date and/or ticker.\n
        Args:\n
            date (str, optional): Date in the format 'yyyy-mm-dd'. Defaults to None.\n
            ticker (str, optional): Ticker symbol. Defaults to None.\n
        Returns:\n
            List[sqlalchemy.orm.Query]: A list of query results.\n
        Raises:\n
            ValueError: If the date is not in the correct format.
        """
        with createSession() as session:
            query = session.query(Hedgeye)

            if date:
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                    query = query.filter(Hedgeye.date == date)
                except ValueError:
                    raise ValueError(f'Date ({date}) needs to be in the format yyyy-mm-dd.')

            if ticker:
                query = query.filter(Hedgeye.ticker == ticker)

            if not date and not ticker: # Gets most recent data by date in table
                most_recent_date = session.query(sqla.func.max(Hedgeye.date)).scalar()
                query = query.filter(Hedgeye.date == most_recent_date)

            result = query.order_by(sqla.asc(Hedgeye.date)).all() # Will return None if the filters don't find anything

            return result


    @staticmethod
    def getAllDates():
        """
        etrieves a list of all unique dates in the database in ascending order.\n        
        Returns:\n
            List[str]: A list of unique dates in the format 'yyyy-mm-dd'.
        """
        with createSession() as session:
            result = session.query(Hedgeye.date).distinct().order_by(sqla.asc(Hedgeye.date)).all()
            return [r[0] for r in result]
        
        
    @staticmethod
    def writeData(date, ticker, description, buy, sell, close, delta_ww, od_delta, ow_delta, om_delta, tm_delta, sm_delta, oy_delta, ra_buy, ra_sell):
        """
        Writes the given data to the database.\n
        Args:\n
            date (str): Date in the format 'yyyy-mm-dd'.\n
            ticker (str): Ticker symbol.\n
            description (str): Ticker name.\n
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
            ra_sell (float): Range asymmetry sell.
        """
        with createSession() as session:
            if Hedgeye.getData(date=date, ticker=ticker) == []:
                new_row = Hedgeye(date=date, ticker=ticker, description=description, 
                                  buy=buy, sell=sell, close=close, delta_ww=delta_ww, 
                                  od_delta=od_delta, ow_delta=ow_delta, om_delta=om_delta, tm_delta=tm_delta, sm_delta=sm_delta, oy_delta=oy_delta, 
                                  ra_buy=ra_buy, ra_sell=ra_sell)
                session.add(new_row)
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
      
        
    @staticmethod
    def getData(date=None):
        """
        Retrieve data from the NASDAQ table in the database.\n
        Args:\n
            date (str, optional): A string representing the date in the format 'yyyy-mm-dd'. If not provided, the most recent data by date in the table is retrieved.\n
        Returns:\n
            An instance of the NASDAQ model class with the retrieved data.\n
        Raises:\n
            ValueError: If the date argument is not in the correct format 'yyyy-mm-dd'.
        """
        with createSession() as session:
            if not date: # Gets most recent data by date in table
                date = session.query(sqla.func.max(NASDAQ.date)).scalar()

            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date needs to be in the format yyyy-mm-dd.')

            result = session.query(NASDAQ).filter(NASDAQ.date == date).first()
            return result
   
        
    @staticmethod
    def getAllDates():
        """
        Retrieve all the distinct dates from the NASDAQ table in the database, ordered in ascending order.\n
        Returns:\n
            A list of strings representing the dates in the format 'yyyy-mm-dd'.
        """
        with createSession() as session:
            result = (
                session.query(NASDAQ.date)
                .distinct()
                .order_by(sqla.asc(NASDAQ.date))
                .all()
            )

        dates = [r[0] for r in result]
        return dates
  
        
    @staticmethod
    def writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, downside_day, 
                  advances, declines, net_ad, td_breakaway, Td_breakaway, ad_ratio, ad_thrust, 
                  fd_ad_thrust, fd_ud_V_thrust, new_highs, new_lows, net_hl, tod_avg, std_avg):
        """
        Write new data to the NASDAQ table in the database.\n
        Args:\n
            date (str): Date in the format 'yyyy-mm-dd'.\n
            advancing_V (float): Advancing volume for the day.\n
            declining_V (float): Dclining volume for the day.\n
            total_V (float): Total volume for the day.\n
            delta_V (float): Change in volumne (%).\n
            close (float): Closing percentage for the day (%).\n
            upside_day (float): Upside day (i.e. the closing price was higher than the previous day's closing price) (%).\n
            downside_day (float): Downside day (i.e. the closing price was lower than the previous day's closing price) (%).\n
            advances (float): Advancing issues for the day.\n
            declines (float): Declining issues for the day.\n
            net_ad (float): Net advancing issues for the day.\n
            td_breakaway (float): 10-day breakaway.\n
            Td_breakaway (float): 20-day breakaway.\n
            ad_ratio (float): Advance-decline ratio for the day.\n
            ad_thrust (float): Advance-decline thrust (%).\n
            fd_ad_thrust (float): 5-day advance-decline thrust day (%).\n
            fd_ud_V_thrust (float): 5-day upside volume thrust day (%).\n
            new_highs (float): New highs for the day.\n
            new_lows (float): New lows for the day.\n
            net_hl (float): Net new highs for the day.\n
            tod_avg (float): 21-day average for the day (Highs/Lows).\n
            std_avg (float): 63-day verage for the day (Highs/Lows).\n
        Returns:\n
            None
        """
        with createSession() as session:
            if NASDAQ.getData(date=date) == None:
                new_row = NASDAQ(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, delta_V=delta_V, 
                                 close=close, upside_day=upside_day, downside_day=downside_day, advances=advances, 
                                 declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, Td_breakaway=Td_breakaway, 
                                 ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust, fd_ud_V_thrust=fd_ud_V_thrust, 
                                 new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, tod_avg=tod_avg, std_avg=std_avg)
                session.add(new_row)
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
        

    @staticmethod
    def getData(date=None):
        """
        Retrieve data from the NYSE table in the database.\n
        Args:\n
            date (str, optional): A string representing the date in the format 'yyyy-mm-dd'. If not provided, the most recent data by date in the table is retrieved.\n
        Returns:\n
            An instance of the NYSE model class with the retrieved data.\n
        Raises:\n
            ValueError: If the date argument is not in the correct format 'yyyy-mm-dd'.
        """
        with createSession() as session:
            if not date: # Gets most recent data by date in table
                date = session.query(sqla.func.max(NYSE.date)).scalar()

            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date needs to be in the format yyyy-mm-dd.')

            result = session.query(NYSE).filter(NYSE.date == date).first()
            return result
   
        
    @staticmethod
    def getAllDates():
        """
        Retrieve all the distinct dates from the NYSE table in the database, ordered in ascending order.\n
        Returns:\n
            A list of strings representing the dates in the format 'yyyy-mm-dd'.
        """
        with createSession() as session:
            result = (
                session.query(NYSE.date)
                .distinct()
                .order_by(sqla.asc(NYSE.date))
                .all()
            )

        dates = [r[0] for r in result]
        return dates
  
        
    @staticmethod
    def writeData(date, advancing_V, declining_V, total_V, delta_V, close, upside_day, downside_day, 
                  advances, declines, net_ad, td_breakaway, Td_breakaway, ad_ratio, ad_thrust, 
                  fd_ad_thrust, fd_ud_V_thrust, new_highs, new_lows, net_hl, tod_avg, std_avg):
        """
        Write new data to the NYSE table in the database.\n
        Args:\n
            date (str): Date in the format 'yyyy-mm-dd'.\n
            advancing_V (float): Advancing volume for the day.\n
            declining_V (float): Dclining volume for the day.\n
            total_V (float): Total volume for the day.\n
            delta_V (float): Change in volumne (%).\n
            close (float): Closing percentage for the day (%).\n
            upside_day (float): Upside day (i.e. the closing price was higher than the previous day's closing price) (%).\n
            downside_day (float): Downside day (i.e. the closing price was lower than the previous day's closing price) (%).\n
            advances (float): Advancing issues for the day.\n
            declines (float): Declining issues for the day.\n
            net_ad (float): Net advancing issues for the day.\n
            td_breakaway (float): 10-day breakaway.\n
            Td_breakaway (float): 20-day breakaway.\n
            ad_ratio (float): Advance-decline ratio for the day.\n
            ad_thrust (float): Advance-decline thrust (%).\n
            fd_ad_thrust (float): 5-day advance-decline thrust day (%).\n
            fd_ud_V_thrust (float): 5-day upside volume thrust day (%).\n
            new_highs (float): New highs for the day.\n
            new_lows (float): New lows for the day.\n
            net_hl (float): Net new highs for the day.\n
            tod_avg (float): 21-day average for the day (Highs/Lows).\n
            std_avg (float): 63-day verage for the day (Highs/Lows).\n
        Returns:\n
            None
        """
        with createSession() as session:
            if NYSE.getData(date=date) == None:
                new_row = NYSE(date=date, advancing_V=advancing_V, declining_V=declining_V, total_V=total_V, delta_V=delta_V, 
                                 close=close, upside_day=upside_day, downside_day=downside_day, advances=advances, 
                                 declines=declines, net_ad=net_ad, td_breakaway=td_breakaway, Td_breakaway=Td_breakaway, 
                                 ad_ratio=ad_ratio, ad_thrust=ad_thrust, fd_ad_thrust=fd_ad_thrust, fd_ud_V_thrust=fd_ud_V_thrust, 
                                 new_highs=new_highs, new_lows=new_lows, net_hl=net_hl, tod_avg=tod_avg, std_avg=std_avg)
                session.add(new_row)
                session.commit()