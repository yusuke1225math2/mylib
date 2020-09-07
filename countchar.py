#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

import pyperclip as pc
import re


src = pc.paste()
src = src.replace('\n','')

src = re.sub('\[.*?\]','',src)
src = re.sub('【.*?】','',src)

print(len(src))
