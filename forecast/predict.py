"""Performs Linear regression over the oil prices and predicts future prices."""

import matplotlib
matplotlib.use('Agg')  # Required before importing pyplot.
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from matplotlib import pyplot
from matplotlib.pyplot import xticks
from matplotlib.pyplot import show
from forecast.models import Price, Region


def OrganizeData(to_predict, window, horizon):
  """Organizes the oil price time series for regression."""
  shape = to_predict.shape[:-1] + (to_predict.shape[-1] - window + 1, window)
  strides = to_predict.strides + (to_predict.strides[-1],)
  X = np.lib.stride_tricks.as_strided(to_predict,
                                      shape=shape,
                                      strides=strides)
  y = np.array([X[i + horizon][-1] for i in range(len(X) - horizon)])
  return X[:-horizon], y


def Predict(region, months=3):
  """Performs linear regression over the oil prices and predicts data."""
  # Fetch region object.
  r = Region.objects.get(name=region)
  # Read price values for region in DataFrame.
  df = pd.DataFrame.from_records(Price.objects.filter(region=r).values(
      'month_str', 'price_per_barrel'))
  # Reverve the sequence of prices to have oldest price first.
  df = df.reindex(index=df.index[::-1])

  to_predict = df.price_per_barrel.values
  # Add last price value in time series for future dates as place holder.
  to_predict = np.append(to_predict, [to_predict[-1]] * months)
  dates = df.month_str.values
  # Generate and append future dates to time series.
  dt = pd.date_range(start=dates[-1], periods=months+1, freq='M')
  dt = dt.map(lambda t: t.strftime('%b-%Y'))
  dates = np.append(dates, dt[1:])

  k = 4  # Number of previous observations to use
  h = 1  # Forecast horizon
  X, y = OrganizeData(to_predict, k, h)
  m = 300 # Number of prices to use for training.

  regressor = LinearRegression(normalize=True)
  regressor.fit(X[:m], y[:m])

  # Predict last 20 values.
  ypred = regressor.predict(X)[-20:]

  y = y[0:-months]
  # Plot the last 20 actual and predicted values.
  f = pyplot.figure(figsize=(10, 7))
  pyplot.plot(y[-20 + months:], label='Actual Price', color='b', linewidth=2)
  pyplot.plot(ypred, 'ro-', linewidth=2, label='Prediction')
  xticks(np.arange(20), dates[-20:], rotation=45)
  pyplot.legend(loc='upper right')
  pyplot.ylabel('Price per barrel (USD)')
  show()
  pyplot.close(f)
  return f
