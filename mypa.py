import pyautogui as pa
import webbrowser as wb
import time as ti
import pyperclip as pc


#Shortcut Key
def selectAll():
    pa.hotkey('command','a')

#Browser Manipulation
def secretWindow():
    pa.hotkey('command','shift','n')

def move_to_addressbar():
    pa.hotkey('command','l')

def closeTab():
    pa.hotkey('command','w')

def reloadPage():
    pa.hotkey('command','r')

#Clipboard
def clipCopy():
    pa.hotkey('command','c')

def clipPaste():
    pa.hotkey('command','v')

def intoClip(str):
    pc.copy(str)

def getClip():
    return pc.paste()

def pasteStr(str):
    intoClip(str)
    ti.sleep(0.4)
    clipPaste()

#Key Control
def paReturn():
    pa.typewrite(['return'])

def paDown():
    pa.typewrite(['down'])

def wait(second=0.5):
    ti.sleep(second)

# brosermanipulation
def scrollDown(sec):
        start = ti.time()
        for i in range(100000000):#secの間スクロールする
                pa.typewrite(['space'])
                pa.typewrite(['space'])
                pa.typewrite(['space'])
                pa.typewrite(['space'])
                if ti.time() - start > sec:
                        break

# scraper
def scrapeTwitterIDintoClip():
    pa.moveTo(75, 539, 0.5)
    pa.rightClick(75, 539)
    pa.typewrite('scr')
    paReturn()
    wait(60)
    # pasteStr('//div[*]/div/div/div/div/div/span/a')
    pasteStr('//*[@id="react-root"]/div/div/div/main/div/div[2]/div/div/div/div/div[2]/section/div/div/div/div[*]/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div[1]/span')
    paReturn()
    wait(2)
    pa.hotkey('shift','tab')
    selectAll()
    clipCopy()


# imacros shortcut
def execMacro(iim_name):
    move_to_addressbar()
    wait(0.5)
    pasteStr(str(iim_name))
    wait(0.5)
    paDown()
    wait(0.5)
    paReturn()
