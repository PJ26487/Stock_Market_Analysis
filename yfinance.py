import yfinance as yf
from datetime import datetime
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import dateutil.relativedelta
import streamlit as st


current_month = datetime.now().month
current_year = datetime.now().year
current_day = datetime.now().day
current_date = str(current_year)+'-'+str(current_month)+'-'+str(current_day)
current_date = pd.to_datetime(current_date)
print(current_date)
name = name
start = current_date - dateutil.relativedelta.relativedelta(month = 1)
end = current_date
stock_df = yf.download(name,
                      start=start,
                      end=end,
                      progress=False)

stock_df['date'] = stock_df.index
# using the ticker to get more information
tsla = yf.Ticker(name)
print('the major shareholders are')
df_share = tsla.major_holders
df_recom = tsla.recommendations
df_options = tsla.options
df_sus = tsla.sustainability

start = pd.to_datetime(start)
start = start.to_pydatetime()

# filtering the dfs
df_recom = df_recom.tail(20)

#df_sus = df_sus[df_sus['']]
print(tsla.major_holders)
print(' ')
print('Recommendations')
print(df_recom)
print(' ')
print('Options')
print(tsla.options)
print('')
st.write(tsla.major_holders)
st.table(df_recom)
st.write(tsla.options)
st.pyplot(stock_df.plot(x ='date', y ='Close',kind = 'line'))
