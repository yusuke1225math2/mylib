import os
import sys
import pyautogui as pa
import pyperclip as pc
import time as ti
from time import sleep
import webbrowser as wb
import re
import mypa
import slack_lib
import file_manipulation as fm

def open_account(account_id, loadtime=6):
    url= 'https://twitter.com/' + account_id
    if os.name == 'nt':
        chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        wb.get(chrome_path).open(url)
    else:
        wb.open(url)
    sleep(loadtime)

# client info
root_str = '/Users/yusuketanbo/Dropbox/mycode/autofollowgui/'
client_db_str = 'db/m_account_list.csv'
client_db_list = fm.gen_list_from(root_str + client_db_str)
client_db_list = [row.replace('"', '').split(', ') for row in client_db_list]

def password_of(client_id):
    for client_info in client_db_list:
        if client_info[0] == client_id:
            return client_info[1]

def name_of(client_id):
    for client_info in client_db_list:
        if client_info[0] == client_id:
            return client_info[2]

def active_status_of(client_id):
    for client_info in client_db_list:
        if client_info[0] == client_id:
            return client_info[3]

def tag_of(client_id):
    for client_info in client_db_list:
        if client_info[0] == client_id:
            try:
                return client_info[4]
            except:
                return ''

# get text
def get_profile_txt(remove_target='', select_loadtime=1, copy_loadtime=1, trimming=1):
    pa.hotkey('command','a')
    mypa.wait(select_loadtime)
    pa.hotkey('command','c')
    mypa.wait(copy_loadtime)

    try:
        profile_html = mypa.getClip()
        mypa.wait(1)
    except:
        profile_html = ''

    if remove_target != '':
        profile_html.replace('@{}'.format(remove_target), '')

    if trimming:
        try:
            try:
                registered_at = re.findall(r'[0-9]{4}年[0-9]{1,2}月に登録', profile_html)[0]
            except:
                registered_at = ''

            profile_list = re.split(r'[0-9]{4}年[0-9]{1,2}月に登録' ,profile_html)
            return profile_list[0] + registered_at
        except:
            return ''
    else:
        return profile_html

def get_text_from_scroll(num, select_pause=5, copy_pause=3):
    if num < 5000:# スクロールで取得するアカウント数の上限を設定しておく
        scroll_sec = int(int(num) / 200 * 10 + 5)
    else:
        scroll_sec = int(int(5000) / 200 * 10 + 5)
        
    mypa.scrollDown(scroll_sec)
    mypa.selectAll()
    mypa.wait(select_pause)
    mypa.clipCopy()
    mypa.wait(copy_pause)
    out_text = mypa.getClip()
    mypa.wait(1)
    return out_text

def remove_recommended(text):
    return text.replace(r'おすすめユーザー[\S\s\n]*広告について','')

def extract_numbers_text(profile_text):
    try:
        profile_list = re.split(r'[0-9]{4}年[0-9]{1,2}月に登録' ,profile_html)
        return profile_list[0]
    except:
        return ''

# get id_list from text
def get_ids_from(text):
    idset = set(re.findall('@[a-zA-Z0-9_]{5,15}',text))
    idset = [id.replace('@', '') for id in idset]
    return idset

def get_following_ids_from(text):
    following_ids = re.findall(r'[a-zA-Z0-9_]{5,15}さんをフォローしています', text)
    following_ids = [s.replace('さんをフォローしています', '') for s in following_ids]
    return following_ids

def get_follower_ids_from(text):
    follower_ids = re.findall(r'[a-zA-Z0-9_]{5,15}[\S\s]{2,3}フォローされています', text)
    follower_ids = [s.replace(u'\u200f', '') for s in follower_ids]
    follower_ids = [s.replace(r' ', '') for s in follower_ids]
    follower_ids = [s.replace(r'フォローされています', '') for s in follower_ids]
    return follower_ids

# judgement from text
def fullfills_conditions(profile_html_sliced, only_keywords=[]):
    following_num = get_following_num_from(profile_html_sliced)
    follower_num = get_follower_num_from(profile_html_sliced)
    tweet_num = get_tweet_num_from(profile_html_sliced)
    like_num = get_like_num_from(profile_html_sliced)

    followingSufficient = 50
    tweet_minimum = 5
    like_minimum = 0
    following_ratioSufficient = 1.5

    if follower_num > 0:
        following_ratio = following_num / follower_num
    else:
        following_ratio = 0

    # フォローする条件の羅列
    fulfilment = 0
    if is_following(profile_html_sliced) != 1:
      if tweet_num > tweet_minimum:
          fulfilment = 1  
      if following_num > followingSufficient:
          fulfilment = 1  
      if like_num > like_minimum:
          fulfilment = 1  
      if following_ratio >= following_ratioSufficient:
          fulfilment = 1  

    return fulfilment

