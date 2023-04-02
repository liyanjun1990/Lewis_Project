import requests
import json
from datetime import datetime
from datetime import timezone
from dateutil import parser
import pandas as pd
import Cred

class Deputy_API:
    def __init__(self,api_data,access_token='',refresh_token='',API_header={}):
        self.api_data = api_data

    def get_temp_code(self):
        Client_Id = self.api_data['client_id']
        print(f'https://once.deputy.com/my/oauth/login?client_id={Client_Id}&redirect_uri=http://localhost&response_type=code&scope=longlife_refresh_token')
        temp_code = input('please provide temp_code')
        self.api_data['code'] = temp_code

    def request_token(self):
        access_token_url = f'https://once.deputy.com/my/oauth/access_token'
        response = requests.post(access_token_url, data=self.api_data)
        print(response.json())
        assess_token_dict = response.json()
        try:
            self.access_token = assess_token_dict['access_token']
            self.refresh_token = assess_token_dict['refresh_token']
            print(self.access_token)
        except:
            self.access_token= input('input_access_token')
        self.API_header = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f"OAuth {self.access_token}"
        }

    def get_employees_by_start_id(self,start_id):
        employee_url = f'https://demo.com/api/v1/supervise/employee/QUERY'

        headers = self.API_header

        js = {
             "search":{"s1":{"field":'Id',"data":start_id,"type":"ge"}},
              "max":500}

        response = requests.post(employee_url, headers=self.API_header,json=js)
    #    print(response)
        return json.loads(response.text)

    def get_location_list(self):

        location_url = f'https://demo.com/api/v1/resource/Company'

        response = requests.get(location_url,headers=self.API_header)
        return json.loads(response.text)

    def get_timesheet_range_modified(self,date):
        timesheet_url = f'https://demo.com/api/v1/resource/Timesheet/QUERY'

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f"OAuth {self.access_token}"
        }

        js = {
            "search": {"s1": {"field": 'Modified', "data": f"%{date}%", "type": "lk"},
                       "s2": {"field": 'TimeApproved', "data": True, "type": "eq"}
                       },
            "join": ["EmployeeAgreementObject", "LeaveRuleObject", "OperationalUnitObject", "Leave"],
            "max": 500}

        response = requests.post(timesheet_url, headers=self.API_header, json=js)
        #print(json.loads(response.text))
        return json.loads(response.text)

    def get_timesheet_by_date(self,date):
        timesheet_url = f'https://demo.deputy.com/api/v1/resource/Timesheet/QUERY'

        js = {
            "search": {"s1": {"field": 'Date', "data": f"%{date}%", "type": "lk"},
                       "s2": {"field": 'TimeApproved', "data": True, "type": "eq"}
                       },
            "join": ["EmployeeAgreementObject", "LeaveRuleObject", "OperationalUnitObject", "Leave"],
            "max": 500}

        response = requests.post(timesheet_url, headers=self.API_header, json=js)
        #print(json.loads(response.text))
        return json.loads(response.text)

    def get_timesheet_by_unix(self,start,end,approve=True):
        timesheet_url = f'https://demo.com/api/v1/resource/Timesheet/QUERY'
        if approve == True:
            js = {
                "search": {"s1": {"field": 'StartTime', "data": f"{start}", "type": "ge"},
                           "s2": {"field": 'StartTime', "data": f"{end}", "type": "le"},
                           "s3": {"field": 'TimeApproved', "data": True, "type": "eq"}
                           },
                "join": ["EmployeeAgreementObject", "LeaveRuleObject", "OperationalUnitObject", "Leave"],
                "max": 500}
        elif approve== 'both':
            js = {
                "search": {"s1": {"field": 'StartTime', "data": f"{start}", "type": "ge"},
                           "s2": {"field": 'StartTime', "data": f"{end}", "type": "le"},
                           },
                "join": ["EmployeeAgreementObject", "LeaveRuleObject", "OperationalUnitObject", "Leave"],
                "max": 500}

        response = requests.post(timesheet_url, headers=self.API_header, json=js)
        #print(json.loads(response.text))
        return json.loads(response.text)
