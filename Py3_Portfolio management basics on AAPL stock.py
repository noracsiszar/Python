#!/usr/bin/env python
# coding: utf-8

# In[43]:


#importing data and calculating returns
#Discrete returns are calculated as the change in price as a percentage of the previous period's price
#Log returns are calculated as the difference between the log of two prices 
#Logreturns aggregate across time,while discrete returns aggregate across assets
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #importing for plots
from scipy.stats import skew #importing for skewness
from scipy.stats import kurtosis #importing for kurtosis
from scipy import stats #testing null hypothesis if data is normally distributed

# Fetch historical data
ticker_symbol_1 = 'AAPL'
appl = yf.Ticker(ticker_symbol_1)
historical_data_appl = appl.history(period="2y")

# Extract relevant columns
daily_prices_aapl = historical_data_appl[['Open', 'High', 'Low', 'Close', 'Volume']]

# Convert the index to a string format (YYYY-MM-DD)
daily_prices_aapl.index = daily_prices_aapl.index.strftime('%Y-%M-%d')

# Add daily returns
daily_prices_aapl.loc[:, "Returns"] = daily_prices_aapl["Close"].pct_change()

# Display the transformed data frame
print(daily_prices_aapl.tail())


# In[24]:


#visualizing return distributions
plt.hist(daily_prices_aapl["Returns"].dropna(), bins=100, density=False)
plt.show()


# In[47]:


#calculating mean, var, kurtosis and skewness of the distribution
mean_return = np.mean(daily_prices_aapl["Returns"])
#annulized mean
annulized_mean = ((1+np.mean(daily_prices_aapl["Returns"]))**252)-1
#std dev
std_deviation = np.std(daily_prices_aapl["Returns"])
#variance
var_return = np.std(daily_prices_aapl["Returns"])**2
#annulized volatility
annulized_vol = np.std(daily_prices_aapl["Returns"]) * np.sqrt(252)
#skewness
skew_1 = skew(daily_prices_aapl["Returns"].dropna())
#kurtosis
kurt_1 = kurtosis(daily_prices_aapl["Returns"].dropna())

#printing out 
print(f"Mean: {mean_return}")
print(f"Mean annulized: {annulized_mean}")
print(f"Standard deviation: {std_deviation}")
print(f"Variance: {var_return}")
print(f"Annulized volatility: {annulized_vol}")
print(f"Skewness: {skew_1}")
print(f"Kurtosis: {kurt_1}")


# In[46]:


#is the data normally distributed

p_value = stats.shapiro(daily_prices_aapl["Returns"].dropna())[1]
if p_value <= 0.05:
    print("Null hypothesis of normality is rejected, not a normal distribution.")
else:
    print("Null hypothesis of normality is accepted.")


# In[ ]:




