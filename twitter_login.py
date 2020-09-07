#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

import webbrowser as wb
import sys
import mypa
from time import sleep
import twitter_account_info as twinfo

def switch_twitter_to(name, csvlogin=0):
      wb.open('https://twitter.com')
      sleep(4)
      logout_twitter()
      if csvlogin == 1:
            login_by_csv(name, twinfo.password_of(name))
      else:
            login_twitter_of(name)

def logout_twitter(loadtime=10):
    mypa.execMacro('LogoutTwitter.iim')
    sleep(loadtime)

    # suspended validation
    mypa.selectAll()
    sleep(0.3)
    mypa.clipCopy()
    sleep(0.3)
    profile_text = mypa.getClip()
    if twinfo.is_suspended(profile_text):
      mypa.execMacro('LogoutWhenSuspended.iim')
      sleep(loadtime)

def login_twitter_of(account_name, loadtime=15):
    mypa.execMacro('LoginTwitterOf{}.iim'.format(account_name))
    sleep(loadtime)
    mypa.closeTab()
    sleep(1)

def login_by_csv(id, password, loadtime=7):
    mypa.execMacro('LoginFromCSV.iim')
    sleep(3)
    mypa.pasteStr(id + '/' + password)
    sleep(0.2)
    mypa.paReturn()
    sleep(loadtime)

