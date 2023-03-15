import pandas as pd

#file_path = r"\\192.168.1.223\Payroll\Payroll\20220718-20220731\2022.07.31Lewis.xlsm"
#outpath = r"\\192.168.1.223\Payroll\Payroll\20220718-20220731\\"

file_path = input('file_path')
outpath = input('outpath')
payrunendday = input('pay run end day DD/MM/YYYY')


df_check_list = pd.read_excel(file_path,sheet_name='Check_List_New',engine='openpyxl')

# UPTO PC
df_check_list = df_check_list.dropna(subset=['Code'])
end_row = df_check_list['Code'].to_list().index('PC')
df_check_list = df_check_list.iloc[0:end_row,:]

#partition

company = set(df_check_list['Company'].tolist())

options = input("ALL\n2.Company_Code, SA,IPA,PPA,TT,TC,NQ")
options = options.split(",")

if options[0] == "ALL":
    pass
elif options[0] !="ALL" and options[0] in company:
    df_check_list = df_check_list[df_check_list['Company'].isin(options)]
else:
    print('No This Company')
    exit()

type_column = df_check_list.columns.to_list().index('Type')

TOIL_AL = df_check_list.columns.to_list().index('Annual Leave')
TOIL_SL = df_check_list.columns.to_list().index('Sick Leave')
TOIL_UP = df_check_list.columns.to_list().index('Unpaid Leave')

TOIL_RAAL = df_check_list.columns.to_list().index('TIL-OT rather than AL')
TOIL_PE_RAAL = df_check_list.columns.to_list().index('TIL-PE rather than AL')

SW_AL = df_check_list.columns.to_list().index('Use AL instead')
SW_SL = df_check_list.columns.to_list().index('Use Sick instead')
TOIL_PO = df_check_list.columns.to_list().index('TIL-OT payout')
TOIL_PO_OT = df_check_list.columns.to_list().index('TIL-OT 1.5 Payout')
TOIL_PE_PO = df_check_list.columns.to_list().index('TIL-PE payout')
# inter change
TOIL_OT_IT = df_check_list.columns.to_list().index('TIL-OT-IT')
TIL_PE_IT = df_check_list.columns.to_list().index('TIL-PE-IT')

TIL_OT_BE = df_check_list.columns.to_list().index('TIL-OT Beg')
TIL_OT_EB = df_check_list.columns.to_list().index('TOIL-OT End')

TIL_PE_BE = df_check_list.columns.to_list().index('TIL-PE Beg')
TIL_PE_EB = df_check_list.columns.to_list().index('TIL-PE End')

Deputy_AL = df_check_list.columns.to_list().index('Deputy Annual Leave')
AL_USE = df_check_list.columns.to_list().index('AL-USE')
Deputy_SL = df_check_list.columns.to_list().index('Deputy Sick leave')
SL_USE = df_check_list.columns.to_list().index('SL-USE')

df_check_list.iloc[:,[TOIL_AL,TOIL_SL,TOIL_UP,TOIL_RAAL,SW_AL,SW_SL,TOIL_PO,TOIL_PE_PO,TOIL_PO_OT,TOIL_PE_RAAL,TOIL_OT_IT,TIL_PE_IT]] = \
    df_check_list.iloc[:,[TOIL_AL,TOIL_SL,TOIL_UP,TOIL_RAAL,SW_AL,SW_SL,TOIL_PO,TOIL_PE_PO,TOIL_PO_OT,TOIL_PE_RAAL,TOIL_OT_IT,TIL_PE_IT]].fillna(0)

Employee_Export_Code = []

Weekday = []

Hours = []

Leave_Type_Name = []





