import os
import pandas as pd
from datetime import datetime

# vend download
df = pd.DataFrame()
for i in os.listdir(path):
    temp_df = pd.read_csv(path+i)
    df = pd.concat([df,temp_df])

# Fix the close late problem
df['Opened_Time'] = ["AM" if int(i[11:13]) <12 else "PM" for i in df['Opened']]
df['Closed_Time'] = ["AM" if int(i[11:13]) <12 else "PM" for i in df['Closed']]

df['Opened_Date'] = [datetime.strptime(i[:10],'%Y-%m-%d') for i in df['Opened']]
df['Close_Date'] = [datetime.strptime(i[:10],'%Y-%m-%d') for i in df['Closed']]

for i in range(len(df)):
    if df['Opened_Date'].iloc[i] != df['Close_Date'].iloc[i] and df['Closed_Time'].iloc[i] == "AM":
        df['Close_Date'].iloc[i] = df['Opened_Date'].iloc[i]

df['Opened'] = df['Opened_Date']
df['Closed'] = df['Close_Date']

df.drop(['Opened_Time','Closed_Time','Opened_Date','Close_Date'],axis=1,inplace=True)

# chang the from and to
date_from_str = input('Date_from')
#date_from_str = '2022-06-06'
date_to_str = input('Date_to')
#date_to_str = '2022-06-12'
date_from = datetime.strptime(date_from_str,'%Y-%m-%d')
date_to = datetime.strptime(date_to_str,'%Y-%m-%d')

#df['Opened'] = [datetime.strptime(i[:10],'%Y-%m-%d') for i in df['Opened']]
#df['Closed'] = [datetime.strptime(i[:10],'%Y-%m-%d') for i in df['Closed']]
df = df[(df['Opened']>=date_from) & (df['Closed']<=date_to)]
df = df.sort_values(by=['Opened'])

df['merge_helper'] = [i + str(j) for i,j in zip(df['Register'],df['Sequence'])]

if df['merge_helper'].is_unique == False:
    print('NOT UNI')
    exit()


df_url = pd.read_csv(combine_path)

if df_url['merge_helper'].is_unique == False:
   print('NOT UNI')
   exit()


df = df.merge(df_url[['merge_helper','href']],left_on='merge_helper',right_on='merge_helper',how='left')

print(df.columns)

df.to_csv(f'{date_from_str}_{date_to_str}_original_vend.csv',index=False)

needed_column  = ['Register', 'Sequence', 'Opened', 'Closed', 'Cash rounding Amount',
       'Cash rounding Posted', 'Cash Amount', 'Cash Posted',
       'Credit Card Amount', 'Credit Card Posted', 'Store Credit Amount',
       'Store Credit Posted', 'Gift Card Amount', 'Gift Card Posted',
       'CommBank Amount', 'CommBank Posted',
       'Other Payment (Wechat Pay or Alipay) Amount',
       'Other Payment (Wechat Pay or Alipay) Posted',
       'PTC Bank Transfer(CONTACT HO)  Amount',
       'PTC Bank Transfer(CONTACT HO)  Posted', 'Online Amount',
       'Online Posted', 'Zip Pay Amount', 'Zip Pay Posted', 'Groupon Amount',
       'Groupon Posted', 'Pay ID Amount',
       'Pay ID Posted',
       'Other Payment Method Amount', 'Other Payment Method Posted',
       'Shop Purchase* Amount', 'Shop Purchase* Posted', 'Total',
       'merge_helper', 'href']

df[needed_column].to_csv(f'{date_from_str}_{date_to_str}vend.csv',index=False)
