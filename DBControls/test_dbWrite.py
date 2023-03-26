from dbReadWrite import Hedgeye, NYSE, NASDAQ
import unittest


class TestHedgeyeWrite(unittest.TestCase):            
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            Hedgeye.writeData()
        
        
class TestNYSEWrite(unittest.TestCase):   
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            NYSE.writeData()
        

class TestNASDAQWrite(unittest.TestCase):
    def test_missing_arguments(self):
        """Cannot have missing arguments"""
        with self.assertRaises(TypeError):
            NASDAQ.writeData()



if __name__ == '__main__':
    unittest.main()