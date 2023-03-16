import re
import urllib.parse
import requests
import json
import pandas as pd
import numpy as np
import credential

Rate_Table = pd.read_csv('Rate_Table.csv')

MYOB_API_KEY =  credential.MYOB_API_KEY
MYOB_API_SECRET = credential.MYOB_API_SECRET
MYOB_API_REDIRECT_URI = 'http://desktop'

MYOB_TT_API_KEY = credential.MYOB_TT_API_KEY
MYOB_TT_API_SECRET = credential.MYOB_TT_API_SECRET
MYOB_TT_API_REDIRECT_URI = 'http://desktop'

MYOB_DIS = credential.MYOB_DIS
MYOB_TT = credential.MYOB_TT
MYOB_CON = credential.MYOB_CON
# ----- #
#use the printed token_url to get the url_encode, paste down
#need to run two times, One for Annie, One for TT

APIfor = input()
if APIfor == 'AN':
    token_url = f'https://secure.myob.com/oauth2/account/authorize?client_id={MYOB_API_KEY}&redirect_uri={MYOB_API_REDIRECT_URI}&response_type=code&scope=CompanyFile'
elif APIfor == 'TT':
    token_url = f'https://secure.myob.com/oauth2/account/authorize?client_id={MYOB_TT_API_KEY}&redirect_uri={MYOB_TT_API_REDIRECT_URI}&response_type=code&scope=CompanyFile'

print(token_url)

ulr_encode = input()

# ----- #

access_token_url = 'https://secure.myob.com/oauth2/v1/authorize'

def get_index(df,column_name):
    return df.columns.to_list().index(column_name)

def get_employee_json(company_MYOB,headers,company_url):
    request_url = 'Contact/Employee'
    url = f'{company_url}{company_MYOB}/' + request_url
    dis_response = requests.get(url, headers=headers)


def get_employee(company_MYOB, headers,company_url='https://ar2.api.myob.com/accountright/'):
    request_url = 'Contact/Employee'
    url = f'{company_url}{company_MYOB}/' + request_url
    dis_response = requests.get(url, headers=headers)
    print(dis_response.json())
    list_of_employee_contact = []
    for i in dis_response.json()['Items']:
        Last_name = i['LastName']
        FirstName = i['FirstName']
        DisplayID = i['DisplayID']
        IsActive = i['IsActive']
        payroll_url = i['EmployeePayrollDetails']['URI']
        temp_list = [Last_name, FirstName, DisplayID, IsActive, payroll_url]
        list_of_employee_contact.append(temp_list)
    column_need = ['Last_name', 'FirstName', 'DisplayID', 'IsActive', 'payroll_url']
    df_employee = pd.DataFrame(list_of_employee_contact, columns=column_need)
    print(list_of_employee_contact)

    return list_of_employee_contact, df_employee

def get_employee_detail(employee_detail_url, headers):
    payroll_url = employee_detail_url
    response_json = requests.get(payroll_url, headers=headers).json()
    DisplayID = response_json['Employee']['DisplayID']
    DateOfBirth = response_json['DateOfBirth'][:10]
    Gender = response_json['Gender']
    StartDate = response_json['StartDate'][:10]
    EmploymentCategory = response_json['EmploymentCategory']
    EmploymentStatus = response_json['EmploymentStatus']
    try:
        EmploymentClassification = response_json['EmploymentClassification']['Name']
    except:
        EmploymentClassification = 'None'
    Email = response_json['PaySlipEmail']
    # wage
    Wage_type = response_json['Wage']['PayBasis']
    Wage_AnnualSalary = response_json['Wage']['AnnualSalary']
    Wage_HourlyRate = response_json['Wage']['HourlyRate']
    Wage_PayFrequency = response_json['Wage']['PayFrequency']
    Rate1_UID = 'NP'
    Rate2_UID = 'NP'
    Rate3_UID = 'NP'
    Rate4_UID = 'NP'
    Rate5_UID = 'NP'
    Annual_leave_loading = 1
    for i in response_json['Wage']['WageCategories']:
        if len(re.findall('^1\.1',i['Name'])) != 0 :
            Rate1_UID = 'NP'
        elif len(re.findall('^1\.2',i['Name'])) != 0 :
            Rate2_UID = i['UID']
        elif len(re.findall('^1\.3',i['Name'])) != 0 :
            Rate3_UID = i['UID']
        elif len(re.findall('^1\.4',i['Name'])) != 0 :
            Rate4_UID = i['UID']
        elif len(re.findall('^1\.5',i['Name'])) != 0:
            Rate5_UID = i['UID']
        elif len(re.findall('^3\.01',i['Name']))!= 0:
            Annual_leave_loading = 1.175
    # Leaves
    temp_leave_list = []
    for i in response_json['Entitlements']:
        temp_leave_list.append(i['EntitlementCategory']['Name'] + " : " + str(i['Total']))
    Leave_info = " | ".join(temp_leave_list)
