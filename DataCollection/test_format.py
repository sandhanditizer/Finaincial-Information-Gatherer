from format import *
import unittest


class TestReformatDate(unittest.TestCase):
    """Test various types of dates for reformating."""
    def test_answer(self):
        dates = [
            "2021-01-01",
            "Jan 1, 2021",
            "01/01/2021",
            "2021/01/01",
            "1st January 2021",
            "January 1st, 2021",
            "2021-Jan-01",
            "2021-January-01",
            "01-Jan-2021",
            "01-January-2021",
            "2021-01-01T12:00:00Z",
            "Jan 1, 2021 12:00:00 PM",
            "01/01/2021 12:00:00",
            "2021/01/01 12:00:00",
            "2021-01-01 12:00:00",
            "2021-01-01T12:00:00+00:00",
            "Jan 1, 2021 12:00:00 PM GMT",
            "01/01/2021 12:00:00 GMT",
            "2021/01/01 12:00:00 GMT",
            "2021-01-01 12:00:00 GMT",
            "2021-01-01T12:00:00-05:00",
            "Jan 1, 2021 12:00:00 PM EST",
            "01/01/2021 12:00:00 EST",
            "2021/01/01 12:00:00 EST",
            "2021-01-01 12:00:00 EST"
            ]
        
        for date in dates:
            with self.subTest(date=date):
                try:
                    reformatDate(date)
                except ValueError:
                    self.fail('ValueError raised for date: {date}')
            

class TestParenthesesRemover(unittest.TestCase):
    def test_answer(self):
        """Removes parentheses and anything between them."""
        spar = 'blahcjdi isdnnsd  odjc (ajsdsbf(&#ub4 k c) dskja'
        correct_s = 'blahcjdi isdnnsd  odjc  dskja'
        s = removeParentheseData(spar)
        self.assertEqual(s, correct_s)

        
class TestReformatData(unittest.TestCase):
    def test_answer(self):
        """Parses data out of raw website data."""
        data = """\n\n\nINDEX\nBUY TRADE\nSELL TRADE\nPREV. CLOSE\n\n\n\n\n\nUST30Y (BULLISH)\n\n30-Year U.S. Treasury Yield\n\n3.96\n3.67\n3.88\n\n\n\nUST10Y (BULLISH)\n\n10-Year U.S. Treasury Yield\n\n3.90\n3.57\n3.82\n\n\n"""
        extracted_data = reformatData(data)
        self.assertEqual(extracted_data, [{'Ticker': 'UST10Y', 'Description': '10-YEAR U.S. TREASURY YIELD', 'Buy': 3.9, 'Sell': 3.57, 'Close': 3.82}, {'Ticker': 'UST30Y', 'Description': '30-YEAR U.S. TREASURY YIELD', 'Buy': 3.96, 'Sell': 3.67, 'Close': 3.88}])
        

class TestClean(unittest.TestCase):
    def test_answer(self):
        """Test if it cleans data correctly."""
        data = {'test': '0.34%', 
                'test2': '$23.45', 
                'test3': '1,249343,4,24,54', 
                'test4': -304.23,
                'Date': '1111-11-11'
                }
        
        result = cleanData(data)
        self.assertEqual(result, {'test': 0.34, 
                                  'test2': 23.45, 
                                  'test3': 124934342454.0, 
                                  'test4': -304.23,
                                  'Date': '1111-11-11'
                                  })


if __name__ == '__main__':
    unittest.main()