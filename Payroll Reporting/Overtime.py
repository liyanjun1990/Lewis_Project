import pandas as pd
import numpy as np
import time
from datetime import datetime

today_string = datetime.now().date().strftime("%Y-%m-%d")

file_path = input('file_full_path, payrun')

deputy_df = pd.read_excel(file_path,sheet_name='Deputy Timesheet',usecols="A:N",skiprows=1,dtype=object,parse_dates=['Timesheet Date'])
deputy_df = deputy_df.dropna(subset=['Display Name','Area Name'])
deputy_df['Timesheet Total Time'] = deputy_df['Timesheet Total Time'].astype('float')
needed_column = ['Timesheet Date','Employee Export Code','Timesheet Total Time','Area Name']
deputy_df = deputy_df[needed_column]

PH_df = pd.read_excel(file_path,sheet_name='Public Holiday',usecols="A:F",dtype=object,parse_dates=['Date'])
PH_df.dropna(subset=['Code'])
PH_df = PH_df[PH_df['Category']=="NW"]
PH_df = PH_df.rename(columns={"Code":"Employee Export Code",'Date':"Timesheet Date","Add Hours":"Timesheet Total Time"})
PH_df['Timesheet Total Time'] = PH_df['Timesheet Total Time'].astype('float')
PH_df['Area Name'] = "Paid Non-Work Hours"
PH_df = PH_df[needed_column]

Final_Timesheet = pd.concat([deputy_df,PH_df])

display_name_df = pd.read_excel(file_path,sheet_name='Most_Location',usecols="B:C,I",dtype=object)
display_name_df = display_name_df.dropna(subset=['PayrollId'])
display_name_df = display_name_df.drop_duplicates(subset=['PayrollId'])

merge_display_name = Final_Timesheet.merge(display_name_df,how='left',left_on='Employee Export Code',right_on='PayrollId')

status_df = pd.read_excel(file_path,sheet_name='Rate',usecols="B,S:T",dtype=object)
merge_display_name = merge_display_name.merge(status_df,how='left',left_on='Employee Export Code',right_on='Code')

needed_column = ['DisplayName','STATUS_2','STATUS_3','Timesheet Date','Employee Export Code','Timesheet Total Time','Area Name','CompanyName']
merge_display_name = merge_display_name[needed_column]

merge_display_name['Total Hours'] = merge_display_name.groupby(['Employee Export Code'])['Timesheet Total Time'].transform("sum")
# RT Only
merge_display_name = merge_display_name[merge_display_name['CompanyName'].str.contains("#|Manager|Training",regex=True)]

merge_display_name_overtime = merge_display_name[merge_display_name['Total Hours'] > 76].sort_values(by=['Employee Export Code','Timesheet Date'])
merge_display_name_overtime =  merge_display_name_overtime.drop(columns=['CompanyName'])

merge_display_name_overtime_summary = merge_display_name_overtime.drop(columns=['Timesheet Date','Timesheet Total Time','Area Name'])
merge_display_name_overtime_summary = merge_display_name_overtime_summary.drop_duplicates(subset=['Employee Export Code']).sort_values(by=['Total Hours'],ascending=False)

with pd.ExcelWriter(f'{today_string} Overtime.xlsx',engine='openpyxl') as writer:
    merge_display_name_overtime_summary.to_excel(writer,sheet_name='Summary',index=False)
    merge_display_name_overtime.to_excel(writer,sheet_name='Detail',index=False)


