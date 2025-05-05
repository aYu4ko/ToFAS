import os
import win32gui
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import win32com.client
import pandas as pd

def checkwindow():
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        return True
    
def locatewindow():
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return (left, top, right - left, bottom - top)

    return None

def validatewindow():
    return x >= 0 and y >= 0 and width > 0 and height > 0 and width > height

def checkTime():
    if formatted_time > 12:
        print("Its time")
    else:
        print("Its not right time yet"
             "\nCorrect time =< 12:00"
            f"\nCurrent time = {date.strftime("%H:%M")}")

def status_update(i,value,status_col = 2):
    val = value
    sheet.Cells(i,status_col).Value = val

def debug_update(i,value,debug_col = 3):
    val = value
    sheet.Cells(i,debug_col).Value = val


#__________________________________________________________________________________________
#__________________________________________________________________________________________


window_title = 'Tower of Fantasy  '

if checkwindow():
    x,y,width,height = locatewindow()
    if validatewindow():
        print("Window Found")
        print(f"x: {x}, y:{y}, dimensions:({width}x{height})")
    print("Window found but not accessible, please make sure whole window is visible")
print("Window not found")


# Initializing paths, names and more

dir_path = sys.path[0]

date = datetime.now(ZoneInfo("Asia/Chongqing"))
formatted_date = date.strftime("%d%b%Y")
formatted_time = float(date.strftime("%H.%M"))

checkTime()

file_name = "tof"+formatted_date+".xlsx"
file_path = dir_path+"\\"+file_name
creds_path = dir_path+"\\"+"accounts.xlsx"

df = pd.read_excel(creds_path)
creds = df[['ign']]
n = len(creds)


excel = win32com.client.Dispatch("Excel.Application")
if os.path.exists(file_path):
    workbook = excel.Workbooks.Open(file_path)
    sheet = workbook.Sheets(1)
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