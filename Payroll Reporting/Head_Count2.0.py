import pandas as pd
from datetime import datetime, timedelta


def fte(DAte):
    weekdays_count = 0
    if DAte.month != 12:
        date_year = DAte.year
        date_month = DAte.month + 1
    else:
        date_year = DAte.year + 1
        date_month = 1

    date_loop = datetime(date_year,date_month,1) - timedelta(days=1)
    for i in range(1,date_loop.day+1):
        if datetime(date_loop.year,date_loop.month,i).weekday() < 5:
            weekdays_count = weekdays_count + 1
    return weekdays_count  * 7.6

Deputy_Dep_file = r"C:\Users\admin\Desktop\work\PTC\Report\Deputy_Dep.csv"

Deputy_Dep_df = pd.read_csv(Deputy_Dep_file,dtype='object')
Deputy_Dep_df= Deputy_Dep_df.sort_values(by=['id_x'],ascending=True)
Deputy_Dep_df= Deputy_Dep_df.drop_duplicates(subset=['DisplayName'],keep='last')

Deputy_Dep_df = Deputy_Dep_df[['DisplayName','PayrollId','Created','TerminationDate','CompanyName']]
Deputy_Dep_df = Deputy_Dep_df.dropna(subset=["PayrollId"])
Deputy_Dep_df['Created'] = [i[:10] for i in Deputy_Dep_df['Created']]
Deputy_Dep_df['Created'] = Deputy_Dep_df['Created'].astype("datetime64[ns]")

Deputy_Dep_df['TerminationDate'] = Deputy_Dep_df['TerminationDate'].fillna("2099-12-31")
Deputy_Dep_df['TerminationDate'] = [i[:10] for i in Deputy_Dep_df['TerminationDate']]
Deputy_Dep_df['TerminationDate'] = Deputy_Dep_df['TerminationDate'].astype("datetime64[ns]")

period = input('Period_string')

period_date = datetime.strptime(period,"%Y%m")
period_date_EOM = period_date + timedelta(days=32) - timedelta(days=(period_date + timedelta(days=32)).day)

#Deputy_Dep_df.to_csv(r'C:\Users\admin\Desktop\work\PTC\Report\result.csv')
Deputy_Dep_df_monthly = Deputy_Dep_df[(Deputy_Dep_df['Created']<=period_date_EOM) & (Deputy_Dep_df['TerminationDate']>=period_date)]

detail_file = r"C:\Users\admin\Desktop\work\PTC\Report\Detail.xlsx"

detail_df = pd.read_excel(detail_file,engine='openpyxl')
detail_df = detail_df.dropna(subset=['Display Name'])
detail_df = detail_df[~(detail_df['Display Name']=='PH')]

detail_df_monthly = detail_df[(detail_df['Timesheet Date']>= period_date) & (detail_df['Timesheet Date']<= period_date_EOM)]
detail_df_monthly['Employee Export Code'] = detail_df_monthly['Employee Export Code'].astype('string')
detail_df_monthly['Employment Type 2'] = [detail_df_monthly['Employment Type'].iloc[j] if i =='Permanent' else detail_df_monthly['Employment Type 2'].iloc[j] for j,i in enumerate(detail_df_monthly['Employment Type 2'])]

# most_location
detail_df_most_location = detail_df_monthly[['Employee Export Code','Location','Timesheet Total Time']]\
                            .groupby(['Employee Export Code','Location'])['Timesheet Total Time'].agg('sum')
detail_df_most_location = detail_df_most_location.reset_index()
detail_df_most_location['Percentage'] = detail_df_most_location['Timesheet Total Time'] / detail_df_most_location.groupby('Employee Export Code')['Timesheet Total Time'].transform('sum')
# add fte
Fte = fte(period_date)
detail_df_most_location['FTE'] = detail_df_most_location['Timesheet Total Time'] / Fte
detail_df_most_location = detail_df_most_location[['Employee Export Code','Location','Percentage','FTE']]


#detail_df_most_location = detail_df_most_location.sort_values(['Employee Export Code','Timesheet Total Time'])
#detail_df_most_location = detail_df_most_location.drop_duplicates(subset='Employee Export Code',keep='last')[['Employee Export Code','Location']]


# most recent status
detail_df_most_status = detail_df_monthly[['Employee Export Code','Timesheet Date','Employment Type 2']].sort_values(['Timesheet Date'])
detail_df_most_status = detail_df_most_status.drop_duplicates(subset='Employee Export Code',keep='last')[['Employee Export Code','Employment Type 2']]
detail_df_most_status = detail_df_most_status[['Employee Export Code','Employment Type 2']]

# merge
Deputy_merge_monthly = Deputy_Dep_df_monthly.merge(detail_df_most_location,left_on='PayrollId',right_on='Employee Export Code',how='left',suffixes=('', '_y'))
Deputy_merge_monthly = Deputy_merge_monthly.merge(detail_df_most_status,left_on='PayrollId',right_on='Employee Export Code',how='left',suffixes=('', '_y'))
Deputy_merge_monthly['Location'] = Deputy_merge_monthly['Location'].fillna('Not Working')
Deputy_merge_monthly['Percentage'] = Deputy_merge_monthly['Percentage'].fillna(1)
Deputy_merge_monthly = Deputy_merge_monthly[['DisplayName','PayrollId','Created','TerminationDate','Percentage','Location','Employment Type 2','FTE']]
Deputy_merge_monthly['Period'] = period
Deputy_merge_monthly.to_csv(f'{period}_FTE.csv',index=False)
