import re
import urllib.parse
import requests
import json
import pandas as pd
import pyautogui
from datetime import datetime, timedelta
import credential

MYOB_API_KEY = credential.MYOB_API_KEY
MYOB_API_SECRET = credential.MYOB_API_SECRET
MYOB_API_REDIRECT_URI = 'http://desktop'
MYOB_CFTOKEN = credential.MYOB_CFTOKEN


MYOB_TT_API_KEY = credential.MYOB_TT_API_KEY
MYOB_TT_API_SECRET = credential.MYOB_TT_API_SECRET
MYOB_TT_API_REDIRECT_URI = 'http://desktop'

MYOB_DIS = credential.MYOB_DIS
MYOB_TT = credential.MYOB_TT
MYOB_CON = credential.MYOB_CON
MYOB_PP = credential.MYOB_PP
MYOB_WC = credential.MYOB_WC
MYOB_LS = credential.MYOB_LS
MYOB_WA = credential.MYOB_WA

# ----- #
# use the printed token_url to get the url_encode, paste down
# need to run two times, One for Annie, One for TT

APIfor = input()
if APIfor == 'AN':
    token_url = f'https://secure.myob.com/oauth2/account/authorize?client_id={MYOB_API_KEY}&redirect_uri={MYOB_API_REDIRECT_URI}&response_type=code&scope=CompanyFile'
elif APIfor == 'TT':
    token_url = f'https://secure.myob.com/oauth2/account/authorize?client_id={MYOB_TT_API_KEY}&redirect_uri={MYOB_TT_API_REDIRECT_URI}&response_type=code&scope=CompanyFile'

print(token_url)

ulr_encode = input()

# ----- #

access_token_url = 'https://secure.myob.com/oauth2/v1/authorize'

decoded = urllib.parse.unquote(ulr_encode[5:])

def get_report_period(start_date_string):

    start_date = datetime.strptime(start_date_string,"%Y-%m-%d")
    end_of_month = start_date + timedelta(days=32)
    end_of_month = end_of_month.replace(day=1) - timedelta(days=1)
    end_date_string = end_of_month.strftime("%Y-%m-%d")
    if start_date.month >=7:
        start_date_YR = datetime(start_date.year,7,1)
    else:
        start_date_YR = datetime(start_date.year-1, 7, 1)

    start_date_YR_String = start_date_YR.strftime("%Y-%m-%d")

    return end_date_string,start_date_YR_String

class MYOB_API:
    def __init__(self, api_data,company_url,company_file_url, access_token='', refresh_token='', MYOB_HEADER={}):
        self.api_data = api_data
        self.company_url = company_url
        self.company_file_url = company_file_url

    def request_token(self):
        response = requests.post(access_token_url, data=self.api_data)
        print(response.json())
        assess_token_dict = response.json()

        self.access_token = assess_token_dict['access_token']
        self.refresh_token = assess_token_dict['refresh_token']
        print(self.access_token)

        self.MYOB_HEADER = {'Authorization': f'Bearer {self.access_token}',
                       'x-myobapi-key': self.api_data['client_id'],
                       'x-myobapi-version': 'v2'}

    def request_info(self,allurl=False,output_Json=False,request_url=""):
        if request_url == "":
            request_url = input('request_url')
        if allurl==False:
            url = f'{self.company_url}{self.company_file_url}/' + request_url
        else:
            url = request_url
        info_response = requests.get(url, headers=self.MYOB_HEADER)
        res_json = json.loads(info_response.text)
        print(res_json)
        if output_Json != False:
            with open(f'{output_Json}.json', 'w', encoding='utf-8') as f:
                json.dump(res_json, f, ensure_ascii=False,indent=4)
        return res_json

