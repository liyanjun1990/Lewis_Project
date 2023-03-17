import pandas as pd
from datetime import datetime

today = datetime.today()
today_str = datetime.strftime(today,'%Y-%m-%d')

file_path = input('file_full_path, payrun')
output_path = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Desktop\Payroll Data\Annual Leave\\"

file_path_dep = input('file_full_path, KPI Report')

df = pd.read_excel(file_path,sheet_name='Check_List_New')

Deputy_path = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Desktop\Payroll Data\Annual Leave\Deputy_Dep.csv"
AL_path = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Desktop\Payroll Data\Result\payroll_rate.csv"

df_Deputy = pd.read_csv(Deputy_path,index_col=False)[['PayrollId','DisplayName','CompanyName']]
df_AL = pd.read_csv(AL_path,index_col=False)[['Code','Annual Leave  Balance','Personal Leave  Balance']]

# take store only
#start_index = df['Code'].to_list().index('WFT')
#df = df.iloc[:start_index,:]
df = df.dropna(subset='Code')
df = df[['Code','Type','TIL_OT_After','TIL-PE_After']]
df['TIL_End_After'] = df['TIL_OT_After'] + df['TIL-PE_After']
df = df[['Code','Type','TIL_End_After']]

df_final = df.merge(df_Deputy,left_on='Code',right_on='PayrollId',how='left')
df_final = df_final.merge(df_AL,left_on='Code',right_on='Code',how='left')
df_final = df_final.dropna(subset='Annual Leave  Balance')
# reorder columns
order_columns = ['Code','Type','DisplayName','CompanyName','Annual Leave  Balance','Personal Leave  Balance','TIL_End_After']
df_final = df_final[order_columns]
df_final = df_final.drop_duplicates(subset=['Code'])
# all
df_final.to_csv(output_path + f'Balance_Report_{today_str}.csv',index=False)

# take out Sick Leave
order_columns = ['Code','Type','DisplayName','CompanyName','Annual Leave  Balance','TIL_End_After']
df_final = df_final[order_columns]
# RT
df_final_RT = df_final[df_final['CompanyName'].str.contains("#|Manager|Training",regex=True)]

# put AM in
df_report_line = pd.read_excel(file_path,sheet_name='ReportLine')[['Store Name','Area Manager']]
df_final_RT = df_final_RT.merge(df_report_line,left_on='CompanyName',right_on='Store Name')
df_final_RT = df_final_RT[['Code','Type','DisplayName','CompanyName','Area Manager','Annual Leave  Balance','TIL_End_After']]
df_final_RT.to_csv(output_path + f'Balance_Report_RT_{today_str}.csv',index=False)

# department only
df_dep = pd.read_excel(file_path_dep,sheet_name='Department')
df_dep = df_dep[['Code','Department']]
df_HOD = pd.read_excel(file_path_dep,sheet_name='Head of Director')

df_final_dep = df_final[~df_final['CompanyName'].str.contains("#|Manager|Training",regex=True)]
df_final_dep = pd.merge(df_final_dep,df_dep,left_on='Code',right_on='Code',how='left')
df_final_dep = pd.merge(df_final_dep,df_HOD,left_on='Department',right_on='Department',how='left')
# Check AM
if df_final_dep['Department'].isna().sum() !=0:
    print("Department not complete")
    print(df_final_dep[df_final_dep['Department'].isna()])

Head_list = df_final_dep['Head'].drop_duplicates().to_list()

df_final_dep = df_final_dep[['Code','Type','DisplayName','Department','Annual Leave  Balance','TIL_End_After','Head']]

for i in Head_list:
    df_temp = df_final_dep[df_final_dep['Head']==i]
    df_temp.to_csv(output_path + f'Dep\Balance_Report_{i}_{today_str}.csv',index=False)
