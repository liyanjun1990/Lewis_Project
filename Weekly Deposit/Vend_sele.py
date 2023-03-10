from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # explictly wait
from selenium.webdriver.support import expected_conditions as EC  # explictly wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd
import os
import re
from datetime import datetime
from datetime import timedelta

import pyperclip
import tkinter as tk
from tkinter import ttk
import pyautogui

import itertools
import threading
import sys

## path
from bs4 import BeautifulSoup
import pandas as pd

todayis = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

download_path = r'C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Documents\GitHub\pythonProject\Deposit_Check\VR\\'

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_path}
chromeOptions.add_experimental_option("prefs",prefs)

#browser = webdriver.Chrome(r"C:\Users\admin\Desktop\AUTO\chromedriver.exe",options=chromeOptions)
browser = webdriver.Chrome(r"C:\Users\Accounting - 10102\Desktop\AUTO\chromedriver.exe",options=chromeOptions)

browser.get('https://ptcrepairs.vendhq.com/dashboards')

def wait_for(key_str,wait_time=4,type='find',manual_text='WHAT?'):
    # get the stamp and put sleeps
    check_point_now = datetime.now().timestamp()
    check_point_then = check_point_now
    if type == 'find':
        while check_point_now + wait_time > check_point_then:
            time.sleep(wait_time/5)
            check_point_then = datetime.now().timestamp()
            try:
                browser.find_element(By.CSS_SELECTOR, key_str)
                return
            except:
                print('Waiting-find')
                pass

    elif type == 'dif':
        check_word_now = browser.find_element(By.CSS_SELECTOR,key_str).text
        print(check_word_now)
        check_word_then = check_word_now
        while check_point_now + wait_time > check_point_then:
            check_point_then = datetime.now().timestamp()
            time.sleep(wait_time / 5)
            try:
                check_word_then = browser.find_element(By.CSS_SELECTOR,key_str).text
                print(check_word_then)
                if check_point_then != check_word_now:
                    return
                print('Waiting-dif')
            except:
                print('Waiting-dif')
                pass
    elif type == 'click':
        while check_point_now + wait_time > check_point_then:
            time.sleep(wait_time/5)
            check_point_then = datetime.now().timestamp()
            try:
                browser.find_element(By.LINK_TEXT,key_str).click()
                return
            except:
                print('Waiting-click')
                pass
    # pass the wait
    pyautogui.confirm(text=manual_text)

# need to change the following

date_from = input("date_from dd/mm/yyyy, take one more day")
#date_from = '13/06/2022'
date_from = datetime.strptime(date_from,"%d/%m/%Y")
print("Enter Start_Page")
start_page = int(input())
#start_page = 5

df = pd.DataFrame()
count = 0
for i in range(start_page,100):
    browser.get(f'https://ptcrepairs.vendhq.com/register/closures?page={i}')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find_all('table',{'class':'item_list table-fixed headers-sortable static-aside'})[0]
    df_temp = pd.read_html(str(table))[0]
    list_href = ["https://ptcrepairs.vendhq.com/" + i.get('href') for i in soup.find_all('a',{'href':re.compile('register/closure/summary/')})]
    df_temp['href'] = list_href
    df = pd.concat([df,df_temp])
    check_date = ",".join(df.iloc[-1, 3].split(",")[0:2])
    check_date = datetime.strptime(check_date,"%b %d, %Y")
    count += 1
    print(check_date,"",str(count))
    browser.find_element(by=By.LINK_TEXT,value='Export CSV').click()
    while count != len(os.listdir(download_path)):
        next_step = input("Downloaded?")
        if next_step == "Y":
            break
    if check_date < date_from:
        break


df['merge_helper'] = [i + str(j) for i,j in zip(df['Register'],df['#'])]

df.to_csv(r"C:\Users\Accounting - 10102\OneDrive - PTC Phone Tech and Comm\Documents\GitHub\pythonProject\Deposit_Check\url.csv",index=False)