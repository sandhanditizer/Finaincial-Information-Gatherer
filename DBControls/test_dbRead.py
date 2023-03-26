from dbReadWrite import Hedgeye, NYSE, NASDAQ
import unittest


class TestHedgeyeRead(unittest.TestCase):
    def test_missing_arguments(self):
        """Must have at least one argument"""
        with self.assertRaises(ValueError):
            Hedgeye.getData()
            
    def test_empty_string_ticker(self):
        """Cannot have empty tickers"""
        with self.assertRaises(ValueError):
            Hedgeye.getData(ticker='')

    def test_empty_string_date(self):
        """Cannot have empty dates"""
        with self.assertRaises(ValueError):
            Hedgeye.getData(date='')

    def test_incomplete_date(self):
        """Cannot have incomplete dates"""
        with self.assertRaises(ValueError):
            Hedgeye.getData(date='2023') 
        
    def test_incomplete_date_with_ticker(self):
        """Cannot have incomplete dates and correct ticker"""
        with self.assertRaises(ValueError):
            Hedgeye.getData(date='2023-', ticker='COIN') 
    
    def test_non_existent_date(self):
        """A date that is not in the table should return an empty list"""
        result = Hedgeye.getData(date='2050-01-25') 
        self.assertEqual(result, [])
    
    def test_non_existent_ticker(self):
        """A ticker that is not in the table should return an empty list"""
        result = Hedgeye.getData(ticker='JESUS') 
        self.assertEqual(result, [])
        
    def test_non_existent_date_and_ticker(self):
        """A date and ticker that are not in the table should return None type"""
        result = Hedgeye.getData(date='2025-03-20', ticker='JESUS') 
        self.assertEqual(result, None)
        
    def test_answer(self):
        """Found correct answer"""
        result = Hedgeye.getData(date='2023-01-25', ticker='COIN') 
        self.assertEqual(result.buy, 37.0)
        

class TestNYSERead(unittest.TestCase):
    def test_missing_arguments(self):
        """Must have at least one argument"""
        with self.assertRaises(TypeError):
            NYSE.getData()
    
    def test_empty_string_date(self):
        """Cannot have an empty date"""
        with self.assertRaises(ValueError):
            NYSE.getData(date='')
            
    def test_incomplete_date(self):
        """Date must be in the complete format yyyy-mm-dd"""
        with self.assertRaises(ValueError):
            NYSE.getData(date='2023') 
            
    def test_non_existent_date(self):
        """A date that does not exist in the table should return None type"""
        result = NYSE.getData(date='2050-01-25') 
        self.assertEqual(result, None)
        
    def test_answer(self):
        """Found correct answer"""
        result = NYSE.getData(date='2023-01-25') 
        self.assertEquals(result.close, 0.13)
        
        
class TestNASDAQRead(unittest.TestCase):
    def test_missing_arguments(self):
        """Must have at least one argument"""
        with self.assertRaises(TypeError):
            NASDAQ.getData()
    
    def test_empty_string_date(self):
        """Cannot have an empty date"""
        with self.assertRaises(ValueError):
            NASDAQ.getData(date='') 

    def test_incomplete_date(self):
        """Date must be in the complete format yyyy-mm-dd"""
        with self.assertRaises(ValueError):
            NASDAQ.getData(date='2023') 
            
    def test_non_existent_date(self):
        """A date that does not exist in the table should return None type"""
        result = NASDAQ.getData(date='2050-01-25') 
        self.assertEqual(result, None)
        
    def test_answer(self):
        """Found correct answer"""
        result = NASDAQ.getData(date='2023-01-25') 
        self.assertEquals(result.close, -0.18)
        
        
        
if __name__ == '__main__':
    unittest.main()