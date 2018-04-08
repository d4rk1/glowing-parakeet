import configparser
config = configparser.ConfigParser()
config.read('../config.cfg')

import pandas as pd
import numpy as np

def createPandasDatasetFromCSV(symbol="NDX"):
  df = pd.read_csv("./tests/daily_NDX.csv", index_col=0, parse_dates=True, usecols=[0,4,5])
  return {"symbol": symbol, "data": df}

def prepareStockData(df):
  df = df.sort_index(axis=0, ascending=True)
  columns = ["price" if "close" == col else col for col in df.columns]
  df.columns = columns
  return df


def fetchStockDataset(symbol="NDX"):
  # as far as we are not online, use local test data
  # TODO: go for dynamic fetching and prepartion (ideally with some caching involved)
  df = createPandasDatasetFromCSV(symbol="NDX")
  df = prepareStockData(df["data"])

  return {"symbol": symbol, "data": df}
