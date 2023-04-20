from format import *
import unittest


class TestGetDriver(unittest.TestCase):
    def test_unavailable_browser(self):
        """Only Edge and Firefox are available for scrapping"""
        with self.assertRaises(ValueError):
            getDriver('Safari')
    

class TestParenthesesRemover(unittest.TestCase):
    def test_answer(self):
        """Removes parentheses and anything between them"""
        spar = 'blahcjdi isdnnsd  odjc (ajsdk c) dskja'
        correct_s = 'blahcjdi isdnnsd  odjc  dskja'
        s = removeParentheses(spar)
        self.assertEqual(s, correct_s)

        
class TestExtract(unittest.TestCase):
    def test_answer(self):
        """Parses data out of a big string of data"""
        data = """\n\n\nINDEX\nBUY TRADE\nSELL TRADE\nPREV. CLOSE\n\n\n\n\n\nUST30Y (BULLISH)\n\n30-Year U.S. Treasury Yield\n\n3.96\n3.67\n3.88\n\n\n\nUST10Y (BULLISH)\n\n10-Year U.S. Treasury Yield\n\n3.90\n3.57\n3.82\n\n\n"""
        extracted_data = extract(data)
        self.assertEqual(extracted_data, [{'Ticker': 'UST30Y',
                            'Description': '30-YEAR U.S. TREASURY YIELD',
                            'Buy': 3.96,
                            'Sell': 3.67,
                            'Close': 3.88},
                            {'Ticker': 'UST10Y',
                            'Description': '10-YEAR U.S. TREASURY YIELD',
                            'Buy': 3.9,
                            'Sell': 3.57,
                            'Close': 3.82}])
        

class TestClean(unittest.TestCase):
    def test_answer(self):
        """Test if it cleans data correctly"""
        data = {'test': '0.34%', 
                'test2': '$23.45', 
                'test3': '1,249343,4,24,54', 
                'test4': -304.23}
        result = clean(data)
        self.assertEqual(result, {'test': 0.34, 
                                  'test2': 23.45, 
                                  'test3': 124934342454.0, 
                                  'test4': -304.23})


if __name__ == '__main__':
    unittest.main()