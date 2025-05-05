import win32com.client

# Start Excel COM instance
excel = win32com.client.Dispatch("Excel.Application")
# excel.Visible = True  # Set to True if you want to see Excel open

# Create a new workbook and access the first sheet
save_path = r"C:\YAD\YADP\Python\tof\example4.xlsx"
workbook = excel.Workbooks.Open(save_path)
sheet = workbook.Sheets(1)
for i in range(1,5):
    for j in range(1,3): 
        sheet.Cells(i,j).Value = "Hello COM"

# Save the workbook
  # Change this path
workbook.Save(save_path)

# Close Excel
# workbook.Close(SaveChanges=False)
# excel.Quit()
