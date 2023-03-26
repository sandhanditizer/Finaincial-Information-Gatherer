from nysePrep import *
import unittest


class TestTotalVolume(unittest.TestCase):
    def test_total(self):
        """Basic adding function"""
        result = compute_total_volume(2, 3)
        self.assertEqual(result, 5)
        

class TestDeltaVolume(unittest.TestCase):
    def test_data_that_isnt_in_the_table(self):
        """This returns None type becuase it cant find the necessary data to continue calculation"""
        result = compute_delta_volume('2000-01-23', 100)
        self.assertEqual(result, None)

    def test_answer(self):
        """Correct answer found"""
        result = compute_delta_volume('2022-01-12', 3960244193.0)
        self.assertEqual(result, -2.85)
        
    
class TestUpsideDay(unittest.TestCase):
    def test_division_by_zero(self):
        """If the sum of advancing and declining volume is 0 there would be an error"""
        with self.assertRaises(ZeroDivisionError):
            compute_upside_day(0, 0)
        
    def test_answer(self):
        """Found correct answer"""
        result = compute_upside_day(2, 2)
        self.assertEqual(result, 50.0)
        

class TestDownsideDay(unittest.TestCase):
    def test_division_by_zero(self):
        """If the sum of advancing and declining volume is 0 there would be an error"""
        with self.assertRaises(ZeroDivisionError):
            compute_downside_day(0, 0)
        
    def test_answer(self):
        """Found correct answer"""
        result = compute_downside_day(2, 2)
        self.assertEqual(result, 50.0)
        
class TestNetAD(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_net_advance_decline(1.10, 1.05)
        self.assertEqual(result, 0.05)
        
        
class TesttdBreakawayMomentum(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_td_breakaway_momentum('2022-01-12', 1711.0, 1624.0)
        self.assertEqual(result, 1.05)
        

class TestTdBreakawayMomentum(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_Td_breakaway_momentum('2022-01-12', 1711.0, 1624.0)
        self.assertEqual(result, 1.17)
        
        
class TestAdvanceDeclineRatio(unittest.TestCase):
    def test_division_by_zero(self):
        """If declines is 0, then it will result in an error"""
        with self.assertRaises(ZeroDivisionError):
            compute_advance_decline_ratio(1, 0)
        
    def test_answer(self):
        """Found correct answer"""
        result = compute_advance_decline_ratio(1, 2)
        self.assertEqual(result, 0.5)
        

class TestAdvanceDeclineThrust(unittest.TestCase):
    def test_division_by_zero(self):
        """If the sum of advances and declines is 0, then it will result in an error"""
        with self.assertRaises(ZeroDivisionError):
            compute_advance_decline_thrust(0, 0)
        
    def test_answer(self):
        """Found correct answer"""
        result = compute_advance_decline_thrust(1, 2)
        self.assertEqual(result, 33.33)
        

class TestFDAdvanceDeclineThrust(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_fd_advance_decline_thrust('2022-01-12', 1711.0, 1624.0)
        self.assertEqual(result, 53.72)
        
        
class TestFDUpDownVolume(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_fd_up_down_volume('2022-01-12', 2439597309.0, 1520646884.0)
        self.assertEqual(result, 60.33)
        
        
class TestNetHighsLows(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_net_highs_lows(128.0, 64.0)
        self.assertEqual(result, 64.0)


class TestTODAverageHighsLows(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_tod_avg_highs_lows('2022-01-12', 64.0)
        self.assertEqual(result, -4.0)
        
        
class TestSTDAverageHighsLows(unittest.TestCase):
    def test_answer(self):
        """Found correct answer"""
        result = compute_std_avg_highs_lows('2022-01-12', 64.0)
        self.assertEqual(result, 32.71)
        
        
class TestAddRow(unittest.TestCase):
    def test_non_string_date(self):
        """Dates cannot be anything but a string"""
        with self.assertRaises(TypeError): 
            add_row(20230101, 1, 2, 3, 4, 5, 6, 7)
        
    def test_empty_string_date(self):
        """Date cannot be an empty string"""
        with self.assertRaises(ValueError):
            add_row('', 1, 2, 3, 4, 5, 6, 7)
        
    def test_bad_format_date(self):
        """Date must be in the format of yyyy-mm-dd"""
        with self.assertRaises(ValueError):
            add_row('20/01/2023', 1, 2, 3, 4, 5, 6, 7)
        
    def test_advancing_volume_type(self):
        """Advancing volume must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', '1', 2, 3, 4, 5, 6, 7)
        
    def test_declining_volume_type(self):
        """Declining volume must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, '2', 3, 4, 5, 6, 7)
        
    def test_close_type(self):
        """Close must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, 2, '3', 4, 5, 6, 7)

    def test_advances_type(self):
        """Advances must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, 2, 3, '4', 5, 6, 7)

    def test_declines_type(self):
        """Declines must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, 2, 3, 4, '5', 6, 7)
        
    def test_new_highs_type(self):
        """New highs must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, 2, 3, 4, 5, '6', 7)

    def test_new_lows_type(self):
        """New lows must be a float or integer"""
        with self.assertRaises(TypeError):
            add_row('2023-01-02', 1, 2, 3, 4, 5, 6, '7')

    def test_declines_is_zero(self):
        """If declines is 0 it causes issues later"""
        with self.assertRaises(ZeroDivisionError):
            add_row('2023-01-02', 1, 2, 3, 4, 0, 6, 7)
        

        
if __name__ == '__main__':
    unittest.main()