from hedgeyePrep import *
import unittest


class TestDelta_WW(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """No ticker with the symbol AAA so cannot complete calculation."""
        result = compute_delta_ww('2023-05-09', 'AAA', 1, 1)
        self.assertEqual(result, None) 
        
    def test_answer_AMZN(self):
        """Find correct answer."""
        result = compute_delta_ww('2023-01-25', 'AMZN', 88, 99)
        self.assertEqual(result, 8.0)
        
    def test_answer_ETHE(self):
        """Find correct answer."""
        result = compute_delta_ww('2023-01-12', 'ETHE', 3.98, 7.14)
        self.assertEqual(result, -1.83)
        

class TestOD_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_od_delta('2022-01-03', 'AAPL', 129)
        self.assertEqual(result, None) 
        
    def test_answer_APPL(self):
        """Find correct answer."""
        result = compute_od_delta('2023-01-04', 'AAPL', 125)
        self.assertEqual(result, -3.10)
        
    def test_answer_COPPER(self):
        """Find correct answer."""
        result = compute_od_delta('2023-01-09', 'COPPER', 3.91)
        self.assertEqual(result, 2.36)


class TestOW_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_ow_delta('2022-01-03', 'AAPL', 129)
        self.assertEqual(result, None)
        
    def test_answer_GOOGL(self):
        """Find correct answer."""
        result = compute_ow_delta('2023-01-10', 'GOOGL', 88)
        self.assertEqual(result, 0.0)
        
    def test_answer_GOLD(self):
        """Find correct answer."""
        result = compute_ow_delta('2023-01-13', 'GOLD', 1898)
        self.assertEqual(result, 3.15)


class TestOM_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_om_delta('2022-01-25', 'NIKK', 27299)
        self.assertEqual(result, None)
        
    def test_answer_NFLX(self):
        """Find correct answer."""
        result = compute_om_delta('2023-04-20', 'NFLX', 323.0)
        self.assertEqual(result, 5.9)
        
    def test_answer_APPL(self):
        """Find correct answer."""
        result = compute_om_delta('2023-04-20', 'AAPL', 167.0)
        self.assertEqual(result, 6.37)
    

class TestTM_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_tm_delta('2022-01-25', 'NIKK', 27299)
        self.assertEqual(result, None)
        
    def test_answer_UST30Y(self):
        """Find correct answer."""
        result = compute_tm_delta('2023-04-20', 'UST30Y', 3.79)
        self.assertEqual(result, 6.16)
        
    def test_answer_UST10Y(self):
        """Find correct answer."""
        result = compute_tm_delta('2023-04-20', 'UST10Y', 3.6)
        self.assertEqual(result, 6.19)
    

class TestSM_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_sm_delta('2022-01-25', 'NIKK', 27299)
        self.assertEqual(result, None)
        
    # I do not have enough data to test correct answers
    

class TestOY_Delta(unittest.TestCase):
    def test_imputs_that_are_not_in_table(self):
        """Not enough information in the database to complete calculation."""
        result = compute_oy_delta('2022-01-25', 'NIKK', 27299)
        self.assertEqual(result, None)
        
    # I do not have enough data to test correct answers
    

class TestRA_Buy(unittest.TestCase):
    def test_division_by_zero(self):
        """Cannot divide by zero."""
        with self.assertRaises(ZeroDivisionError):
            compute_ra_buy(1, 0)
        
    def test_answer_BUY1(self):
        """Find correct answer."""
        result = compute_ra_buy(218, 239)
        self.assertEqual(result, -8.79)

    def test_answer_BUY2(self):
        """Find correct answer."""
        result = compute_ra_buy(103, 123)
        self.assertEqual(result, -16.26)
        
        
class TestRA_Sell(unittest.TestCase):
    def test_division_by_zero(self):
        """Cannot divide by zero."""
        with self.assertRaises(ZeroDivisionError):
            compute_ra_sell(1, 0)
        
    def test_answer_SELL1(self):
        """Find correct answer."""
        result = compute_ra_sell(242, 239)
        self.assertEqual(result, 1.26)

    def test_answer_SELL1(self):
        """Find correct answer."""
        result = compute_ra_sell(128, 123)
        self.assertEqual(result, 4.07)
 
 
class TestAddRow(unittest.TestCase):
    def test_bad_date(self):
        """Dates can only be strings and in the format yyyy-mm-dd."""
        with self.assertRaises(TypeError):
            add_row(0, 'ABC', 'ZZZ', 1, 2, 3)
        
    def test_bad_ticker(self):
        """Tickers can only be a strings."""
        with self.assertRaises(TypeError):
            add_row('1111-11-11', 0, 'ZZZ', 1, 2, 3)
        
    def test_bad_description(self):
        """Descriptions can only be strings."""
        with self.assertRaises(TypeError):
            add_row('1111-11-11', 'ABC', 0, 1, 2, 3)
            
    def test_bad_buy(self):
        """Buy values must be a integer or a float."""
        with self.assertRaises(TypeError):
            add_row('1111-11-11', 'ABC', 'ZZZ', '1', 2, 3)

    def test_bad_sell(self):
        """Sell values must be a integer or a float."""
        with self.assertRaises(TypeError):
            add_row('1111-11-11', 'ABC', 'ZZZ', 1, '2', 3)
        
    def test_bad_close(self):
        """Close values must be a integer or a float."""
        with self.assertRaises(TypeError):
            add_row('1111-11-11', 'ABC', 'ZZZ', 1, 2, '3')
            
    def test_date_format(self):
        """Date can only be in the format yyyy-mm-dd."""
        with self.assertRaises(ValueError):
            add_row('2/4/2000', 'ABC', 'ZZZ', 1, 2, 3)
        
    def test_preventative_division_by_zero(self):
        """Catches future division by zero errors."""
        with self.assertRaises(ZeroDivisionError):
            add_row('1111-11-11', 'ABC', 'ZZZ', 1, 2, 0)


if __name__ == '__main__':
    unittest.main()