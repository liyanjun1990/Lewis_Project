# Description of File

### Essential_API 2.0.py
The function of the script is to extract the essential employee data from MYOB essential, which will then be applied to construct the employee dimension table.

### API Report 1.0.py
the purpose of the script is to utilize the Essentials API for requesting the balance sheet and profit and loss statement. This data will be utilized as a source in Power Query. Consequently, Excel will generate the profit and loss statement for seven different entities.

### Generate_Report.bas
The purpose of the VBA script is to create a monthly balance sheet and profit and loss report from the data source requested from API report 1.0.py through Power Query. These statements will be generated under separate tabs in Excel and utilized for consolidated financial reporting.
