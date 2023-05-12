import unittest
from dbReadWrite import Hedgeye, NASDAQ, NYSE, createSession

# BEFORE TESTING ... CHANGE db_filename = 'DBControls/market_data.db' in dbReadWrite.py to db_filename = 'market_data.db'

class TestHedgeye(unittest.TestCase):
    def test_read_write_functions(self):
        """Tests getData, getAllDates, and writeData."""
        test_data = {
            'date': '1111-11-11',
            'ticker': 'TEST',
            'description': 'Test Ticker',
            'buy': 100.0,
            'sell': 90.0,
            'close': 95.0,
            'delta_ww': 5.0,
            'od_delta': 1.0,
            'ow_delta': 2.0,
            'om_delta': 3.0,
            'tm_delta': 4.0,
            'sm_delta': 5.0,
            'oy_delta': 6.0,
            'ra_buy': 7.0,
            'ra_sell': 8.0
        }
        Hedgeye.writeData(**test_data)
        
        # Test bad date
        with self.assertRaises(ValueError):
            Hedgeye.getData(date='202-20-01')
            
        # Test empty return
        result = Hedgeye.getData(date='3111-11-11')
        self.assertEqual(result, [])
        
        # Test empty return
        result = Hedgeye.getData(ticker='ABCDE')
        self.assertEqual(result, [])
            
        # Test getting data by date
        result = Hedgeye.getData(date='1111-11-11')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ticker, 'TEST')

        # Test getting data by ticker
        result = Hedgeye.getData(ticker='TEST')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, '1111-11-11')

        # Test getting data by both date and ticker
        result = Hedgeye.getData(date='1111-11-11', ticker='TEST')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, '1111-11-11')
        self.assertEqual(result[0].ticker, 'TEST')
        
        # Test getting most recent data
        result = Hedgeye.getData()
        self.assertGreater(len(result), 1)

        # Test getting all dates
        all_dates = Hedgeye.getAllDates()
        self.assertIn('1111-11-11', all_dates)

        # Clean up the test data
        with createSession() as session:
            session.query(Hedgeye).filter(Hedgeye.date == '1111-11-11', Hedgeye.ticker == 'TEST').delete()
            session.commit()


class TestNASDAQ(unittest.TestCase):
    def test_read_write_functions(self):
        """Tests getData, getAllDates, and writeData."""
        test_data = {
            'date': '1111-11-11', 
            'advancing_V': 1.0, 
            'declining_V': 2.0, 
            'total_V': 3.0, 
            'delta_V': 4.0, 
            'close': 5.0, 
            'upside_day': 6.0, 
            'downside_day': 7.0, 
            'advances': 8.0, 
            'declines': 9.0, 
            'net_ad': 10.0, 
            'td_breakaway': 11.0, 
            'Td_breakaway':12.0, 
            'ad_ratio': 13.0, 
            'ad_thrust': 14.0, 
            'fd_ad_thrust': 15.0, 
            'fd_ud_V_thrust': 16.0, 
            'new_highs': 17.0, 
            'new_lows': 18.0, 
            'net_hl': 19.0, 
            'tod_avg': 20.0, 
            'std_avg': 21.0
        }
        NASDAQ.writeData(**test_data)
        
        # Test bad date
        with self.assertRaises(ValueError):
            NASDAQ.getData(date='202-20-01')
            
        # Test empty return
        result = NASDAQ.getData(date='3111-11-11')
        self.assertIsNone(result)
        
        # Test getting data by date
        result = NASDAQ.getData(date='1111-11-11')
        self.assertEqual(result.date, '1111-11-11')
        self.assertEqual(result.close, 5.0)
        
        # Test getting most recent data
        result = NASDAQ.getData()
        self.assertIsNotNone(result)

        # Test getting all dates
        all_dates = NASDAQ.getAllDates()
        self.assertIn('1111-11-11', all_dates)

        # Clean up the test data
        with createSession() as session:
            session.query(NASDAQ).filter(NASDAQ.date == '1111-11-11').delete()
            session.commit()


class TestNYSE(unittest.TestCase):
    def test_read_write_functions(self):
        """Tests getData, getAllDates, and writeData."""
        test_data = {
            'date': '1111-11-11', 
            'advancing_V': 1.0, 
            'declining_V': 2.0, 
            'total_V': 3.0, 
            'delta_V': 4.0, 
            'close': 5.0, 
            'upside_day': 6.0, 
            'downside_day': 7.0, 
            'advances': 8.0, 
            'declines': 9.0, 
            'net_ad': 10.0, 
            'td_breakaway': 11.0, 
            'Td_breakaway':12.0, 
            'ad_ratio': 13.0, 
            'ad_thrust': 14.0, 
            'fd_ad_thrust': 15.0, 
            'fd_ud_V_thrust': 16.0, 
            'new_highs': 17.0, 
            'new_lows': 18.0, 
            'net_hl': 19.0, 
            'tod_avg': 20.0, 
            'std_avg': 21.0
        }
        NYSE.writeData(**test_data)
        
        # Test bad date
        with self.assertRaises(ValueError):
            NYSE.getData(date='202-20-01')
            
        # Test empty return
        result = NYSE.getData(date='3111-11-11')
        self.assertIsNone(result)
        
        # Test getting data by date
        result = NYSE.getData(date='1111-11-11')
        self.assertEqual(result.date, '1111-11-11')
        self.assertEqual(result.close, 5.0)
        
        # Test getting most recent data
        result = NYSE.getData()
        self.assertIsNotNone(result)

        # Test getting all dates
        all_dates = NYSE.getAllDates()
        self.assertIn('1111-11-11', all_dates)

        # Clean up the test data
        with createSession() as session:
            session.query(NYSE).filter(NYSE.date == '1111-11-11').delete()
            session.commit()


if __name__ == '__main__':
    unittest.main()
