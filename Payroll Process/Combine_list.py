import sys
import csv
import numpy as np
import pandas as pd
from dbfread import DBF
import os
from datetime import datetime

last_payrun_day = input("Payunrun Last Day: YYYY-MM-DD")
last_payrun_day = datetime.strptime(last_payrun_day,"%Y-%m-%d")


def get_rates(file_path,company):
    table = DBF(file_path,ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))
    df = df[df['PAYNUM']==0]
    needed_cloumn = ['STAFF_CODE', 'HOUR_RATE1', 'HOUR_RATE2', 'HOUR_RATE3', 'HOUR_RATE4', 'HOUR_RATE5',
                     'SALARY']
    df = df[needed_cloumn]
    df['Company_Rate'] = company
    df['STAFF_CODE_Company'] =  df['STAFF_CODE'].apply(lambda x: str(x)) +df['Company_Rate']

    return df

def get_staff(file_path,company):
    table = DBF(file_path,ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))

    needed_cloumn = ['CODE','ALPHA_SORT','LAST_NAME','FIRST_NAME','PER_CASUAL','FULL_PART','CURRENT',
                 'START_DATE','BIRTH_DATE','DEPARTMENT','HOL_GROUP','SALARY_WAG',
                 'HOL_BF_D','HOL_CY_GR','HOL_CY_ND','HOL_CY_D','HOL_CY_AD','HOL_CY_AA',
                 'SICK_BAL','SICK_OUT','SICK_ADV',
                 'DEFAULT_CC','STEMAIL','TFNNUMBER','FINISH','MOBILE','ADDRESS','SUBURB','CITY','POSTCODE'
                 ]
    df = df[needed_cloumn]
#    df = df[df['CURRENT'] == True]
    df['Company'] = company
    df['CODE_Company'] = df['CODE'].apply(lambda x: str(x)) + df['Company']
    df['CODE_Company_DCC'] = df['DEFAULT_CC'].apply(lambda x: str(x)) + df['Company']
    return df

def get_leaveent(file_path,company):
    table = DBF(file_path,ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))
    needed_cloumn = ['ENTID', 'STAFF_CODE', 'STARTDATE', 'ENDDATE', 'LGCODE', 'LGTYPE']
    df = df[needed_cloumn]
    df = df.astype({'STARTDATE': 'datetime64[ns]', 'ENDDATE': 'datetime64[ns]'})
    df = df[(df['LGTYPE'] == 'H') &
                        (df['STARTDATE'] <= last_payrun_day) &
                        (df['ENDDATE'] >= last_payrun_day)]
    df['Annual Leave  Group'] = df['LGCODE'].apply(lambda x: 1.175 if x.strip() =="AL" else 1)
    needed_cloumn = ['STAFF_CODE', 'Annual Leave  Group']
    df = df[needed_cloumn]
    df['Company_leave'] = company
    df['STAFF_CODE_Company_leave'] =  df['STAFF_CODE'].apply(lambda x: str(x)) +df['Company_leave']

    return df

def getcostcnter(file_path,company):

    table = DBF(file_path,ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))

    needed_cloumn = ['CODE','NAME','CCSTATE'
                 ]
    df = df[needed_cloumn]
    df['Company'] = company
    df['CODE_Company_CC'] = df['CODE'].apply(lambda x: str(x)) + df['Company']
    # remove company column
    df = df[['CODE','NAME','CCSTATE','CODE_Company_CC']]
    return df

def get_super(file_path,company):

    table = DBF(file_path,ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))
    df = df[df['PNPAYNUM'] == 0]
    needed_cloumn = ['PNSTAFF','PNCOSTCENT']
    df = df[needed_cloumn]
    df['Company'] = company
    df['Code_Super_Company'] = df['PNSTAFF'].apply(lambda x: str(x)) + df['Company']
    # remove company column
    df = df[['PNSTAFF','PNCOSTCENT','Company','Code_Super_Company']]
    return df

df_cc = pd.DataFrame()
for i in dict_of_cc.keys():
    df_temp = getcostcnter(dict_of_cc[i],i)
    df_cc = pd.concat([df_cc,df_temp])


