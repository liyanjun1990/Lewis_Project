import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

last_payrun_day = input("Open Payunrun Day: YYYY-MM-DD")
last_payrun_day = datetime.strptime(last_payrun_day,"%Y-%m-%d")

file_path = "payroll_rate.csv"
file_path_check = "RateLevel Table.xlsx"

df = pd.read_csv(file_path,index_col=0,parse_dates=['Birth Date','Start Date'],dayfirst=True)
df_shop = df[df['Company'].isin(['SA','TC','NQ','PPA','IPA','TT'])]
# check wages
df_rate = pd.read_excel(file_path_check,sheet_name='Rate')

def calculate_age(today_date,born_date):
    return today_date.year - born_date.year - ((today_date.month, today_date.day) < (born_date.month, born_date.day))


# check minimun rate
for i in range(len(df_shop)):
    Status = df_shop['STATUS_2'].iloc[i]
    age = calculate_age(last_payrun_day,df_shop['Birth Date'].iloc[i])
#    work_age = math.floor(((last_payrun_day - df_shop['Start Date'].iloc[i]).days / 365)*10)/10
    work_age = df_shop['Start Date'].iloc[i]+ relativedelta(months=6)<= last_payrun_day
    if age >= 21:
        age = 21
    elif age == 20 and work_age == 1:
        age = 21
    elif age < 16:
        age = 'Under'
#    print(df['Code'].iloc[i]," ",age,"",Status)
    RATE = df_rate[(df_rate['STATUS_2'] == Status) & (df_rate['AGE'] == age)]['RATE'].iloc[0]
    Employee_rate = df_shop['HOUR_RATE1'].iloc[i]
    difference_check = (Employee_rate - RATE)
    if difference_check < -0.5:
        print(f"Check minumun rate: {df_shop['Code'].iloc[i]} Start_Day: {df_shop['Start Date'].iloc[i]}, Bithday:{df_shop['Birth Date'].iloc[i]}, turn Age: {age} after: {last_payrun_day} OldRate: {Employee_rate} NewRate: {RATE}_{difference_check}")

# Change leave Group
df_load = pd.read_excel(file_path_check,sheet_name='AL')
for i in range(len(df)):
    Status = df['STATUS_2'].iloc[i]
    # Check Casual
    if Status == "Casual" :
        if df['Annual Leave  Group'].iloc[i] == 0:
#            print(f"Casual {df_shop['Code'].iloc[i]} OK")
            continue
        else:
            print(f"Check Leave Group: Casual {df['Code'].iloc[i]} Not Correct {df['Annual Leave  Group'].iloc[i]}")
            continue
    # Check Permannet part-time
    if df['STATUS_1'].iloc[i] == 'Part-Time' and df['STATUS_2'].iloc[i] == 'Permanent':
        if df['Annual Leave  Group'].iloc[i] == 1.175:
            #            print(f"Casual {df_shop['Code'].iloc[i]} OK")
            continue
        else:
            print(f"Check Leave Group: Part-time {df['Code'].iloc[i]} Not Correct {df['Annual Leave  Group'].iloc[i]}")
            continue

    # Check Permannet full-time
    age = calculate_age(last_payrun_day,df['Birth Date'].iloc[i])
    if age >= 21:
        age = 21
    if age < 16:
        age = 'Under'
#    print(df['Code'].iloc[i]," ",age,"",Status)
    RATE = df_load[(df_load['STATUS_2'] == Status) & (df_load['AGE'] == age)]['RATE'].iloc[0]
    Employee_rate = df['HOUR_RATE1'].iloc[i]
    difference_check = (Employee_rate - RATE)
    if difference_check < 0.1 and df['Annual Leave  Group'].iloc[i] == 1.175:
#        print(f"Permannent {df_shop['Code'].iloc[i]} OK")
        continue
    elif difference_check >= 0.1 and df['Annual Leave  Group'].iloc[i] == 1:
#        print(f"Permannent {df_shop['Code'].iloc[i]} OK")
        continue
    else:
        print(f"Check Leave Group: Permannent {df['Code'].iloc[i]} {age} Not Correct {df['Annual Leave  Group'].iloc[i]} {difference_check}")

# Check wages
df_wage = df[df['STATUS_3']=='Wages']
if df_wage[(df_wage['HOUR_RATE2'] - df_wage['HOUR_RATE1'])==0].empty == False:
    print(df_wage[(df_wage['HOUR_RATE2'] - df_wage['HOUR_RATE1'])==0])
df_PT = df[df['STATUS_1']=='Part-Time']
if df_PT[df_PT['HOUR_RATE3']=='Salary'].empty == False:
    print(df_PT[df_PT['HOUR_RATE3']=='Salary'])
# Check part-time

print("----------------------------------------")

# Check Cost_Center and Super
super_file = r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Documents\GitHub\pythonProject\payroll\super.csv"
df_super = pd.read_csv(super_file,dtype='object')
df_super['PNSTAFF'] = df_super['PNSTAFF'].astype('int64')
df_super_active_only = df.merge(df_super,left_on='Code',right_on='PNSTAFF',how='left')[['Code','PNCOSTCENT']]
df_super_active_only['PNCOSTCENT'] = df_super_active_only['PNCOSTCENT'].fillna('2')
df_super_active_only['last_digit'] = [i[-1] for i in df_super_active_only['PNCOSTCENT']]
df_super_check = df_super_active_only[df_super_active_only['PNCOSTCENT']=='1']




