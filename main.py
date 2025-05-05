import excels

# def listWindows():
#     def callback(hwnd, extra):
#         if win32gui.IsWindowVisible(hwnd):
#             windowTitle = win32gui.GetWindowText(hwnd)
#             windowClass = win32gui.GetClassName(hwnd)
#             windowRect = win32gui.GetWindowRect(hwnd)

#             print (f"Title: '{windowTitle}' | Class: '{windowClass}' | Rect: {windowRect}")
#     win32gui.EnumWindows(callback, None)

# listWindows()

# def locateWindow(window_name):
#     hwnd = win32gui.FindWindow(None, window_name)
#     if hwnd:
#         left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#         return {f"x: {left} y: {top}, height: {right - left}, width: {bottom - top}"}
#     else:
#         return None
    
# print(locateWindow("main.py - tof - Visual Studio Code [Administrator]"))
        