df_rate = pd.DataFrame()
for i in dict_of_rate_path.keys():
    df_temp = get_rates(dict_of_rate_path[i],i)
    df_rate = pd.concat([df_rate,df_temp])

df_staff = pd.DataFrame()
for i in dict_of_staff_path.keys():
    df_temp = get_staff(dict_of_staff_path[i],i)
    df_staff = pd.concat([df_staff,df_temp])

df_staff.to_csv(out_path + 'all.csv')
df_staff = df_staff[df_staff['CURRENT'] == True]

df_leave = pd.DataFrame()
for i in dict_of_leave_path.keys():
    df_temp = get_leaveent(dict_of_leave_path[i],i)
    df_leave = pd.concat([df_leave,df_temp])

df_cc = pd.DataFrame()
for i in dict_of_cc.keys():
    df_temp = getcostcnter(dict_of_cc[i],i)
    df_cc = pd.concat([df_cc,df_temp])

df_super = pd.DataFrame()
for i in dict_of_super.keys():
    df_temp = get_super(dict_of_super[i], i)
    df_super = pd.concat([df_super, df_temp])

# check employee_cost_center
df_wage_cc = df_staff[['CODE','DEFAULT_CC','CODE_Company']].to_csv('wage_cc.csv')
#print(df_wage_cc[(df_wage_cc['DEFAULT_CC']%2)==0])
df_super.to_csv('super.csv')
#print(df_super[(df_super['PNCOSTCENT']%2)== 1])

# ETL staff table
df_staff['Code'] = df_staff['CODE']
df_staff['Alpha Code'] = df_staff['ALPHA_SORT']
df_staff['Name'] = df_staff['LAST_NAME'] + ',' + df_staff['FIRST_NAME']
df_staff['Start Date'] = df_staff['START_DATE']
df_staff['Department'] = df_staff['DEPARTMENT']
df_staff['Employment  Status'] = df_staff['PER_CASUAL'].map({1:'Permanent',2:'Casual'})
df_staff['Salary/ Wage'] = df_staff['SALARY_WAG'].map({1:'Salary',2:'Wages'})
df_staff['Birth Date'] = df_staff['BIRTH_DATE']
df_staff['STATUS_1'] = df_staff['FULL_PART'].map({1:'Full-Time',2:'Part-Time'})
df_staff['STATUS_2'] = df_staff['Employment  Status']
df_staff['STATUS_3'] = df_staff['Salary/ Wage']
df_staff['Annual Leave  Balance'] = df_staff['HOL_BF_D'] + df_staff['HOL_CY_GR'] + df_staff['HOL_CY_ND'] + df_staff['HOL_CY_D'] - df_staff['HOL_CY_AD']
df_staff['Personal Leave  Balance'] = df_staff['SICK_BAL'] + df_staff['SICK_OUT'] - df_staff['SICK_ADV']

#df_staff['Annual Leave  Group'] = df_staff['HOL_GROUP'].apply(lambda x: 1.175 if x.strip() =="AL" else 1)

# merge three table
df_final = df_staff.merge(df_rate,left_on='CODE_Company',right_on='STAFF_CODE_Company',how='left')
df_final = df_final.merge(df_leave,left_on='CODE_Company',right_on='STAFF_CODE_Company_leave',how='left')

# change the salary
Index_of_salary_rate = df_final.columns.to_list().index('SALARY')
Index_of_Salary = df_final.columns.to_list().index('STATUS_3')
Index_of_hour = df_final.columns.to_list().index('HOUR_RATE1')

for i in range(len(df_final)):
    if df_final.iloc[i,Index_of_Salary] == 'Salary':
        df_final.iloc[i,Index_of_hour:(Index_of_hour+5)] = df_final.iloc[i,Index_of_salary_rate]/76

df_final['Standard Hourly Rate'] = df_final['HOUR_RATE1']
# fill up the 0s
df_list_fillna = df_final[['Code','Standard Hourly Rate']]

df_final[["HOUR_RATE1","HOUR_RATE2","HOUR_RATE3","HOUR_RATE4","HOUR_RATE5"]]=\
    df_final[["HOUR_RATE1","HOUR_RATE2","HOUR_RATE3","HOUR_RATE4","HOUR_RATE5"]].replace(0, np.nan)

