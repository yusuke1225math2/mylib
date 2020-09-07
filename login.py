#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

import webbrowser as wb
import mypa
import sys
from time import sleep

if __name__ == '__main__':
  try:
    platform = sys.argv[1]
    account = sys.argv[2]
  except:
    print('Plz input PLATFORM ACCOUNT_NAME')
    sys.exit()

  wb.open('https://google.com')
  sleep(1)
  mypa.secretWindow()
  sleep(3)
  mypa.execMacro('Login{}Of{}.iim'.format(platform, account))