#    print(Leave_info)
    # Annual Leave
    Annual_leave = re.findall('Annual Leave Accrual : -?\d+\.\d+',Leave_info)[0]
    Annual_leave = re.findall('-?\d+\.\d+',Annual_leave)[0]
    # Sick Leave
    Sick_Leave = re.findall('Personal Leave Accrual : -?\d+\.\d+',Leave_info)[0]
    Sick_Leave = re.findall('-?\d+\.\d+',Sick_Leave)[0]

    temp_list = [DisplayID, DateOfBirth, Gender, StartDate, EmploymentCategory, EmploymentStatus,
                 EmploymentClassification, Email, Wage_type, Wage_AnnualSalary, Wage_HourlyRate,
                 Wage_PayFrequency, Leave_info,Annual_leave,Sick_Leave,
                 Rate1_UID,Rate2_UID,Rate3_UID,Rate4_UID,Rate5_UID,Annual_leave_loading]
    print(DisplayID, "Done")
    return temp_list

def get_employee_df(company):
    column_need = ['DisplayID', ' DateOfBirth', 'Gender', 'StartDate', 'EmploymentCategory', 'EmploymentStatus',
                   'EmploymentClassification', 'Email', 'Wage_type', 'Wage_AnnualSalary', 'Wage_HourlyRate',
                   'Wage_PayFrequency', 'Leave_info','Annual_leave','Sick_Leave',
                   'Rate1_UID','Rate2_UID','Rate3_UID','Rate4_UID','Rate5_UID','Annual_leave_loading']
    df_payroll_detail = pd.DataFrame(list_of_payroll_detail, columns=column_need)
    df_payroll_detail.to_csv(f'{company}_payroll.csv')

    df_combine = df_employee.merge(df_payroll_detail, on='DisplayID', how='left')
    # drop false
    df_combine.to_csv(f'{company}_combine.csv')
    df_combine_final = df_combine[df_combine['IsActive'] == True]
    # get ready for combine
    df_combine_final['Code'] = df_combine_final['DisplayID']
    df_combine_final['Name'] = df_combine_final['FirstName'] + " " + df_combine_final['Last_name']
    df_combine_final['Start Date'] = df_combine_final['StartDate']
    df_combine_final['Department'] = 'Warehouse'
    df_combine_final['Birth Date'] = df_combine_final[' DateOfBirth']
    df_combine_final['Standard Hourly Rate'] = df_combine_final['Wage_HourlyRate']

    # -- get multiplier
    df_combine_final['Rate1_MUL'] = np.dot(
        df_combine_final['Rate1_UID'].values[:,None] == Rate_Table['rate_UID'].values,
        Rate_Table['rate_multipleer'].values)

    df_combine_final['Rate2_MUL'] = np.dot(
        df_combine_final['Rate2_UID'].values[:, None] == Rate_Table['rate_UID'].values,
        Rate_Table['rate_multipleer'].values)

    df_combine_final['Rate3_MUL'] = np.dot(
        df_combine_final['Rate3_UID'].values[:, None] == Rate_Table['rate_UID'].values,
        Rate_Table['rate_multipleer'].values)

    df_combine_final['Rate4_MUL'] = np.dot(
        df_combine_final['Rate4_UID'].values[:, None] == Rate_Table['rate_UID'].values,
        Rate_Table['rate_multipleer'].values)

    df_combine_final['Rate5_MUL'] = np.dot(
        df_combine_final['Rate5_UID'].values[:, None] == Rate_Table['rate_UID'].values,
        Rate_Table['rate_multipleer'].values)

    # -- #
    df_combine_final["HOUR_RATE1"] = df_combine_final['Standard Hourly Rate'] * df_combine_final['Rate1_MUL']
    df_combine_final["HOUR_RATE2"] = df_combine_final['Standard Hourly Rate'] * df_combine_final['Rate2_MUL']
    df_combine_final["HOUR_RATE3"] = df_combine_final['Standard Hourly Rate'] * df_combine_final['Rate3_MUL']
    df_combine_final["HOUR_RATE4"] = df_combine_final['Standard Hourly Rate'] * df_combine_final['Rate4_MUL']
    df_combine_final["HOUR_RATE5"] = df_combine_final['Standard Hourly Rate'] * df_combine_final['Rate5_MUL']
    df_combine_final["Company"] = company
    df_combine_final["STATUS_1"] = df_combine_final['EmploymentStatus']
    df_combine_final["STATUS_2"] = df_combine_final['EmploymentCategory']
    df_combine_final["STATUS_3"] = df_combine_final['Wage_type']
    df_combine_final["Annual Leave  Balance"] = df_combine_final['Annual_leave']
    df_combine_final["Personal Leave  Balance"] = df_combine_final['Sick_Leave']
    df_combine_final["Annual Leave  Group"] = df_combine_final['Annual_leave_loading']
    # Change Status Mapping FullTime to Full-Time, PartTime to Part-Time, Casual to Casual
    df_combine_final['STATUS_1'] = df_combine_final['STATUS_1'].map(
        {'FullTime': 'Full-Time', 'PartTime': 'Part-Time', 'Casual': 'Part-Time'})

    df_combine_final['STATUS_2'] = df_combine_final['STATUS_2'].map(
        {'Temporary': 'Casual','Permanent':'Permanent'})

    df_combine_final['STATUS_3'] = df_combine_final['HOUR_RATE2'] - df_combine_final['HOUR_RATE1']
    df_combine_final['STATUS_3'] = df_combine_final['STATUS_3'].apply(lambda x: 'Salary' if x==0 else 'Wages')

    # --- #
    Needed_column = ['Code', 'Name', 'Start Date', 'Department', 'Birth Date', 'Standard Hourly Rate', 'HOUR_RATE1',
                     'HOUR_RATE2'
        , 'HOUR_RATE3', 'HOUR_RATE4', 'HOUR_RATE5', 'Company', 'STATUS_1', 'STATUS_2', 'STATUS_3',
                     'Annual Leave  Balance','Personal Leave  Balance','Annual Leave  Group']

    df_combine_final[Needed_column].to_csv(f'{company}_final.csv', index=False)


