import win32process
import win32gui
import win32api
import win32con

# hwnd = win32gui.FindWindow(None, "Tower of Fantasy  ")
# if hwnd:
#     _, pid = win32process.GetWindowThreadProcessId(hwnd)
#     phandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid) #(Access Type, Inheritance,pid)
#     x,y = win32process.GetProcessWorkingSetSize(phandle)
#     print(x,y)

import win32gui

def get_window_geometry(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return {
            "x": left,
            "y": top,
            "width": right - left,
            "height": bottom - top
        }
    return None

# Usage
geometry = get_window_geometry("Tower of Fantasy  ")
print(geometry) 

# import win32gui
# def list_windows():
#     def callback(hwnd, extra):
#         if win32gui.IsWindowVisible(hwnd):
#             title = win32gui.GetWindowText(hwnd)
#             class_name = win32gui.GetClassName(hwnd)
#             rect = win32gui.GetWindowRect(hwnd)
#             print(f"Title: '{title}' | Class: '{class_name}' | Rect: {rect}")
#     win32gui.EnumWindows(callback, None)

# list_windows()

