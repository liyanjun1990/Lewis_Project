# Description of File

## Add New Staff

### contract_information
The purpose of this script is to utilize Selenium to extract employee contract information from T-hub, a platform that charges for each API request. By using this script, you can avoid incurring additional charges and instead directly obtain the necessary employee contract data from T-hub. The collected data can then be conveniently integrated into your payroll system using EXO.py.

### EXO.py
This script is intended to utilize the PyAutoGUI library and guide the user in entering employee information into a payroll system, as there is no import option available.

## Fetch information from payroll System, MYOB API to get the recent employee information, such as payrun, leave balance and ect

### Essential_API 2.0.py
The function of the script is to extract the essential employee data from MYOB essential, which will then be applied to construct the employee dimension table.

### Combine_List.py
This script is employed to retrieve employee data from the EXO payroll database and merge it with the information obtained from MYOB essential.

### Check_RateTable.py
The primary purpose of this script is to perform an integrity check on the pay rates of employees and ensure that they have been set up accurately according to the Modern Award. Additionally, the script verifies whether the cost center has been configured correctly.

## Automate Public Holiday pay calculation

### Regular_hours_Weighted.py
The purpose of this script is to accurately calculate the weekly normal work hours of employees in the retail industry, which can be subject to flexibility. 
In addition, the script compares these work hours to the agreed-upon employee hours to determine whether the agreement is still current. The output of this calculation is then utilized to calculate both public holiday non-work hours pay and public holiday penalty time of in lieu pay. 

### Template_AddHours1.1.py
The purpose of this script is to accurately calculate both public holiday non-work hours pay and public holiday penalty time of in lieu pay. These calculations are based on the current payrun timesheet, as well as individual employee regular hours that are generated using the Regular_Hours_Weighted.py script.

## Excel interface for payroll process (due to the condidential information, the excel sheet is not in the folder)
A user interface has been developed in Excel to conduct integrity checks on timesheets.

In cases where a full-time employee or a salaried employee fails to work the required number of hours (76 hours), the system will automatically assign leave entitlement to make up for the shortage. This will be done in a specific order, starting with time in lieu overtime, followed by time in lieu public holiday penalty, approved sick leave, approved annual leave, and then approved unpaid leave. The system will then generate a report of any shortfall, which can be used to communicate with the Area Manager about any discrepancies such as insufficient work hours, excessive use of approved annual leave or sick leave, or a low balance of available leave.

## Entry_Check_List2.0.py
The script is intended to create transactions in the payroll fact database based on the modifications made in the Excel interface.

Once the Area Manager has completed the shortage report, adjustments will be made to the timesheet using the Excel interface. The Entry_Check_List2.0.py will generate transactions to reflect the adjustments, which will then be added to the payroll database and made available for importing into the payroll system.

## Excel interface (due to the condidential information, the excel sheet is not in the folder)
The timesheet from the payroll fact database can be exported in CSV format using the Excel interface, which is compatible with both EXO and payroll systems.

Once the timesheet is imported into the EXO and Essential payroll system, a comparison will be performed between the payrun results and the timesheet to verify the accuracy of the payment and the super payable at the employee level.