if APIfor == 'AN':
    decoded = urllib.parse.unquote(ulr_encode[5:])

    data = {
        'client_id': MYOB_API_KEY,
        'client_secret': MYOB_API_SECRET,
        'scope': 'CompanyFile',
        'code': decoded,
        'redirect_uri': MYOB_API_REDIRECT_URI,
        'grant_type': 'authorization_code'}


    response = requests.post(access_token_url, data=data)
    print(response.json())
    assess_token_dict = response.json()

    access_token = assess_token_dict['access_token']
    refresh_token = assess_token_dict['refresh_token']
    print(access_token)

    MYOB_HEADER = {'Authorization': f'Bearer {access_token}',
                  'x-myobapi-key': MYOB_API_KEY,
                  'x-myobapi-version': 'v2'}


    # distribution ----- #



    list_of_employee_contact, df_employee =  get_employee(MYOB_DIS,headers=MYOB_HEADER)
    list_of_payroll_detail = []
    for i in list_of_employee_contact:
        # only get active one
        if i[3] == False:
            continue
        temp_list = get_employee_detail(i[4],headers=MYOB_HEADER)
        list_of_payroll_detail.append(temp_list)
    print("ALL DONE")

    get_employee_df('PD')

    # change casual rate


    # --- connect ---#

    list_of_employee_contact, df_employee =  get_employee(MYOB_CON,headers=MYOB_HEADER)
    list_of_payroll_detail = []
    for i in list_of_employee_contact:
        if i[3] == False:
            continue
        temp_list = get_employee_detail(i[4],headers=MYOB_HEADER)
        list_of_payroll_detail.append(temp_list)
    print("ALL DONE")

    get_employee_df('PC')

# --- TT --- #
if APIfor == 'TT':
    decoded = urllib.parse.unquote(ulr_encode[5:])

    data = {
        'client_id': MYOB_TT_API_KEY,
        'client_secret': MYOB_TT_API_SECRET,
        'scope': 'CompanyFile',
        'code': decoded,
        'redirect_uri': MYOB_TT_API_REDIRECT_URI,
        'grant_type': 'authorization_code'}


    response = requests.post(access_token_url, data=data)
    print(response.json())
    assess_token_dict = response.json()

    access_token = assess_token_dict['access_token']
    refresh_token = assess_token_dict['refresh_token']
    print(access_token)

    MYOB_HEADER = {'Authorization': f'Bearer {access_token}',
                  'x-myobapi-key': MYOB_TT_API_KEY,
                  'x-myobapi-version': 'v2'}


    list_of_employee_contact, df_employee =  get_employee(MYOB_TT,headers=MYOB_HEADER,company_url="https://arl2.api.myob.com/accountright/")
    list_of_payroll_detail = []
    for i in list_of_employee_contact:
        # only get active one
        if i[3] == False:
            continue
        temp_list = get_employee_detail(i[4],headers=MYOB_HEADER)
        list_of_payroll_detail.append(temp_list)
    print("ALL DONE")

    get_employee_df('TT')

