#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Welcome to the FX spot market game!")
name = input("Enter your name: ")
print(f"Hello, {name}! In case of error, the computer will guide you through this simulation.")
print("Get ready!")


# In[2]:


print("----------------------------------------------------------------------------")
print("Your bank has the current FX gaps reported by the Market risk unit in USD m:")
print("For simplicity, we will assume a 100% hedge ratio while creating the hedges.")


# In[3]:


import pandas as pd

FXgaps = {
    "EUR": -10,
    "GBP": +15,
    "CHF": -9
}

df_fxgaps = pd.DataFrame(list(FXgaps.items()), columns=['CCY', 'GAP in USD m'])
print(df_fxgaps)


# In[4]:


CCYconv = {
    "USD_EUR": [0.9282, 0.9286],
    "USD_GBP": [0.7984, 0.7987],
    "USD_CHF": [0.9063, 0.9067]
}

df_ccyconv = pd.DataFrame(list(CCYconv.items()), columns=['CCYpair', 'bid_ask'])
df_ccyconv[['bid', 'ask']] = pd.DataFrame(df_ccyconv['bid_ask'].tolist(), index=df_ccyconv.index)
df_ccyconv.drop(columns=['bid_ask'], inplace=True)
print("Here is the overview of the current market rates:")
print("-------------------------------------------------")
print(df_ccyconv)


# In[5]:


while True:
    print("----------------------------------------------------------------------------")
    print("The market user buys USD at ask and sells USD at ask.")
    print("To close the USD gap in EUR with -10mn USD, would you like to buy or sell USD?")
    print("1) buy USD")
    print("2) sell USD")
    buyorsell = input("Enter 1 or 2: ")

    if buyorsell == '1':
        print("You will buy USD.")
        print("The current market price is 1 USD = 0.9286 EUR.")
        print("You buy 10m USD. This equals to 0.9286*10.000.000 = -9.286m EUR")
        df_fxgaps.loc[df_fxgaps['CCY'] == 'EUR', 'Hedge Position'] = df_fxgaps.loc[df_fxgaps['CCY'] == 'EUR', 'GAP in USD m'] * -1
        break  # Exit the loop after one round of transactions
    else:
        print("You chose to sell USD.")
        print("However, we are already short.")
        print("Therefore you need to buy USD.")

    print(df_fxgaps)

    print("Wanna start again? Type 'y' for yes.")
    restart = input()
    if restart.lower() != 'y':
        print("Exiting...")
        break  # Exit the loop if the user chooses not to restart


# In[6]:


while True:
    print("----------------------------------------------------------------------------")
    print("The market user buys USD at ask and sells USD at ask.")
    print("To close the USD gap in GBP with +15mn USD, would you like to buy or sell USD?")
    print("1) buy USD")
    print("2) sell USD")
    buyorsell = input("Enter 1 or 2: ")

    if buyorsell == '2':
        print("You will sell USD.")
        print("The current market price is 1 USD = 0.9286 GBP.")
        print("You sell 15m USD. This equals to 0.7984*15.000.000 = +11.976m GBP")
        df_fxgaps.loc[df_fxgaps['CCY'] == 'GBP', 'Hedge Position'] = df_fxgaps.loc[df_fxgaps['CCY'] == 'GBP', 'GAP in USD m'] * -1
        break  # Exit the loop after one round of transactions
    else:
        print("You chose to buy USD.")
        print("However, we are already long.")
        print("Therefore you need to sell USD.")

    print(df_fxgaps)

    print("Wanna start again? Type 'y' for yes.")
    restart = input()
    if restart.lower() != 'y':
        print("Exiting...")
        break  # Exit the loop if the user chooses not to restart


# In[7]:


