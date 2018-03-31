import configparser
config = configparser.ConfigParser()
config.read('config.cfg')

import pandas as pd
import numpy as np

def createPandasDatasetFromCSV():
  df = pd.read_csv("./test/daily_NDX.csv", index_col=0, parse_dates=True, usecols=[0,4,5])
  return df

def prepareStockData(df):
  df = df.sort_index(axis=0, ascending=True)
  return df


def executeUserDefinedFunction(df, WINDOWLENGTH=200, THRESHOLD = 0.01):
  recentPrice = df["close"][-1]

  df["movingAverage"] = df["close"].rolling(window=WINDOWLENGTH).mean()
  df["aboveAverage"] = (df["close"] - df["movingAverage"]) > 0

  df["threshold"] = (((df["close"]-df["movingAverage"])/df["close"]).abs() > THRESHOLD)

  df = df[ df["threshold"] ]

  se = df["aboveAverage"].values[:-1] != df["aboveAverage"].values[1:]
  df = df.assign(unique=np.insert(se, 0, True))

  df.drop(["movingAverage", "volume", "threshold"], axis=1)

  startInvested = df[df.unique]["aboveAverage"][0]
  endInvested = df[df.unique]["aboveAverage"][-1]

  prices = df[df.unique]["close"].values

  if not startInvested:
    prices = prices[1:]
  
  if endInvested:
    prices = np.append(prices, recentPrice)

  factors = (prices[1::2] / prices[:-1:2])


  return factors, prices, factors.prod(), len(factors)


def main():
  df = createPandasDatasetFromCSV()
  df = prepareStockData(df)
  return [(days, thresh, executeUserDefinedFunction(df, days, thresh)[2:]) for days in [20,50,75,100,150,200,300,400,500,750,1000] for thresh in [0.00, 0.01, 0.02, 0.05, 0.1]] 