def is_suspended(profile_text):
    suspended_match = re.search(r'電話番号を確認|パスワードを変更してください|ご利用のアカウントは一時的に機能が制限されています|お使いのアカウントに不自然なアクティビティを検出しました。',profile_text)
    if suspended_match:
        return 1
    else:
        return 0

def do_not_follow(profile_html_sliced, except_keywords=[]):
    nosignalStr = 'インターネットに接続されていません'# インターネット接続がない場合の処理
    nosignalMatch = re.search(nosignalStr,profile_html_sliced)
    if nosignalMatch:
        print('No internet connection')
        sys.exit()

    # 非公開・存在しないアカウント・ツイートの無いアカウントの判定
    protectedMatch = re.search(r'(非公開ツイート|凍結済みアカウント|フォロー中|接続されていません|制限されています|ツイートしていません|存在しません|非公開です。)',profile_html_sliced)
    do_not_follow = 0
    if protectedMatch:
        do_not_follow = 1
    
    if is_spam(profile_html_sliced):
        do_not_follow = 1
    
    return do_not_follow

def is_spam(profile_html_sliced):
    matching = re.search(r'(相互|相互フォロー|フォローバック|100%)',profile_html_sliced)
    is_spam = 0
    if matching:
        is_spam = 1
    ti.sleep(1)
    return is_spam

def is_following(profile_html_sliced):
    protectedMatch = re.search(r'(フォロー中)',profile_html_sliced)
    is_following = 0
    if protectedMatch:
        is_following = 1
    ti.sleep(1)
    return is_following
    
# get number from text
def get_following_num_from(profile_html_sliced):
    followingMatch = re.search(r'フォロー\n[0-9,]+\n',profile_html_sliced)
    if followingMatch:
        followingText = followingMatch[0]
        following_numMatch = re.search('[0-9,]+',followingText)
        try:
            following_num = int(following_numMatch[0].replace(',',''))
        except ValueError:
            following_num = 0
    else:
        following_num = 0
    return following_num

def get_follower_num_from(profile_html_sliced):
    followerMatch = re.search(r'フォロワー.*?\n[0-9,]+\n',profile_html_sliced)
    if followerMatch:
        followerText = followerMatch[0]
        follower_numMatch = re.search('[0-9,]+',followerText)
        try:
            follower_num = int(follower_numMatch[0].replace(',',''))
        except ValueError:
            follower_num = 0
    else:
        follower_num = 0
    return follower_num

def get_like_num_from(profile_html_sliced):
    likeMatch = re.search(r'いいね[\S\s]+?[0-9,]+',profile_html_sliced)
    if likeMatch:
        likeText = likeMatch[0]
        like_numMatch = re.search('[0-9,]+',likeText)
        try:
            like_num = int(like_numMatch[0].replace(',',''))
        except ValueError:
            like_num = 0
    else:
        like_num = 0
    return like_num

def get_tweet_num_from(profile_html_sliced):
    tweetMatch = re.search(r'ツイート[\S\s]+?\n.+?[0-9,]+',profile_html_sliced)
    if tweetMatch:
        tweetText = tweetMatch[0]
        tweet_numMatch = re.search('[0-9,]+',tweetText)
        try:
            tweet_num = int(tweet_numMatch[0].replace(',',''))
        except ValueError:
            tweet_num = 0
    else:
        tweet_num = 0
    return tweet_num

def get_registered_at_from(profile_html_sliced):
    tweet_match = re.search(r'[0-9]{4}年[0-9]{1,2}月に登録',profile_html_sliced)
    if tweet_match:
        registered_str = tweet_match[0]
        registered_at = registered_str.replace('月に登録', '').replace('年', '-')
    else:
        registered_at = '0000-00'
    return registered_at

def get_name_from(profile_html_sliced):
    name_match = re.search(r'ユーザーアクション\n.*?\n',profile_html_sliced)
    if name_match:
        name_str = name_match[0]
        name = name_str.replace('ユーザーアクション\n', '').replace('\n', '')
    else:
        name = 'ERROR'
    return name

def get_introduction_from(profile_html_sliced):
    introduction_match = re.search(r'ユーザーアクション\n.*?\n@.*\n.*', profile_html_sliced)
    if introduction_match:
        introduction_str = introduction_match[0]
        introduction = introduction_str.split('\n')[-1]
        introduction = re.sub(r'[0-9]{4}年[0-9]{1,2}月に登録', '', introduction)
    else:
        introduction = 'ERROR'
    return introduction