while True:
    print("----------------------------------------------------------------------------")
    print("The market user buys USD at ask and sells USD at ask.")
    print("To close the USD gap in CHF with -9mn USD, would you like to buy or sell USD?")
    print("1) buy USD")
    print("2) sell USD")
    buyorsell = input("Enter 1 or 2: ")

    if buyorsell == '1':
        print("You will buy USD.")
        print("The current market price is 1 USD = 0.9067 CHF.")
        print("You buy 9m USD. This equals to 0.9067*9.000.000 = -8.16m CHF")
        df_fxgaps.loc[df_fxgaps['CCY'] == 'CHF', 'Hedge Position'] = df_fxgaps.loc[df_fxgaps['CCY'] == 'CHF', 'GAP in USD m'] * -1
        break  # Exit the loop after one round of transactions
    else:
        print("You chose to sell USD.")
        print("However, we are already short.")
        print("Therefore you need to buy USD.")

    print(df_fxgaps)

    print("Wanna start again? Type 'y' for yes.")
    restart = input()
    if restart.lower() != 'y':
        print("Exiting...")
        break  # Exit the loop if the user chooses not to restart


# In[8]:


#update table with net position
df_fxgaps['Net Position'] = df_fxgaps['GAP in USD m'] + df_fxgaps['Hedge Position']
print(df_fxgaps)


# In[9]:


FXrates = {
    "USD_EUR": [0.9284, 0.9289],
    "USD_GBP": [0.7987, 0.7990],
    "USD_CHF": [0.9061, 0.9068]
}
df_fx_rates_eod = pd.DataFrame(list(FXrates.items()), columns=['CCYpair', 'bid_ask'])
df_fx_rates_eod[['bid', 'ask']] = pd.DataFrame(df_fx_rates_eod['bid_ask'].tolist(), index=df_fx_rates_eod.index)
df_fx_rates_eod.drop(columns=['bid_ask'], inplace=True)

if sum(df_fxgaps['Net Position']) == 0:
    print("You successfully closed all the FX Gaps.")
    print("Let's see what is the PnL of the position at the end of the day depending on the market closing.")
    print(df_fx_rates_eod)
    
    # Creating DataFrame
    execution_rates_data = {
        "CCY": ["EUR", "GBP", "CHF"],
        "execution_rate": [0.9286, 0.7984, 0.9063]  # Assuming the execution rates
    }
    df_execution_rates = pd.DataFrame(execution_rates_data)

    # Ensure proper mapping of execution rates to currencies
    df_fxgaps['executed_rates'] = df_execution_rates.set_index('CCY')['execution_rate'][df_fxgaps['CCY']].values

print(df_fxgaps)


# In[10]:


# Calculate the difference between end-of-day rate and execution rate
df_fxgaps['diff_eod_price_minus_price_fixed'] = 0  # Initialize the column

# For EUR and CHF
eur_chf_mask = df_fxgaps['CCY'].isin(['EUR', 'CHF'])
df_fxgaps.loc[eur_chf_mask, 'diff_eod_price_minus_price_fixed'] = df_fx_rates_eod.loc[eur_chf_mask, 'ask'] - df_fxgaps.loc[eur_chf_mask, 'executed_rates']

# For GBP
gbp_mask = df_fxgaps['CCY'] == 'GBP'
df_fxgaps.loc[gbp_mask, 'diff_eod_price_minus_price_fixed'] = df_fx_rates_eod.loc[gbp_mask, 'bid'] - df_fxgaps.loc[gbp_mask, 'executed_rates']

# Calculate PnL based on the difference and net position
df_fxgaps['PnL Hedge Position eod'] = df_fxgaps['diff_eod_price_minus_price_fixed'] * df_fxgaps['Hedge Position']

# Print the DataFrame showing the end-of-day rates and PnL
print("End of Day Rates:")
print(df_fx_rates_eod)
print("\n")
print("Profit and Loss (PnL):")
print(df_fxgaps[['CCY', 'Hedge Position', 'diff_eod_price_minus_price_fixed', 'PnL Hedge Position eod']])


# In[ ]:




