#!/usr/bin/env python
# coding: utf-8

# In[34]:


#Technical stock analysis in Python in talib library
#getting data from yahoofinance for AAPL, CVX, KO, JNJ and PG
get_ipython().system('pip install plotly')
get_ipython().system('pip install ta-lib')
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import talib
import numpy as np
from scipy.stats import norm



ticker_symbol_1 = 'AAPL'
appl = yf.Ticker(ticker_symbol_1)
historical_data_appl = appl.history(period="2y")
daily_prices_aapl = historical_data_appl[['Open', 'High', 'Low', 'Close', 'Volume']]

# Convert the index to a string format (YYYY-MM-DD)
daily_prices_aapl.index = daily_prices_aapl.index.strftime('%Y-%m-%d')
# Display the transformed data frame
print(daily_prices_aapl.head())


# In[10]:


#Plot a timeseries chart
plt.plot(daily_prices_aapl['Close'], color='red')
plt.title("Daily close price")
plt.show()


# In[11]:


#Plotting a candlestick chart: for this, plotly has to be installed and plothy graph objects has to be imported
#Define the candlestick
candlestick = go.Candlestick(x = daily_prices_aapl.index,
                             open = daily_prices_aapl['Open'], 
                             high = daily_prices_aapl['High'],
                             low = daily_prices_aapl['Low'], 
                             close = daily_prices_aapl['Close'])
# Create a plot  
fig = go.Figure(data=[candlestick])
# Show the plot
fig.show()


# In[14]:


#Compute daily asset returns 
daily_returns = daily_prices_aapl.pct_change()


# In[20]:


#Simple moving average(SMA):arithmetic mean price over a specied n-period 
daily_prices_aapl['sma_3'] = daily_prices_aapl['Close'].rolling(window=3).mean() 
# Display the first few rows, but until there are no 50 datapoints, the sma will be empty
print(daily_prices_aapl.head())


# In[22]:


#plot the 50 rolling average
plt.plot(daily_prices_aapl['Close'], label='Close')
plt.plot(daily_prices_aapl['sma_50'], label='SMA_50')
plt.legend()
plt.show()


# In[36]:


# Calculate two SMAs, for this ta-lib has to be installed
daily_prices_aapl.loc[:, 'SMA_short'] = talib.SMA(daily_prices_aapl['Close'], timeperiod=10)
daily_prices_aapl.loc[:, 'SMA_long'] = talib.SMA(daily_prices_aapl['Close'], timeperiod=50)
# Print the last five rows
print(daily_prices_aapl.tail())


# In[37]:


#Plotting the SMAs
#Plot SMA with the price
plt.plot(daily_prices_aapl['SMA_short'],label='SMA_short')
plt.plot(daily_prices_aapl['SMA_long'], label='SMA_long')
plt.plot(daily_prices_aapl['Close'],label='Close')
plt.legend()
plt.title('SMAs')
plt.show()


# In[38]:


#calculate exponential moving average
daily_prices_aapl.loc[:, 'EMA_short'] = talib.EMA(daily_prices_aapl['Close'], timeperiod=10)
daily_prices_aapl.loc[:, 'EMA_long'] = talib.EMA(daily_prices_aapl['Close'], timeperiod=50)
# Print the last five rows
print(daily_prices_aapl.tail())                    


# In[39]:


#Plotting the EMAs
#Plot EMA with the price
plt.plot(daily_prices_aapl['EMA_short'],label='EMA_short')
plt.plot(daily_prices_aapl['EMA_long'], label='EMA_long')
plt.plot(daily_prices_aapl['Close'],label='Close')
plt.legend()
plt.title('EMAs')
plt.show()


# In[40]:


#calculating ADX (Average Directional Movement Index)
daily_prices_aapl.loc[:, 'ADX'] = talib.ADX(daily_prices_aapl['High'], daily_prices_aapl['Low'], daily_prices_aapl['Close'], timeperiod=14)
# Print the last five rows
print(daily_prices_aapl.tail())                                     


# In[41]:


#plotting ADX
#Create subplots
fig, (ax1, ax2) = plt.subplots(2)
# Plot ADX with the price
ax1.set_ylabel('Price')
ax1.plot(daily_prices_aapl['Close'])
ax2.set_ylabel('ADX')
ax2.plot(daily_prices_aapl['ADX'])
ax1.set_title('Price and ADX')
plt.show()


# In[42]:


# Calculate RSI
daily_prices_aapl.loc[:, 'RSI'] = talib.RSI(daily_prices_aapl['Close'], timeperiod=14)
# Print the last five rows
print(daily_prices_aapl.tail())  


# In[43]:


#plotting RSI
# Create subplots
fig, (ax1, ax2) = plt.subplots(2)
# Plot RSI with the price
ax1.set_ylabel('Price')
ax1.plot(daily_prices_aapl['Close'])
ax2.set_ylabel('RSI')
ax2.plot(daily_prices_aapl['RSI'])
ax1.set_title('Price and RSI')
plt.show()


# In[44]:


# Define the Bollinger Bands
upper, mid, lower = talib.BBANDS(daily_prices_aapl['Close'], nbdevup=2, nbdevdn=2, timeperiod=20)


# In[45]:


# Plot the Bollinger Bands 
plt.plot(daily_prices_aapl['Close'],label='Price')
plt.plot(upper, label="Upper band")
plt.plot(mid, label='Middle band')
plt.plot(lower, label='Lower band')
plt.title('Bollinger Bands')
plt.legend()
plt.show()


# In[ ]:




