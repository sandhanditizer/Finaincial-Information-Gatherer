"""
You need to remove 'DBControls/' on line 7 in 'dbReadWrite.py' before running tests.
You also need to remove the prepended 'DBControls' for identifying folder location in hedgeyePrep.py.
"""

import unittest
from test_dbReadWrite import TestHedgeye, TestNASDAQ, TestNYSE
import test_hedgeyePrep as hedgeye
import test_compositePrep as composite


test_suite = unittest.TestSuite()

# Testing all read and write functions
test_suite.addTest(unittest.makeSuite(TestHedgeye))
test_suite.addTest(unittest.makeSuite(TestNYSE))
test_suite.addTest(unittest.makeSuite(TestNASDAQ))

# Testing all metric calculations
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

# Testing all metric calculations
test_suite.addTest(unittest.makeSuite(composite.TestVolumeDelta))
test_suite.addTest(unittest.makeSuite(composite.TestUpsideDay))
test_suite.addTest(unittest.makeSuite(composite.TestDownsideDay))
test_suite.addTest(unittest.makeSuite(composite.TestNetAD))
test_suite.addTest(unittest.makeSuite(composite.TesttdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(composite.TestTdBreakawayMomentum))
test_suite.addTest(unittest.makeSuite(composite.TestAdvanceDeclineRatio))
test_suite.addTest(unittest.makeSuite(composite.TestAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(composite.TestFDAdvanceDeclineThrust))
test_suite.addTest(unittest.makeSuite(composite.TestFDUpDownVolume))
test_suite.addTest(unittest.makeSuite(composite.TestNetHighsLows))
test_suite.addTest(unittest.makeSuite(composite.TestTODAverageHighsLows))
test_suite.addTest(unittest.makeSuite(composite.TestSTDAverageHighsLows))
test_suite.addTest(unittest.makeSuite(composite.TestAddRow))



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite)

    