df_list_fillna["HOUR_RATE1"] = df_list_fillna['Standard Hourly Rate']
df_list_fillna["HOUR_RATE2"] = df_list_fillna['Standard Hourly Rate']
df_list_fillna["HOUR_RATE3"] = df_list_fillna['Standard Hourly Rate']
df_list_fillna["HOUR_RATE4"] = df_list_fillna['Standard Hourly Rate']
df_list_fillna["HOUR_RATE5"] = df_list_fillna['Standard Hourly Rate']

df_final = df_final.fillna(df_list_fillna)


reorder_column = ['Code','Alpha Code','Name','Start Date','Department','Employment  Status','Salary/ Wage',
                 'Standard Hourly Rate','Birth Date',
                 'HOUR_RATE1','HOUR_RATE2','HOUR_RATE3','HOUR_RATE4','HOUR_RATE5',
                 'CODE','Company','STATUS_1','STATUS_2','STATUS_3',
                 'Annual Leave  Balance','Personal Leave  Balance','Annual Leave  Group','DEFAULT_CC','CODE_Company_DCC']

df_final = df_final[reorder_column]

# combine Essential
dis_rate_df = pd.read_csv(dis_path)
con_rate_df = pd.read_csv(con_path)
tt_rate_df = pd.read_csv(tt_path)
#df_rate_merge['Leave_info'] = ''
df_final_merge = pd.concat([df_final,dis_rate_df,con_rate_df,tt_rate_df])

# change casual AL Loading to 0
df_final_merge['Annual Leave  Group'] = [0 if df_final_merge['STATUS_2'].iloc[i] == 'Casual' else df_final_merge['Annual Leave  Group'].iloc[i] for i in range(len(df_final_merge['STATUS_2']))]

# Change Casual to Wages
df_final_merge['STATUS_3'] = ['Wages' if df_final_merge['STATUS_2'].iloc[i] == 'Casual' else df_final_merge['STATUS_3'].iloc[i] for i in range(len(df_final_merge['STATUS_3']))]

# join payroll tax table
df_state = pd.read_csv(state_path)
df_final_merge = pd.merge(df_final_merge,df_cc,left_on='CODE_Company_DCC',right_on='CODE_Company_CC',how='left')
df_final_merge = pd.merge(df_final_merge,df_state,left_on='CCSTATE',right_on='CODE',how='left')

reorder_column = ['Code','Alpha Code','Name','Start Date','Department','Employment  Status','Salary/ Wage',
                 'Standard Hourly Rate','Birth Date',
                 'HOUR_RATE1','HOUR_RATE2','HOUR_RATE3','HOUR_RATE4','HOUR_RATE5',
                 'CODE','Company','STATUS_1','STATUS_2','STATUS_3',
                 'Annual Leave  Balance','Personal Leave  Balance','Annual Leave  Group','PayrollRate']

df_final_merge = df_final_merge[reorder_column]

# fill payroll rate null as 0
df_final_merge['PayrollRate'] = df_final_merge['PayrollRate'].fillna(0)
# fill the Alpha Code
df_final_merge['Alpha Code'] = df_final_merge['Alpha Code'].fillna(df_final_merge['Name'])

df_final_merge.to_csv(out_path + 'payroll_rate.csv')

# merge deputy
Deputy_path = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Desktop\Payroll Data\Annual Leave\Deputy_Dep.csv"
df_Deputy = pd.read_csv(Deputy_path,index_col=False)[['PayrollId','DisplayName','CompanyName']]
df_HR_Sheet = df_final_merge[['Code','Company','Name','Start Date','STATUS_2']].merge(df_Deputy,left_on='Code',right_on='PayrollId',how='left')
df_HR_Sheet = df_HR_Sheet[['Code','Company','Name','DisplayName','STATUS_2','CompanyName']]
df_HR_Sheet = df_HR_Sheet[df_HR_Sheet['CompanyName'].str.contains("#|Manager|Training",regex=True)]

df_HR_Sheet.to_excel(out_path + 'TeamSheet.xlsx',index=False)
