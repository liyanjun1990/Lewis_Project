import pandas as pd
from datetime import datetime

update_database = input("1.Detail and Rate\n2.Balance Report")

pay_detail_path = r"\\192.168.1.223\Payroll\Payroll\Payrun DataBase\Payment Date\Pay Detail.csv"
balance_path = r"\\192.168.1.223\Payroll\Payroll\Payrun DataBase\Payment Date\Balance Report.csv"
payrate_path = r"\\192.168.1.223\Payroll\Payroll\Payrun DataBase\Payment Date\Payrate.csv"

if update_database == "1":
    file_path = input("file_path_payrun")
    period = input("last day of period")
    # update pr
    df_pr = pd.read_csv(payrate_path)
    df_pr = df_pr.dropna(how='all')
    df_temp_pr = pd.read_excel(file_path,sheet_name="Rate",usecols="B:T,X")
    df_temp_pr = df_temp_pr.dropna(how='all')
    df_temp_pr['Start Date'] = df_temp_pr['Start Date'].apply(lambda x:x.strftime("%d/%m/%Y"))
    df_temp_pr['Birth Date'] = df_temp_pr['Birth Date'].apply(lambda x:x.strftime("%d/%m/%Y"))
    # check if column is right
    if df_temp_pr.columns[-2] != "STATUS_3":
        print("Pay Rate  Recheck Columns")
        exit()
    # check if period duplicated or not
    if sum(df_pr['Period'].isin([period])) != 0:
        print("Pay Rate Period Duplicated")
        exit()
    df_temp_pr['Period'] = period
    df_pr = pd.concat([df_pr,df_temp_pr])

    # update pd
    df_pd = pd.read_csv(pay_detail_path)
    df_pd = df_pd.dropna(how='all')
    df_temp_pd = pd.read_excel(file_path,sheet_name="Cut_off_Deputy",usecols="A:AA",skiprows=1)
    df_temp_pd = df_temp_pd.dropna(how='all')
    df_temp_pd['Timesheet Date'] = df_temp_pd['Timesheet Date'].apply(lambda x: x.strftime("%d/%m/%Y"))
    # check if column is right
    if df_temp_pd.columns[-1] != "AL Accrue($)":
        print("Pay Detail Recheck Columns")
        exit()
    # check if period duplicated or not
    if sum(df_pd['Period'].isin([period])) != 0:
        print("Pay Detail Period Duplicated")
        exit()
    df_temp_pd['Period'] = period

    df_pd = pd.concat([df_pd,df_temp_pd])

    df_pr.to_csv(payrate_path, index=False,date_format="%Y/%d/%m")
    df_pd.to_csv(pay_detail_path,index=False,date_format="%Y/%d/%m")
    print('updated')

if update_database == "2":
    file_path = input("file_path_balance")
    period = input("last day of period")
    # update pr
    df_br = pd.read_csv(balance_path)
    df_br = df_br.dropna(how='all')
    df_temp_br = pd.read_csv(file_path)
    df_temp_br = df_temp_br.dropna(how='all')
    # check if column is right
    if df_temp_br.columns[-1] != "TIL_End_After":
        print("Balance  Recheck Columns")
        exit()
    # check if period duplicated or not
    if sum(df_br['Period'].isin([period])) != 0:
        print("Balance Period Duplicated")
        exit()
    df_temp_br['Period'] = period
    df_br = pd.concat([df_br,df_temp_br])

    df_br.to_csv(balance_path,index=False)
    print('Balance Updated')

#if update_database == "4":

