import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import win32com.client
import pandas as pd

dir_path = sys.path[0]

date = datetime.now(ZoneInfo("Asia/Chongqing"))
formatted_date = date.strftime("%d%b%Y")
formatted_time = float(date.strftime("%H.%M"))

if formatted_time > 12:
    print("Its time")
else:
    print("Its not right time yet"
          "\nCorrect time =< 12:00"
          f"\nCurrent time = {date.strftime("%H:%M")}")

file_name = "tof"+formatted_date+".xlsx"
file_path = dir_path+"\\"+file_name
creds_path = dir_path+"\\"+"accounts.xlsx"
df = pd.read_excel(creds_path)
creds = df[['ign']]
n = len(creds)
status_col = 2
debug_col = 3

def status_update(i,value):
    val = value
    sheet.Cells(i,2).Value = val

def debug_update(i,value):
    val = value
    sheet.Cells(i,3).Value = val


excel = win32com.client.Dispatch("Excel.Application")
if os.path.exists(file_path):
    workbook = excel.Workbooks.Open(file_path)
    sheet = workbook.Sheets(1)

    # sheet.Cells(14,2).Value = "TESTT"
    # sheet.Cells(20,status_col).Value = "well"
    # sheet.Cells(20,debug_col).Value = "welll"
    workbook.Save()

else:
    workbook = excel.Workbooks.Add()
    sheet = workbook.Sheets(1)

    creds['status'] = "not checked"
    creds['debug'] = ""
# Write headers
    for col_num, column_name in enumerate(creds.columns, start=1):
        sheet.Cells(1, col_num).Value = column_name

# Write data rows
    for row_num, row in enumerate(creds.values, start=2):  # Start at row 2
        for col_num, value in enumerate(row, start=1):
            sheet.Cells(row_num, col_num).Value = value

    workbook.SaveAs(file_path)

excel.Visible = True

