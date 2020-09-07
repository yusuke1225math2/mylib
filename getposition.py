#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

import pyautogui as pa
import pyperclip as pc

xy = pa.position()
print(xy)
pc.copy(str(xy))
