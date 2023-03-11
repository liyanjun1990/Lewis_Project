import time
import re
from datetime import datetime

import pyperclip
import tkinter as tk
import pyautogui

default_x = 1841
default_y = 144
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Enter Employee"
        self.hi_there["command"] = self.enter_basic_info
        self.hi_there.pack(side="top")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Enter Address and TFN"
        self.hi_there["command"] = self.add_ATFN
        self.hi_there.pack(side="top")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Enter Stauts"
        self.hi_there["command"] = self.add_status
        self.hi_there.pack(side="top")
    def enter_basic_info(self):
        global  EMPINFO
        EMPINFO = pyautogui.prompt(title="Employee_Info")
        EMPINFO = EMPINFO.split("\n")
        next_step = pyautogui.confirm(buttons=['OK','STOP'])
        if next_step == 'STOP':
            return
        pyautogui.click(pyautogui.position())
        pyautogui.write(EMPINFO[0])
        pyautogui.press('tab')
        pyautogui.write(EMPINFO[1])
        pyautogui.press('tab')
        pyautogui.write(EMPINFO[2][:8])
        pyautogui.press('tab')
        Start_date = datetime.strptime(EMPINFO[3], "%d/%m/%Y").strftime("%d/%m/%Y")
        pyautogui.write(Start_date)

    def add_ATFN(self):
        address = pyautogui.prompt(default= EMPINFO[5])
        next_step = pyautogui.confirm(title='To the Top of the field',buttons=['OK','STOP'])
        if next_step == 'STOP':
            return
        address = address.split(",")
        address = [i.strip() for i in address]
        address_line1 = address[0]
        address_sub = address[1]
        address_state_position = re.search(" ",address[2]).span()[0]
        address_state = address[2][:address_state_position]
        address_code = address[2][address_state_position+1:]

        pyautogui.click(pyautogui.position())
        pyautogui.write(address_line1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(address_sub)
        pyautogui.press('tab')
        pyautogui.write(address_state)
        pyautogui.press('tab')
        pyautogui.write(address_code)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(EMPINFO[6])
        pyautogui.press('tab')
        pyautogui.write(EMPINFO[7][:31])
        pyautogui.press('tab')
        pyautogui.write(EMPINFO[8])
        pyautogui.confirm(text=f'Claim Tax Thredhold: {EMPINFO[10]} \n Student Loan: {EMPINFO[11]}')

    def add_status(self):
        employe_id = pyautogui.prompt(title='Employee_Id')
        Gender = pyautogui.confirm(text=EMPINFO[12],buttons=['Male','Female'])
        Status_3 = pyautogui.confirm(text=EMPINFO[13],buttons=['Casual','Perman'])
        if Status_3 == 'Casual':
            Status_1 = 'Full'
            Status_2 = 'Wage'
        elif Status_3 == 'Perman':
            Status_1 = pyautogui.confirm(text=EMPINFO[13],buttons=['Full','Part'])
            Status_2 = pyautogui.confirm(text=EMPINFO[14], buttons=['Wage', 'Salary'])

        next_step = pyautogui.confirm(buttons=['OK','STOP'])
        if next_step == 'STOP':
            return

        pyautogui.click(pyautogui.position())
        pyautogui.write(Gender)
        pyautogui.press('tab')
        pyautogui.write(Status_1)
        pyautogui.press('tab')
        pyautogui.write(Status_2)
        pyautogui.press('tab')
        pyautogui.write(Status_3)
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.write('0')
        pyautogui.press('tab')
        pyautogui.write('0')
        pyautogui.press('tab')
        Birth_day = datetime.strptime(EMPINFO[16], "%d/%m/%Y").strftime("%d/%m/%Y")
        pyautogui.write(Birth_day)
        pyautogui.press('tab')

        pyautogui.confirm(text=f'Leave Title: {EMPINFO[17]} Leave Loading: {EMPINFO[18]}')

        pyautogui.confirm(text=f'Email: {EMPINFO[19]}')

        cur_x = pyautogui.position()[0]
        cur_y = pyautogui.position()[1]

        pyautogui.click(x=default_x, y=default_y)
        pyautogui.write(EMPINFO[19])

        pyautogui.moveTo(cur_x,cur_y)

        pyperclip.copy(EMPINFO[21])
        pyautogui.confirm(title='PLEASE DOUBLE CHECK',text=f'Number: {EMPINFO[21]} \n USI: {EMPINFO[20]} \n Super :{EMPINFO[22]}')
        # add bank
        step = pyautogui.confirm(text=f'BSB: {EMPINFO[23]} \n Account: {EMPINFO[24]}')
        if step == 'OK':
            pyautogui.click(x=default_x, y=default_y)
            pyautogui.write(EMPINFO[23])
            pyautogui.write(EMPINFO[24])
            pyautogui.write('WAGES')
            pyautogui.confirm(text=f'BSB: {EMPINFO[23]} \n Account: {EMPINFO[24]}')
        pyautogui.confirm(title=f'ID : {employe_id}',text=f'{Status_3} \n Assign Rate {Status_2} \n Rate: {EMPINFO[26]}')

root = tk.Tk()
root.geometry("+0+0")
app = Application(master=root)
app.mainloop()