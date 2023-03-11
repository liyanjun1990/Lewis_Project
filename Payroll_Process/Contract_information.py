from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd

import pyperclip


#browser = webdriver.Chrome(r"C:\Users\admin\Desktop\AUTO\chromedriver.exe")
browser = webdriver.Chrome(r"C:\Users\Accounting - 10102\Desktop\AUTO\chromedriver.exe")

url = 'https://ptchub.worldmanager.com/admin/login-next.php?logout=true'

browser.get(url)

user = browser.find_element(By.ID,"username")
pw = browser.find_element(By.ID,"password")
login = browser.find_element(By.ID,"loginbutton")

user.send_keys('1355.lewis')
pw.send_keys('Qweasd!2345')


request_Thub_Id =input('login?and Request Thub ID ?')

def copy_to_pyperclip(browser_item):
    pyperclip.copy('')
    action = ActionChains(browser)
    action.double_click(browser_item)
    action.double_click(browser_item)
    action.key_down(Keys.CONTROL)
    action.send_keys("c")
    action.key_up(Keys.CONTROL)
    action.perform()
    print(pyperclip.paste())
    return pyperclip.paste()

def get_contract_info(contract_id):

    url_candidate_Detail = f'https://ptchub.worldmanager.com/contracts/{contract_id}/steps/details/candidateAU'

    browser.get(url_candidate_Detail)

    browser.implicitly_wait(5)

    time.sleep(1)

    if 'Accepted' not in browser.find_element(By.CLASS_NAME,'wizard-status').text:
        print(browser.find_element(By.CLASS_NAME,'wizard-status').text)
        return 'Pending'

    else:

        Title = copy_to_pyperclip(browser.find_elements(By.CSS_SELECTOR,"div[class='input-control disabled']")[0])

        First_Name = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.firstName']"))

        Middle_Name = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.middleName']"))

        Last_Name = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.lastName']"))

        Date_of_Birth = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.dateOfBirth']"))

        Email = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='contact.emailAddress']"))

        Contact_number = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='contact.contactNumber']"))

        url_contract_Detail = f'https://ptchub.worldmanager.com/contracts/{contract_id}/steps/details/contractAU'

        browser.get(url_contract_Detail)

        Position_Type = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='employment.positionType']"))

        Contract_Type = copy_to_pyperclip(browser.find_elements(By.CSS_SELECTOR,"div[class='input-control disabled']")[1])

        Start_Date = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='employment.startsAt']"))

        Salary = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='salary.baseSalary']"))

        Award = copy_to_pyperclip(browser.find_elements(By.CSS_SELECTOR,"div[class='input-control disabled']")[3])

        Hourly_Rate = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='salary.hourlyRate']"))

        url_position = f'https://ptchub.worldmanager.com/contracts/{contract_id}/steps/details/positionAU'

        browser.get(url_position)

        Position = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.name']"))

        Location = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.location']"))

        Created_Date = copy_to_pyperclip(browser.find_element(By.CSS_SELECTOR,"input[data-slug='details.date']"))

        Company = copy_to_pyperclip(browser.find_elements(By.CSS_SELECTOR,"div[class='input-control disabled']")[2])

        Status = browser.find_element(By.CSS_SELECTOR,'wizard-status').text

        list = [contract_id,Title,First_Name,Middle_Name,Last_Name,Date_of_Birth,Email,Contact_number,Position_Type,Contract_Type,Start_Date,
                Salary,Award,Hourly_Rate,Position,Location,Created_Date,Company,Status]

        return list

def get_employee_info(thub_id):

    browser.get(f'https://ptchub.worldmanager.com/admin/ctrl?page=accounts%2FnewAccount&accountID={thub_id}&activeTab=profile')
    firstname = browser.find_element(By.ID,'firstName').get_attribute('value')
    lastname = browser.find_element(By.ID,'lastName').get_attribute('value')
    phone_number = browser.find_element(By.ID,'el-phone').get_attribute('value')
    email = browser.find_element(By.ID,'emailField').get_attribute('value')
    username = browser.find_element(By.ID,'username').get_attribute('value')

    browser.get(f'https://ptchub.worldmanager.com/admin/ctrl?page=accounts%2FnewAccount&accountID={thub_id}&activeTab=customFields')
    Address = browser.find_element(By.ID,'datafield-2').get_attribute('value')
    Bank_acc = browser.find_element(By.ID,'datafield-16').get_attribute('value')
    BSB = browser.find_element(By.ID,'datafield-6').get_attribute('value')
    Super_Member_Id = browser.find_element(By.ID,'datafield-10').get_attribute('value')
    SPIN_USI = browser.find_element(By.ID,'datafield-9').get_attribute('value')
    Super_company = browser.find_element(By.ID,'datafield-8').get_attribute('value')
    TFN = browser.find_element(By.ID,'datafield-7').get_attribute('value')
    Visa = browser.find_element(By.ID,'datafield-14').get_attribute('value')


    list = [thub_id,firstname, lastname, phone_number, email, username,Address,Bank_acc,BSB,Super_Member_Id,SPIN_USI,Super_company,TFN,Visa]

    return list

# get people info
if request_Thub_Id == 'OK':
    employee_list = []
    count = 0
    for i in range(1201,1350):
        try:
            employee_list.append(get_employee_info(str(i)))
            count = 0
        except:
            if count == 5:
                break
            count = count + 1
            pass

    pd.DataFrame(employee_list,columns=['thub_id','firstname', 'lastname', 'phone_number', 'email', 'username','Address',
                                        'Bank_acc','BSB','Super_Member_Id','SPIN_USI','Super_company','TFN','Visa'
                                        ],dtype='string').to_csv('employee_list.txt')

request_contract = input("Request_contract,OK?/n")

# get all contract ID

if request_contract =="OK":

    list_of_contract = []

    master_list = []

    list_of_contract = pd.read_csv(r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Documents\GitHub\pythonProject\Add_New\contract_id",header=None)[0].astype('string').to_list()

    for i in list_of_contract:
        return_info = get_contract_info(i)
        if return_info != 'Pending':
            master_list.append(return_info)

    pd.DataFrame(master_list,columns=['contract_id','Title','First_Name','Middle_Name','Last_Name','Date_of_Birth','Email',
                                      'Contact_number','Position_Type','Contract_Type','Start_Date','Salary',
                                      'Award','Hourly_Rate','Position','Location','Created_Date','Company','Status'
                                      ],dtype='string').to_csv('contract_info.txt')

