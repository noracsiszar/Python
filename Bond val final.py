#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing libraries
import numpy as np
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

#import 1Yr Austrian Gov bonds data to get an idea how to 1yr term yield 
#changed in the Austrian market over time

# Path to the uploaded CSV file
file_path = 'Austria 1-Year Bond Yield Historical Data.csv'

df = pd.read_csv(file_path, parse_dates=['Date'])

# Display the first few rows of the DataFrame to confirm date parsing
print(df.head())

# Display the data types to confirm the 'Date' column is now datetime type
print(df.dtypes)

# Ensure the Date column is set as the index 
df_with_dates = df.set_index('Date', inplace=True)
#Plot a timeseries chart
plt.plot(df['Yield'], color='blue')
plt.title("Austrian Government bond yields for 1Yr maturity")
plt.show()


# In[12]:


# Create a list of dictionaries for the bonds below as following, where each dictionary 
#represents a bond and its main attributes
bonds_data = [
    {
        "ISIN": "AT0000A2ZQB7",
        "Issuer": "Hypo Wohnbaubank AG",
        "coupon_rate": "2.75",
        "Payment": "annual",
        "Value_date": "2022-08-04",
        "Maturity_date": "2034-08-04",
        "Erstausgabekurs": "101.55",
        "Current_price": "92.95",
        "Next_c": "2024-08-04",
        "remaining_c_payments": "10",
        "AT govt yield": "2.998"
        
    },
    {
        "ISIN": "AT0000A38JE8",
        "Issuer": "Hypo Wohnbaubank AG",
        "coupon_rate": "3.9",
        "Payment": "annual",
        "Value_date": "2023-11-28",
        "Maturity_date": "2035-03-28",
        "Erstausgabekurs": "103",
        "Current_price": "105.4",
        "Next_c": "2024-11-28",
        "remaining_c_payments": "10",
        "AT govt yield": "2.998"
       
    },
    {
        "ISIN": "AT0000A3AZV7",
        "Issuer": "Hypo Wohnbaubank AG",
        "coupon_rate": "3.25",
        "Payment": "annual",
        "Value_date": "2024-03-07",
        "Maturity_date": "2036-03-07",
        "Erstausgabekurs": "99.80",
        "Current_price": "99.80",
        "Next_c": "2025-03-07",
        "remaining_c_payments": "11",
        "AT govt yield": "3.000"
      
    },
    {
        "ISIN": "AT0000A3AZW5",
        "Issuer": "Hypo Wohnbaubank AG",
        "coupon_rate": "3.3",
        "Payment": "annual",
        "Value_date": "2024-03-07",  # Corrected: added comma here
        "Maturity_date": "2036-10-07",
        "Erstausgabekurs": "100.70",
        "Current_price": "92.95",
        "Next_c": "2025-03-07",
        "remaining_c_payments": "12",
        "AT govt yield": "3.173"
      
    }
]

# Convert the list of dictionaries into a DataFrame
bonds_df = pd.DataFrame(bonds_data)

# Display the DataFrame
print(bonds_df)


# In[7]:


#display term structure of current Austrian government bonds, 
#will be used for price calculation of the bonds entered before

austrian_bonds_data = {
    "3 months": 3.805,
    "6 months": 3.727,
    "1 year": 3.480,
    "2 years": 3.144,
    "3 years": 2.945,
    "4 years": 2.872,
    "5 years": 2.866,
    "6 years": 2.864,
    "7 years": 2.888,
    "8 years": 2.931,
    "9 years": 2.963,
    "10 years": 2.998,
    "15 years": 3.173,
    "20 years": 3.198,
    "25 years": 3.190,
    "30 years": 3.127,
    "40 years": 3.216,
    "50 years": 2.899,
    "70 years": 2.967,
    "95 years": 2.930,
    "100 years": 2.317
}
df_govies = pd.DataFrame(list(austrian_bonds_data.items()), columns=['Term', 'Interest Rate'])
print(df_govies)

#plot the data to visualize
plt.plot(df_govies['Term'], df_govies['Interest Rate'])
plt.title("Austrian Government bond yields per maturity")
plt.xlabel("Term")
plt.ylabel("Interest Rate (%)")
plt.xticks(rotation=45)


# In[22]:


