import pandas as pd
import os
from datetime import datetime
import re
import numpy as np

file_path = input("file_path") + "\\"

df = pd.DataFrame()
for i in os.listdir(file_path):
    temp = pd.read_csv(file_path + i)
    df = pd.concat([df,temp])
    print(i,"Done")

# Upper the case
df['Description'] = [i.upper() for i in df['Description']]
df.to_csv(file_path + f'combine.csv')
# Combine all


# DEPOSIT
df['Process date'] = [datetime.strptime(i,'%d/%m/%Y') for i in df['Process date']]

deposit_from_str = input("deposit_from,YYYY-MM-DD")
deposit_from = datetime.strptime(deposit_from_str,'%Y-%m-%d')
deposit_to_str = input("deposit_to,YYYY-MM-DD")
deposit_to = datetime.strptime(deposit_to_str,'%Y-%m-%d')

df_deposit = df[(df['Process date']>=deposit_from) & (df['Process date']<=deposit_to)]
df_deposit.to_csv(file_path + f'{deposit_from_str}_{deposit_to_str}deposit.csv')

# CASH
cash_from_str = input("cash_from,YYYY-MM-DD")
cash_from = datetime.strptime(cash_from_str,'%Y-%m-%d')
cash_to_str = input("cash_to,YYYY-MM-DD")
cash_to = datetime.strptime(cash_to_str,'%Y-%m-%d')

df_cash = df[(df['Process date']>=cash_from) & (df['Process date']<=cash_to)]
df_cash['Description'] = [i if re.search("CASH",i) else np.nan for i in df_cash['Description']]
df_cash = df_cash.dropna(subset=['Description'])
df_cash.to_csv(file_path + f'{cash_from_str}_{cash_to_str}cash.csv')