for i in range(len(df_check_list)):
    # TOIL accumulated or used
    if df_check_list.iloc[i,TIL_OT_BE] - df_check_list.iloc[i,TIL_OT_EB] != 0:
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(df_check_list.iloc[i,TIL_OT_BE] - df_check_list.iloc[i,TIL_OT_EB])
        Leave_Type_Name.append('TOIL-OT')
    # mark down AL
    if df_check_list.iloc[i,Deputy_AL] + df_check_list.iloc[i,AL_USE] !=0:
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(-df_check_list.iloc[i,Deputy_AL] - df_check_list.iloc[i,AL_USE])
        Leave_Type_Name.append('Annual Leave')
    # mark down SL
    if df_check_list.iloc[i,Deputy_SL] + df_check_list.iloc[i,SL_USE] !=0:
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(-df_check_list.iloc[i,Deputy_SL] - df_check_list.iloc[i,SL_USE])
        Leave_Type_Name.append('Sick Leave')
    # adjust TOIL-OT
    if df_check_list.iloc[i, TOIL_AL] !=0:
        # change btween AL and TOIL
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, TOIL_AL])
        Leave_Type_Name.append('Annual Leave')

        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_AL])
        Leave_Type_Name.append('TOIL-OT')

    if df_check_list.iloc[i, TOIL_SL] != 0:
        # change btween SL and TOIL
        Employee_Export_Code.append(df_check_list.iloc[i, 0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, TOIL_SL])
        Leave_Type_Name.append('Sick Leave')

        Employee_Export_Code.append(df_check_list.iloc[i, 0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_SL])
        Leave_Type_Name.append('TOIL-OT')
    if df_check_list.iloc[i, TOIL_UP] != 0:
        # Unpaid
        Employee_Export_Code.append(df_check_list.iloc[i, 0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_UP])
        Leave_Type_Name.append('TOIL-OT Unpaid')
    if df_check_list.iloc[i, TOIL_RAAL] != 0:
        # switch between AL and TOIL
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, TOIL_RAAL])
        Leave_Type_Name.append('Annual Leave')

        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_RAAL])
        Leave_Type_Name.append('TOIL-OT')
    if df_check_list.iloc[i, TOIL_PO] != 0:
        # payout TOIL
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_PO])
        Leave_Type_Name.append('TOIL-OT Payout')
    if df_check_list.iloc[i, TOIL_PO_OT] != 0:
        # payout TOIL 1.5 OT
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(-df_check_list.iloc[i, TOIL_PO_OT])
        Leave_Type_Name.append('TOIL-OT 1.5 Payout')

    # adjust TOIL-PE
    if df_check_list.iloc[i,TIL_PE_BE] - df_check_list.iloc[i,TIL_PE_EB] != 0:
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(df_check_list.iloc[i,TIL_PE_BE] - df_check_list.iloc[i,TIL_PE_EB])
        Leave_Type_Name.append('TOIL-PE')


    if df_check_list.iloc[i, TOIL_PE_RAAL] != 0:
        # switch between AL and TOIL
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, TOIL_PE_RAAL])
        Leave_Type_Name.append('Annual Leave')

        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_PE_RAAL])
        Leave_Type_Name.append('TOIL-PE')

    if df_check_list.iloc[i, TOIL_PE_PO] != 0:
        # payout TOIL
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_PE_PO])
        Leave_Type_Name.append('TOIL-PE Payout')

    # switch between PT and PE
    if df_check_list.iloc[i, TOIL_OT_IT] != 0:
        # switch OT
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TOIL_OT_IT])
        Leave_Type_Name.append('TOIL-OT Inter Change')

    if df_check_list.iloc[i, TIL_PE_IT] != 0:
        # switch PE
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append('Ord')
        Hours.append(-df_check_list.iloc[i, TIL_PE_IT])
        Leave_Type_Name.append('TOIL-PE Inter Change')

    # switch AL SL and Unpaid
    if df_check_list.iloc[i, SW_AL] != 0:
        # switch AL SL and Unpaid
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, SW_AL])
        Leave_Type_Name.append('Annual Leave')
    if df_check_list.iloc[i, SW_SL] != 0:
        # switch AL SL and Unpaid
        Employee_Export_Code.append(df_check_list.iloc[i,0])
        Weekday.append(' ')
        Hours.append(df_check_list.iloc[i, SW_SL])
        Leave_Type_Name.append('Sick Leave')



# create df
df_final = pd.DataFrame({'Employee Export Code':Employee_Export_Code,
              'Weekday':Weekday,
              'Hours':Hours,
              'Leave Type Name':Leave_Type_Name
              })

df_final['Timesheet Date'] = payrunendday
df_final['Day'] = ''
df_final['Timesheet Start Time'] = ''
df_final['Timesheet End Time'] = ''
df_final['Night Hours'] = ''
df_final['Timesheet Total Time'] = df_final['Hours']
df_final['Area Name'] = ''
reorder = ['Timesheet Date','Day','Employee Export Code','Timesheet Start Time','Timesheet End Time','Weekday',
           'Hours','Night Hours','Timesheet Total Time','Area Name','Leave Type Name']

df_final = df_final[reorder]
df_final.to_csv(outpath + r'\\Entry_Check_List_' + ",".join(options)  + '.csv')