if APIfor=="TT":
    TT_Request = MYOB_API(api_data={
            'client_id': MYOB_TT_API_KEY,
            'client_secret': MYOB_TT_API_SECRET,
            'scope': 'CompanyFile',
            'code': decoded,
            'redirect_uri': MYOB_TT_API_REDIRECT_URI,
            'grant_type': 'authorization_code'
    },company_url="https://arl2.api.myob.com/accountright/",company_file_url=MYOB_TT)

    TT_Request.request_token()

#    start_date_string = "2022-12-01"
    start_date_string = input("YYYY-MM-01")
    end_date_string,start_date_YR_String = get_report_period(start_date_string)

    reporting_basis = "Accrual"
    year_end_adjust = True
    requestPandLM = f'Report/ProfitAndLossSummary/?StartDate={start_date_string}&EndDate={end_date_string}&ReportingBasis={reporting_basis}&YearEndAdjust={year_end_adjust}'
    requestPandLY = f'Report/ProfitAndLossSummary/?StartDate={start_date_YR_String}&EndDate={end_date_string}&ReportingBasis={reporting_basis}&YearEndAdjust={year_end_adjust}'
    requestBS = f'Report/BalanceSheetSummary/?AsOfDate={end_date_string}&YearEndAdjust={year_end_adjust}&ReportingBasis={reporting_basis}'


    TT_Request.request_info(request_url=requestPandLM,output_Json='./PLBS/TT_Detail_Month')
    TT_Request.request_info(request_url=requestPandLY,output_Json='./PLBS/TT_Detail_Yearly')
    TT_Request.request_info(request_url=requestBS,output_Json='./PLBS/TT_Detail_BS')
    TT_Request.request_info(request_url='/GeneralLedger/Account',output_Json='./PLBS/TT_Account')

elif APIfor=="AN":

    AN_Request = MYOB_API(api_data={
        'client_id': MYOB_TT_API_KEY,
        'client_secret': MYOB_TT_API_SECRET,
        'scope': 'CompanyFile',
        'code': decoded,
        'redirect_uri': MYOB_TT_API_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }, company_url="https://ar2.api.myob.com/accountright/", company_file_url=MYOB_CON)

    AN_Request.request_token()

    #    start_date_string = "2022-12-01"
    start_date_string = input("YYYY-MM-01")

    list_of_file = [
        {'Company':'CON','url':MYOB_CON},
        {'Company': 'DIS', 'url': MYOB_DIS},
        {'Company': 'PP', 'url': MYOB_PP},
        {'Company': 'WC', 'url': MYOB_WC},
        {'Company': 'LS', 'url': MYOB_LS},
        {'Company': 'WA', 'url': MYOB_WA}
    ]

    for i in list_of_file:
        company_name = i['Company']
        MYOB_URL = i['url']
        AN_Request.company_file_url = MYOB_URL

        end_date_string, start_date_YR_String = get_report_period(start_date_string)

        reporting_basis = "Accrual"
        year_end_adjust = True
        requestPandLM = f'Report/ProfitAndLossSummary/?StartDate={start_date_string}&EndDate={end_date_string}&ReportingBasis={reporting_basis}&YearEndAdjust={year_end_adjust}'
        requestPandLY = f'Report/ProfitAndLossSummary/?StartDate={start_date_YR_String}&EndDate={end_date_string}&ReportingBasis={reporting_basis}&YearEndAdjust={year_end_adjust}'
        requestBS = f'Report/BalanceSheetSummary/?AsOfDate={end_date_string}&YearEndAdjust={year_end_adjust}&ReportingBasis={reporting_basis}'

        AN_Request.request_info(request_url=requestPandLM, output_Json=rf'./PLBS/{company_name}_Detail_Month')
        AN_Request.request_info(request_url=requestPandLY, output_Json=rf'./PLBS/{company_name}_Detail_Yearly')
        AN_Request.request_info(request_url=requestBS, output_Json=rf'./PLBS/{company_name}_Detail_BS')
        AN_Request.request_info(request_url='/GeneralLedger/Account', output_Json=rf'./PLBS/{company_name}_Account')
