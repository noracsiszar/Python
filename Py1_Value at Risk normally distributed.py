#!/usr/bin/env python
# coding: utf-8
#getting data from yahoofinance for AAPL, CVX, KO, JNJ and PG
#importing pandas for dataframe handling
#including matplotlib for plots visualisation
#including numpy
#importing norm from scipystats for VaR
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

#defining tickers for pulling data
ticker_symbol_1 = 'AAPL'
ticker_symbol_2 = 'CVX'
ticker_symbol_3 = 'KO'
ticker_symbol_4 = 'JNJ'
ticker_symbol_5 = 'PG'

#defining the historical period starting from today
appl = yf.Ticker(ticker_symbol_1)
cvx = yf.Ticker(ticker_symbol_2)
ko = yf.Ticker(ticker_symbol_3)
jnj = yf.Ticker(ticker_symbol_4)
pg = yf.Ticker(ticker_symbol_5)

#defining to only pull Close column from historical data
historical_data_appl = appl.history(period="2y")
historical_data_cvx = cvx.history(period="2y")
historical_data_ko = ko.history(period="2y")
historical_data_jnj = jnj.history(period="2y")
historical_data_pg = pg.history(period="2y")

#deciding only use Close from historical data
daily_prices_aapl = historical_data_appl[['Close']]
daily_prices_cvx = historical_data_cvx[['Close']]
daily_prices_ko = historical_data_ko[['Close']]
daily_prices_jnj = historical_data_jnj[['Close']]
daily_prices_pg = historical_data_pg[['Close']]

#creating a combined dataframe of all data
combined_prices = pd.concat([daily_prices_aapl, daily_prices_cvx, daily_prices_ko, daily_prices_jnj, daily_prices_pg], axis=1)

# Convert the index to a string format (YYYY-MM-DD)
combined_prices.index = combined_prices.index.strftime('%Y-%m-%d')

#renaming colum "Close" into corresponding tickers
# Rename columns
tickers = ['AAPL', 'CVX', 'KO', 'JNJ', 'PG']
combined_prices.columns = tickers

# Display the transformed data frame
print(combined_prices.head())

#creating a plot for visualisation
combined_prices.plot().set_ylabel("Closing prices in US$")
plt.show()

#Compute daily asset returns 
daily_returns = combined_prices.pct_change()

#creating a list for portfolio weights
weights = [0.4, 0.2, 0.1, 0.15, 0.15]

#defining portfolio returns as a product of weights and daily returns - dot
portfolio_returns = daily_returns.dot(weights)

#plotting portfolio returns
portfolio_returns.plot().set_ylabel("Daily returns in %")
plt.show()

#Generate the covariance matrix from the portfolio daily returns
covariance = daily_returns.cov()

#annulize the covariance using 252 days per year
covariance_annulized = covariance * 252
print(covariance_annulized)

#let us compute the mean and the variance of the portfolio returns
portfolio_mean = portfolio_returns.mean()
portfolio_std = portfolio_returns.std()
VaR_95 = norm.ppf(0.95, loc=portfolio_mean, scale=portfolio_std)
print("VaR at 95% confidence level:", VaR_95)
print("The mean of the portfolio:", portfolio_mean)
print("The std dev of the portfolio:",portfolio_std)

#lets do some plots
plt.hist(norm.rvs(size=1000000, loc=portfolio_mean, scale=portfolio_std), bins=100)
plt.axvline (x = VaR_95, c= 'r', label = "VaR 95% confidence level")
plt.legend();
plt.show()





