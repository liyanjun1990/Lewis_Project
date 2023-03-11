import pandas as pd
from datetime import datetime , timedelta

df_payrate = pd.read_csv(file_payrate)
df_payrate['Code'] = df_payrate['Code'].astype('string')
df_payrate = df_payrate[['Code','STATUS_1','STATUS_2','STATUS_3']]
df_payrate = df_payrate[df_payrate['STATUS_2']=='Permanent']
list_of_per = df_payrate['Code'].to_list()

df = pd.read_csv(file_path,parse_dates=['Timesheet Date'])
df['Employee Export Code'] = df['Employee Export Code'].astype("string")

print(list(df['Leave Type Name'].unique()))

df['Leave Type Name'] = df['Leave Type Name'].fillna('Working')
df_non_unpaid = df[~df['Leave Type Name'].str.contains('Unpaid')]

print(list(df_non_unpaid['Leave Type Name'].unique()))

# ------ create data_table ------

start_date_string = input('Start Date of Previous Pay Period')
start = datetime.strptime(start_date_string,"%Y-%m-%d")
end = start + timedelta(days=41)

multiplier = [4,9.4,16,31,40,50.5]
multipliers = []
for i in multiplier:
    for j in range(7):
        multipliers.append(i)


date_range = pd.date_range(start=start, end=end)

date_df =  pd.DataFrame()

for i in list_of_per:
    temp_df = pd.DataFrame({"Date_Range":date_range,"Multipliers":multipliers})
    temp_df['Day_name'] = [i.strftime('%a') for i in temp_df['Date_Range']]
    temp_df['Emp_id'] = i
    date_df = pd.concat([date_df,temp_df])

# ------ create data_table  -----
# ------ create normal time -----
df_merge = date_df.merge(df,left_on=['Date_Range','Emp_id'],right_on=['Timesheet Date','Employee Export Code'],how='left')
df_merge['Timesheet Total Time'] = df_merge['Timesheet Total Time'].fillna(0)
df_merge_group_by = df_merge.groupby(['Emp_id','Day_name','Timesheet Total Time'])['Multipliers'].agg('sum').reset_index()
df_merge_group_by_sort = df_merge_group_by.sort_values(by=['Emp_id','Day_name','Multipliers'],ascending=False)
df_merge_group_by_sort_max = df_merge_group_by_sort.drop_duplicates(subset=['Emp_id','Day_name'])

mapping = {'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6,'Sun':7}
df_merge_group_by_sort_max['Day_number'] = df_merge_group_by_sort_max['Day_name'].map(mapping)
Result = df_merge_group_by_sort_max.sort_values(by='Day_number')
Result = Result[['Emp_id','Day_name','Timesheet Total Time']]
Result_Pivot = pd.pivot_table(Result,values='Timesheet Total Time',columns=['Day_name'],index='Emp_id')
Result_Pivot = Result_Pivot[['Mon','Tue','Wed','Thu','Fri','Sat','Sun']]

# ------ create normal time -----
# ------ create alter -----

Result_Pivot['total'] = Result_Pivot[['Mon','Tue','Wed','Thu','Fri','Sat','Sun']].sum(axis=1)
Result_Pivot = Result_Pivot.reset_index()
Result_Pivot_merge = Result_Pivot.merge(df_payrate,left_on='Emp_id',right_on='Code',how='left')
Result_Pivot_merge.to_csv('RH.csv')
