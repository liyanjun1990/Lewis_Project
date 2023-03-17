import Deputy_Lib
import pandas as pd
import json
from datetime import datetime, timedelta
import Cred

Deputy_Request  = Deputy_Lib.Deputy_API(
    api_data = {
        "client_id": Cred.Client_Id,
        "client_secret": Cred.Client_Secret,
        "redirect_uri" : Cred.Re_uri,
        "grant_type" : "authorization_code",
        "code" : '',
        "scope" : "longlife_refresh_token"
    }
)

Deputy_Request.get_temp_code()
Deputy_Request.request_token()

# get employee
request_what = input("Request what? 1.Deputy_Staff 2.Timesheet Mod  3.Timesheet Range")

if request_what == '1':
    print('Deputy_Staff Exporting')
    json_respond = Deputy_Request.get_employees_by_start_id(1)
    employee_list_length= len(json_respond)

    while employee_list_length == 500:
        json_temp = Deputy_Request.get_employees_by_start_id(json_respond[-1]['Id']+1)
        json_respond = json_respond + json_temp
        employee_list_length = len(json_temp)

    df = pd.json_normalize(json_respond,max_level=0)
    df.to_csv('staff.csv')

    df_result = df[['Id','DisplayName','PayrollId','Active','Company','Created','TerminationDate']]

    # get location
    json_respond = Deputy_Request.get_location_list()
    df = pd.json_normalize(json_respond,max_level=0)
    df.to_csv('locations.csv',index=False)
    df_company = df[['Id','CompanyName']]

    df_merge = df_result.merge(df_company,left_on='Company',right_on='Id',how='left')

    #df_merge.to_csv(r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Desktop\Payroll Data\Annual Leave\Deputy_Dep.csv")
    df_merge.to_csv(r"Deputy_Dep.csv")
    print('Exported')

elif request_what == '2':
    print('Timesheet Mod Exporting')

    json_respond = Deputy_Request.get_timesheet_range_modified("2023-02-14")
    # give alert if 500 more
    if len(json_respond)>=500:
        print("More than 500")
    df = pd.json_normalize(json_respond, max_level=0)
    needed_column = ['Id', 'Employee', 'TotalTime', 'EmployeeComment', 'Modified', 'StartTimeLocalized',
                     'EndTimeLocalized']
    df_short = df[needed_column]
    df_short['Modified'] = [i[:19] for i in df_short['Modified']]
    df_short['Modified'] = pd.to_datetime(df_short['Modified'])
    df_short['StartTimeLocalized'] = [i[:19] for i in df_short['StartTimeLocalized']]
    df_short['StartTimeLocalized'] = pd.to_datetime(df_short['StartTimeLocalized'])
    df_short['EndTimeLocalized'] = [i[:19] for i in df_short['EndTimeLocalized']]
    df_short['EndTimeLocalized'] = pd.to_datetime(df_short['EndTimeLocalized'])

    df_modified = df_short[(df_short['Modified'] >= datetime(2023, 2, 14, 13, 0, 0)) & (
                df_short['EndTimeLocalized'] < datetime(2023, 2, 13, 0, 0, 0))]
    df_modified.to_csv('modified.csv')

elif request_what == '3':
    print('Timesheet Exporting')
    start_date = input("Start Date as YYYY-MM-DD, default 14 days")
    date_int = int(input("default 14 days"))
    start_date_unix = datetime.timestamp(datetime.strptime(start_date,"%Y-%m-%d"))
    end_date_unix = datetime.timestamp(datetime.strptime(start_date,"%Y-%m-%d") + timedelta(days=date_int))
    json_respond = Deputy_Request.get_timesheet_by_unix(start_date_unix,end_date_unix)
    employee_list_length = len(json_respond)
    while employee_list_length == 500:
        json_temp = Deputy_Request.get_timesheet_by_unix(json_respond[-1]['StartTime'],end_date_unix)
        json_respond = json_respond + json_temp
        employee_list_length = len(json_temp)
        print("In Process ", json_respond[-1]['StartTime'])

    df = pd.json_normalize(json_respond, max_level=1)
    df = df.drop_duplicates(subset=['Id'])
    df.to_csv('Timesheet_ori_2.csv')
    # get payroll_id

    needed_column = ['Id','Employee', 'EmployeeAgreementObject.PayrollId','StartTimeLocalized','EndTimeLocalized','TotalTime',
                     'TimeApproved', 'OperationalUnitObject.OperationalUnitName',
                     'LeaveRuleObject.Name','Leave.Comment','Leave.TotalHours','Modified']

    df_short = df[needed_column]
    df_short['Modified'] = [i[:19] for i in df_short['Modified']]
    df_short['Modified'] = pd.to_datetime(df_short['Modified'])
    df_short['StartTimeLocalized'] = [i[:19] for i in df_short['StartTimeLocalized']]
    df_short['StartTimeLocalized'] = pd.to_datetime(df_short['StartTimeLocalized'])
    df_short['EndTimeLocalized'] = [i[:19] for i in df_short['EndTimeLocalized']]
    df_short['EndTimeLocalized'] = pd.to_datetime(df_short['EndTimeLocalized'])
    df_short.to_csv("Timesheet.csv")