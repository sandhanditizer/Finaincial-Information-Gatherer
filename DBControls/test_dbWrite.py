from dbReadWrite import Hedgeye, NYSE, NASDAQ, createSession
import unittest


class TestHedgeyeWrite(unittest.TestCase):            
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            Hedgeye.writeData()
            
    def test_write(self):
        """Testing if it writes data properly and if it then shows up"""
        Hedgeye.writeData('1111-11-11', 'ABC', 'ZZZZ', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        result = Hedgeye.getData(date='1111-11-11', ticker='ABC')
        self.assertIsNotNone(result)
        
        with createSession() as session:
            session.query(Hedgeye).\
                filter(Hedgeye.date == '1111-11-11').\
                filter(Hedgeye.ticker == 'ABC').delete()
            session.commit()
        
        result = Hedgeye.getData(date='1111-11-11', ticker='ABC')
        self.assertIsNone(result)
        
        
class TestNASDAQWrite(unittest.TestCase):
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            NASDAQ.writeData()
            
    def test_write(self):
        """Testing if it writes data properly and if it then shows up"""
        NASDAQ.writeData('1111-11-11', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
        result = NASDAQ.getData(date='1111-11-11')
        self.assertIsNotNone(result)
        
        with createSession() as session:
            session.query(NASDAQ).\
                filter(NASDAQ.date == '1111-11-11').delete()
            session.commit()
        
        result = NASDAQ.getData(date='1111-11-11')
        self.assertIsNone(result)
      
        
class TestNYSEWrite(unittest.TestCase):   
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            NYSE.writeData()
            
    def test_write(self):
        """Testing if it writes data properly and if it then shows up"""
        NYSE.writeData('1111-11-11', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
        result = NYSE.getData(date='1111-11-11')
        self.assertIsNotNone(result)
        
        with createSession() as session:
            session.query(NYSE).\
                filter(NYSE.date == '1111-11-11').delete()
            session.commit()
        
        result = NYSE.getData(date='1111-11-11')
        self.assertIsNone(result)
        


if __name__ == '__main__':
    unittest.main()