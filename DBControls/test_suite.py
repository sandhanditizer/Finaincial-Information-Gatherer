"""
To properly run the test suite, you need to remove the prepended folder location, 'DBControls' 
from the imports in files being tested. You also need to remove 'DBControls/' on line 7
in 'dbReadWrite.py'.
"""

import unittest
from test_dbRead import TestHedgeyeRead, TestNYSERead, TestNASDAQRead
from test_dbWrite import TestHedgeyeWrite, TestNYSEWrite, TestNASDAQWrite
import test_hedgeyePrep as hedgeye
import test_nasdaqPrep as nasdaq 
import test_nysePrep as nyse


test_suite = unittest.TestSuite()

# From test_dbRead
test_suite.addTest(unittest.makeSuite(TestHedgeyeRead))
test_suite.addTest(unittest.makeSuite(TestNYSERead))
test_suite.addTest(unittest.makeSuite(TestNASDAQRead))

# From test_dbWrite
test_suite.addTest(unittest.makeSuite(TestHedgeyeWrite))
test_suite.addTest(unittest.makeSuite(TestNYSEWrite))
test_suite.addTest(unittest.makeSuite(TestNASDAQWrite))

# From test_hedgeyePrep
test_suite.addTest(unittest.makeSuite(hedgeye.TestDelta_WW))
test_suite.addTest(unittest.makeSuite(hedgeye.TestOD_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestOW_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestOM_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestTM_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestSM_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestOY_Delta))
test_suite.addTest(unittest.makeSuite(hedgeye.TestRA_Buy))
test_suite.addTest(unittest.makeSuite(hedgeye.TestRA_Sell))
test_suite.addTest(unittest.makeSuite(hedgeye.TestAddRow))

# From test_nasdaqPrep
test_suite.addTest(unittest.makeSuite(nasdaq.TestTotalVolume))
test_suite.addTest(unittest.makeSuite(nasdaq.TestDeltaVolume))
test_suite.addTest(unittest.makeSuite(nasdaq.TestUpsideDay))
test_suite.addTest(unittest.makeSuite(nasdaq.TestDownsideDay))
test_suite.addTest(unittest.makeSuite(nasdaq.TestNetAD))
test_suite.addTest(unittest.makeSuite(nasdaq.TesttdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(nasdaq.TestTdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(nasdaq.TestAdvanceDeclineRatio))
test_suite.addTest(unittest.makeSuite(nasdaq.TestAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(nasdaq.TestFDAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(nasdaq.TestFDUpDownVolume))
test_suite.addTest(unittest.makeSuite(nasdaq.TestNetHighsLows))
test_suite.addTest(unittest.makeSuite(nasdaq.TestTODAverageHighsLows))
test_suite.addTest(unittest.makeSuite(nasdaq.TestSTDAverageHighsLows))
test_suite.addTest(unittest.makeSuite(nasdaq.TestAddRow))

# From test_nysePrep
test_suite.addTest(unittest.makeSuite(nyse.TestTotalVolume))
test_suite.addTest(unittest.makeSuite(nyse.TestDeltaVolume))
test_suite.addTest(unittest.makeSuite(nyse.TestUpsideDay))
test_suite.addTest(unittest.makeSuite(nyse.TestDownsideDay))
test_suite.addTest(unittest.makeSuite(nyse.TestNetAD))
test_suite.addTest(unittest.makeSuite(nyse.TesttdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(nyse.TestTdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(nyse.TestAdvanceDeclineRatio))
test_suite.addTest(unittest.makeSuite(nyse.TestAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(nyse.TestFDAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(nyse.TestFDUpDownVolume))
test_suite.addTest(unittest.makeSuite(nyse.TestNetHighsLows))
test_suite.addTest(unittest.makeSuite(nyse.TestTODAverageHighsLows))
test_suite.addTest(unittest.makeSuite(nyse.TestSTDAverageHighsLows))
test_suite.addTest(unittest.makeSuite(nyse.TestAddRow))



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite)

    