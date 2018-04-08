# Create an indicator class
#
# Definition of output:
# An indicator of name "myIndicator" should take a pandas DataField and return a pandas DataField (or series?) with 
# identical indices and an additional column. This additional column is labelled "myIndicator" and indicates an 
# investment (boolean true) or disinvestment (boolean false) at each point in time (i.e. per row).
#
# Turning points in investment are identified on "strategy"-level.
#
# Input:
#   * DataField with at least following columns
#     * price
#     * volume
#
# Output:
#   * DataSeries (same indices as input DataField) of booleans (invested/not invested)
#

class Indicator:
  def __init__(self):
    self.bla = []

  @classmethod
  def from_string(cls, str):
    pass

def executeUserDefinedFunction(df, WINDOWLENGTH=200, THRESHOLD = 0.01):
  recentPrice = df["close"][-1]

  # START: indicator logic
  df["movingAverage"] = df["close"].rolling(window=WINDOWLENGTH).mean()
  df["aboveAverage"] = (df["close"] - df["movingAverage"]) > 0

  df["threshold"] = (((df["close"]-df["movingAverage"])/df["close"]).abs() > THRESHOLD)

  df = df[ df["threshold"] ] # selection -> is this already "strategy"? should we try to keep all decisions in the DataField?


  # from here, it seems like this is "strategy"-level
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


def evaluateIndicator():
    return [(days, thresh, executeUserDefinedFunction(df, days, thresh)[2:]) for days in [20,50,75,100,150,200,300,400,500,750,1000] for thresh in [0.00, 0.01, 0.02, 0.05, 0.1]] 