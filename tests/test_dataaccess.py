# In this file we test dataaccess routines and data preparation
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../src"))

import unittest

import dataaccess as da
import pandas as pd
import numpy as np

class TestCreatePandasDatasetFromCSV(unittest.TestCase):
  def setUp(self):
    self.returnValue = da.createPandasDatasetFromCSV("NDX")
  
  def test_datatype(self):
    self.assertTrue("symbol" in self.returnValue)
    self.assertTrue("data" in self.returnValue)
    self.assertEqual("NDX", self.returnValue["symbol"])
    self.assertIsInstance(self.returnValue["data"], pd.core.frame.DataFrame)

  def test_datastructure(self):
    tmp = self.returnValue["data"]
    self.assertEqual(tmp.shape, (4589, 2))
    self.assertEqual(tmp.index.dtype_str, 'datetime64[ns]')
    self.assertTrue("close" in tmp.columns)
    self.assertTrue("volume" in tmp.columns)
    self.assertEqual(tmp.volume.dtype.str, '<i8')
    self.assertEqual(tmp.close.dtype.str, '<f8')

class TestPrepareStockDataSynthetic(unittest.TestCase):
  def setUp(self):
    self.size = np.random.randint(42)
    rng = pd.date_range("12/04/1987", periods=self.size, freq="D")
    syntheticData = pd.DataFrame(np.random.randn(len(rng)), columns=["close"], index=rng).assign(volume=(1000000*np.random.rand(len(rng))).astype(int))
    syntheticData = syntheticData.sort_values("close")
    
    self.returnValue = da.prepareStockData(syntheticData)

  def test_ordering(self):
    tmp = self.returnValue
    last = None
    for row in tmp.iterrows():
      if last:
        self.assertTrue(row[0] > last)
      last = row[0]

  def test_datastructure(self):
    tmp = self.returnValue
    self.assertIsInstance(tmp, pd.core.frame.DataFrame)
    self.assertEqual(tmp.shape, (self.size, 2))
    self.assertTrue("price" in tmp)
    self.assertTrue("volume" in tmp)
    self.assertFalse("close" in tmp)
  

class TestPrepareStockData(TestPrepareStockDataSynthetic):
  def setUp(self):
    self.size = 4589
    tmp = da.createPandasDatasetFromCSV("NDX")
    self.returnValue = da.prepareStockData(tmp["data"])

class TestFetchStockDataset(TestPrepareStockDataSynthetic):
  def setUp(self):
    self.size = 4589
    self.returnDict = da.fetchStockDataset("NDX")
    self.returnValue = self.returnDict["data"]
  
  def test_structure(self):
    self.assertTrue("symbol" in self.returnDict)
    self.assertTrue("data" in self.returnDict)
    self.assertEqual("NDX", self.returnDict["symbol"])
    self.assertIsInstance(self.returnDict["data"], pd.core.frame.DataFrame)


if __name__ == '__main__':
    unittest.main()