#importing datetime for converting maturity date and such into date fomat
import pandas as pd
from datetime import datetime
# Convert columns to numeric
bonds_df['coupon_rate'] = (pd.to_numeric(bonds_df['coupon_rate'], errors='coerce'))
bonds_df['Erstausgabekurs'] = pd.to_numeric(bonds_df['Erstausgabekurs'], errors='coerce')
bonds_df['Current_price'] = pd.to_numeric(bonds_df['Current_price'], errors='coerce')
bonds_df['AT govt yield'] = (pd.to_numeric(bonds_df['AT govt yield'], errors='coerce'))
bonds_df['remaining_c_payments'] = pd.to_numeric(bonds_df['remaining_c_payments'])
# Convert 'Value_date' and 'Maturity_date' to datetime objects
bonds_df['Value_date'] = pd.to_datetime(bonds_df['Value_date'])
bonds_df['Maturity_date'] = pd.to_datetime(bonds_df['Maturity_date'])
bonds_df['Next_c'] = pd.to_datetime(bonds_df['Next_c'])

# Calculate days to next coupon
bonds_df['days_to_next_coupon'] = (bonds_df['Next_c'] - pd.Timestamp.today()).dt.days

# Calculate days to maturity
bonds_df['days_to_maturity'] = (bonds_df['Maturity_date'] - pd.Timestamp.today()).dt.days

# Convert days to years
bonds_df['years_to_next_coupon'] = bonds_df['days_to_next_coupon'] / 365
bonds_df['years_to_maturity'] = bonds_df['days_to_maturity'] / 365

# Calculate number of periods until maturity
bonds_df['frequency'] = bonds_df['Payment'].apply(lambda x: 12 if x == 'monthly' else 1)  # Assuming annual payments
bonds_df['periods'] = bonds_df['years_to_maturity'] * bonds_df['frequency']

# Calculate coupon payment
bonds_df['coupon_payment'] = bonds_df['coupon_rate'] * 100  # Assuming face value of 100

# Estimate YTM
bonds_df['ytm'] = npf.rate(nper=bonds_df['periods'], pmt=bonds_df['coupon_payment'], pv=-bonds_df['Current_price'], fv=100) * bonds_df['frequency'] * 100

# Print or use bonds_df to see the calculated values
print(bonds_df)


# In[23]:


# Duration
# price = -npf.pv(rate=gov yield, nper=remaining payments, pmt=coupon, fv=100)
# price_up = -npf.pv(rate=gov yield+1, nper=remaining payments, pmt=coupon, fv=100)
# price_down = -npf.pv(rate=gov yield-1, nper=remaining payments, pmt=coupon, fv=100)
# duration = (price_down - price_up) / (2 * price * 0.01)

# Calculate the price
bonds_df['int_up'] = bonds_df['AT govt yield'] + 0.01 
bonds_df['int_down'] = bonds_df['AT govt yield'] - 0.01 
bonds_df['price'] = -npf.pv(rate=bonds_df['AT govt yield'], nper=bonds_df['remaining_c_payments'], pmt=bonds_df['coupon_rate'], fv=100)
bonds_df['price_up'] = -npf.pv(rate=bonds_df['int_up'], nper=bonds_df['remaining_c_payments'], pmt=bonds_df['coupon_rate'], fv=100)
bonds_df['price_down'] = -npf.pv(rate=bonds_df['int_down'], nper=bonds_df['remaining_c_payments'], pmt=bonds_df['coupon_rate'], fv=100)
bonds_df['duration'] = (bonds_df['price_down'] - bonds_df['price_up']) / (2 * bonds_df['price'] * 0.01)

# Print or use bonds_df to see the calculated values
print(bonds_df)


# In[24]:


#Plotting maturity in years remaining against duration
plt.plot(bonds_df['years_to_maturity'], bonds_df['duration'])
plt.xlabel('Maturity (Years)')
plt.ylabel('Duration (%)')
plt.title("Effect of Varying Maturity On Bond Duration")
plt.show()


# In[25]:


#Dollar Duration = Duration × Bond Price × 0.01
#DV01 = dollar duration/100
bonds_df['dollar_duration'] = bonds_df['duration'] * bonds_df['Current_price'] * 0.01
bonds_df['DV01'] = bonds_df['dollar_duration'] /100
print(bonds_df)


# In[26]:


# Hedging DV01 example
#Your existing portfolio has a DV01 of EUR 10,000 -> number of bonds to sell to hedge EUR 10,000 DV01
bonds_df['hedge_quantity'] = round(10000 / bonds_df['DV01'])
print(bonds_df)


# In[27]:


#What is convexity?
#Measures the curvature of bond prices
#Used to improve bond price prediction and risk measurement
#Higher convexity = more curved price/yield relationship
bonds_df['Convexity'] =  (bonds_df['price_down'] + bonds_df['price_up'] - 2 * bonds_df['price']) / (bonds_df['price'] * 0.01 ** 2)
print(bonds_df)


# In[ ]:




