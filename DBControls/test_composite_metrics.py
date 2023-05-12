from compositePrep import *
from dbReadWrite import NASDAQ, NYSE, createSession
import unittest


class TestVolumeDelta(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make delta calculation."""
        result = compute_volume_delta(NASDAQ, '2000-01-01', 1)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_volume_delta(NASDAQ, '2023-05-09', 4068224032)
        self.assertEqual(result, -2.03)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_volume_delta(NYSE, '2023-05-09', 3687592909)
        self.assertEqual(result, 3.83)
        
        
class TestUpsideDay(unittest.TestCase):
    def test_division_by_zero(self):
        """Check ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            compute_upside_day(0, 0)
        
    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_upside_day(1746192160, 2322031872)
        self.assertEqual(result, 42.92)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_upside_day(1665884957, 2021707952)
        self.assertEqual(result, 45.18)
        

class TestDownsideDay(unittest.TestCase):
    def test_division_by_zero(self):
        """Check ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            compute_downside_day(0, 0)
        
    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_downside_day(1746192160, 2322031872)
        self.assertEqual(result, 57.08)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_downside_day(1665884957, 2021707952)
        self.assertEqual(result, 54.82)
        
        
class TestNetAD(unittest.TestCase):
    def test_answer(self):
        """Find correct answer."""
        result = compute_net_advance_decline(1.10, 1.05)
        self.assertEqual(result, 0.05)
        
        
class TesttdBreakawayMomentum(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_td_breakaway_momentum(NASDAQ, '2000-01-01', 1, 2)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_td_breakaway_momentum(NASDAQ, '2023-05-09', 1877.0, 2531.0)
        self.assertEqual(result, 1.0)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_td_breakaway_momentum(NYSE, '2023-05-09', 1202.0, 1753.0)
        self.assertEqual(result, 0.95)
        

class TestTdBreakawayMomentum(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_Td_breakaway_momentum(NASDAQ, '2000-01-01', 1, 2)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_Td_breakaway_momentum(NASDAQ, '2023-05-09', 1877.0, 2531.0)
        self.assertEqual(result, 0.89)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_Td_breakaway_momentum(NYSE, '2023-05-09', 1202.0, 1753.0)
        self.assertEqual(result, 0.9)
        
        
class TestAdvanceDeclineRatio(unittest.TestCase):
    def test_division_by_zero(self):
        """Check ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            compute_advance_decline_ratio(1, 0)
        
    def test_answer(self):
        """Find correct answer."""
        result = compute_advance_decline_ratio(1, 2)
        self.assertEqual(result, 0.5)
        

class TestAdvanceDeclineThrust(unittest.TestCase):
    def test_division_by_zero(self):
        """Check ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            compute_advance_decline_thrust(0, 0)
        
    def test_answer(self):
        """Find correct answer."""
        result = compute_advance_decline_thrust(1, 2)
        self.assertEqual(result, 33.33)
        

class TestFDAdvanceDeclineThrust(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_fd_advance_decline_thrust(NASDAQ, '2000-01-01', 1, 2)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_fd_advance_decline_thrust(NASDAQ, '2023-05-09', 1877.0, 2531.0)
        self.assertEqual(result, 50.73)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_fd_advance_decline_thrust(NYSE, '2023-05-09', 1202.0, 1753.0)
        self.assertEqual(result, 48.12)
        
        
class TestFDUpDownVolume(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_fd_up_down_volume(NASDAQ, '2000-01-01', 1, 2)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_fd_up_down_volume(NASDAQ, '2023-05-09', 1746192160, 2322031872)
        self.assertEqual(result, 54.4)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_fd_up_down_volume(NYSE, '2023-05-09', 1665884957, 2021707952)
        self.assertEqual(result, 51.37)
        
        
class TestNetHighsLows(unittest.TestCase):
    def test_answer(self):
        """Find correct answer."""
        result = compute_net_highs_lows(128.0, 64.0)
        self.assertEqual(result, 64.0)


class TestTODAverageHighsLows(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_tod_avg_highs_lows(NASDAQ, '2000-01-01', 1)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_tod_avg_highs_lows(NASDAQ, '2023-05-09', -101.0)
        self.assertEqual(result, -152.29)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_tod_avg_highs_lows(NYSE, '2023-05-09', -27.0)
        self.assertEqual(result, -10.19)
        
        
class TestSTDAverageHighsLows(unittest.TestCase):
    def test_data_void(self):
        """Cannot find data pass 2000-01-01 to make calculation."""
        result = compute_std_avg_highs_lows(NASDAQ, '2000-01-01', 1)
        self.assertEqual(result, None)

    def test_answer_NASDAQ(self):
        """Find correct answer."""
        result = compute_std_avg_highs_lows(NASDAQ, '2023-05-09', -101.0)
        self.assertEqual(result, -110.59)
        
    def test_answer_NYSE(self):
        """Find correct answer."""
        result = compute_std_avg_highs_lows(NYSE, '2023-05-09', -27.0)
        self.assertEqual(result, -5.9)
        
        
class TestAddRow(unittest.TestCase):
    def test_non_string_date(self):
        """Dates cannot be anything but a string in the format yyyy-mm-dd."""
        with self.assertRaises(TypeError): 
            add_row(NASDAQ, 20230101, 1, 2, 3, 4, 5, 6, 7)
        
    def test_advancing_volume_type(self):
        """Advancing volume must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', '1', 2, 3, 4, 5, 6, 7)
        
    def test_declining_volume_type(self):
        """Declining volume must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, '2', 3, 4, 5, 6, 7)
        
    def test_close_type(self):
        """Close must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, 2, '3', 4, 5, 6, 7)

    def test_advances_type(self):
        """Advances must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, 2, 3, '4', 5, 6, 7)

    def test_declines_type(self):
        """Declines must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, 2, 3, 4, '5', 6, 7)
        
    def test_new_highs_type(self):
        """New highs must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, 2, 3, 4, 5, '6', 7)

    def test_new_lows_type(self):
        """New lows must be a float or integer."""
        with self.assertRaises(TypeError):
            add_row(NASDAQ, '2023-01-02', 1, 2, 3, 4, 5, 6, '7')
            
    def test_bad_format_date(self):
        """Date must be in the format of yyyy-mm-dd."""
        with self.assertRaises(ValueError):
            add_row(NASDAQ, '20/01/2023', 1, 2, 3, 4, 5, 6, 7)

    def test_declines_is_zero(self):
        """If declines is 0 it causes issues later."""
        with self.assertRaises(ZeroDivisionError):
            add_row(NASDAQ, '2023-01-02', 1, 2, 3, 4, 0, 6, 7)
            
    def test_add_row_NASDAQ(self):
        """Test adding a row to NASDAQ after making calculations."""
        add_row(NASDAQ, '1111-11-11', 0, 1, 2, 3, 4, 5, 6)
        result = NASDAQ.getData(date='1111-11-11')
        self.assertIsNotNone(result)
        
        with createSession() as session:
            session.query(NASDAQ).filter(NASDAQ.date == '1111-11-11').delete()
            session.commit()
        
        
    def test_add_row_NYSE(self):
        """Test adding a row to NYSE after making calculations."""
        add_row(NYSE, '1111-11-11', 0, 1, 2, 3, 4, 5, 6)
        result = NYSE.getData(date='1111-11-11')
        self.assertIsNotNone(result)
        
        with createSession() as session:
            session.query(NYSE).filter(NYSE.date == '1111-11-11').delete()
            session.commit()
        
        
if __name__ == '__main__':
    unittest.main()