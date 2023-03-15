import pandas as pd
from datetime import datetime
import numpy as np

master_path = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Documents\GitHub\pythonProject\payroll\\"
current_file = master_path + r"crun.csv"
#previous_file = master_path + r"prun.csv"
employee_file = master_path + r"employee_tem.xlsx"
PH_file = master_path + r"PH.csv"
summary_file = master_path + r'summary.csv'

c_df = pd.read_csv(current_file)
#Drop leaves
c_df = c_df.dropna(subset=['Area Name'])
#drop FALSE
c_df = c_df[(c_df['Pay Approve'] == True)]
# change to datetime
c_df['Timesheet Date'] = [datetime.strptime(i,"%d/%m/%Y") for i in c_df['Timesheet Date']]
c_df_sum = c_df[['Employee Export Code','Timesheet Date','Timesheet Total Time']].groupby(['Employee Export Code','Timesheet Date']).sum()
c_df_sum = c_df_sum.reset_index()

# ---------- # will be provided by AM

final = pd.read_csv(summary_file)

# ---------- #
# calculate penalty
employee_df = pd.read_excel(employee_file)[['Employee_ID','Type','State']]
employee_list = employee_df['Employee_ID'].to_list()
employee_list = [x for x in employee_list if np.isnan(x) == False]

# list of public holiday
ph_df = pd.read_csv(PH_file)
ph_df['PH'] = [datetime.strptime(i,"%d/%m/%Y") for i in ph_df['PH']]
ph_df_merge = employee_df.merge(ph_df,left_on='State',right_on='State',how='left')


def calculate(type,r_hour,w_hour):
    if type == 'NP':
        return ('NP',w_hour * 1.25, max(r_hour - w_hour,0), "worked hour:" + str(w_hour)+" * 1.25 + " + " off hour: " + str(max(r_hour - w_hour,0)))
    elif type == 'P':
        return ('P',0,max(r_hour - w_hour, 0), "worked hour:" + str(w_hour)  +" off hour: " + str(max(r_hour - w_hour, 0)))

def get_work_hour(df,id,day):
    if df[(df['Employee Export Code'] == id) & (df['Timesheet Date'] == day)].empty == True:
        return (0,"")
    else:
        worked_hour = df[(df['Employee Export Code'] == id) & (df['Timesheet Date'] == day)][
        'Timesheet Total Time'].values[0]
        worked_place = c_df[(c_df['Employee Export Code'] == id) & (c_df['Timesheet Date'] == day)]['Area Name'].values[0]
        return (worked_hour,worked_place)

def get_regular_hour(df,id,day):
    if df[(df['Employee Export Code'] == id)][day].empty == True:
        return 0
    else:
        return df[(df['Employee Export Code'] == id)][day].values[0]

master_list = []
for i_ids in employee_list:
    employee_type = employee_df[employee_df['Employee_ID']==i_ids]['Type'].values[0]
    print(employee_type)
    for j_days in ph_df_merge[ph_df_merge['Employee_ID']==i_ids]['PH'].to_list():
        work_hours,work_place = get_work_hour(c_df_sum,i_ids,j_days)
        print(work_hours)
        regular_hours = get_regular_hour(final,i_ids,j_days.strftime("%a"))
        print(regular_hours)

        E_type,p_add,nw_add,reason = calculate(employee_type,regular_hours,work_hours)
        if E_type == "NP":
            temp_list = [i_ids,j_days,p_add,reason,work_place,"P"]
            master_list.append(temp_list)
            temp_list = [i_ids,j_days,nw_add,reason,"","NW"]
            master_list.append(temp_list)
        elif E_type == "P":
            temp_list = [i_ids,j_days,nw_add,reason,"","NW"]
            master_list.append(temp_list)
        print(i_ids," Good")

df_result = pd.DataFrame(master_list,columns=['Code','Date','Add Hours','Reason','Worked Location','Type'])
df_result = df_result.drop_duplicates()
df_result = df_result[df_result['Add Hours']!=0]
df_result.to_csv('Public_Holiday_Result.csv')






