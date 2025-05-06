import pygetwindow as pw

# winTitles = pw.getAllTitles()
# print(winTitles)

# win = pw.getAllWindows()
# print(win)

# win1 = pw.getActiveWindowTitle()
# print(win1)


win = pw.getWindowsWithTitle('Tower of Fantasy  ')[0]
print(win)
# print(dir(win))    # win properties
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', 
# '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
#  '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
# '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', 
# '__subclasshook__', '__weakref__', '_getWindowRect', '_hWnd', '_rect', '_setupRectProperties', 
# 'activate', 'area', 'bottom', 'bottomleft', 'bottomright', 'box', 'center', 'centerx', 'centery', 
# 'close', 'height', 'hide', 'isActive', 'isMaximized', 'isMinimized', 'left', 'maximize',
#  'midbottom', 'midleft', 'midright', 'midtop', 'minimize', 'move', 'moveRel', 'moveTo', 'resize', 
# 'resizeRel', 'resizeTo', 'restore', 'right', 'show', 'size', 'title', 'top', 'topleft', 'topright', 
# 'visible', 'width']

# x = win.left
# y = win.top
# width = win.width
# height = win.height

win.resizeTo(720,480)
win.moveTo(0,0)
x, y, width, height = win.left, win.top, win.width, win.height
print(f"x: {x}, y: {y}, width: {width}, height: {height}")
print(win.center)
