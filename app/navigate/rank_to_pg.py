'''
Script to navigate me to automatically navigate me to that leaderboard pg on which a given rank is present
This is being done to review recordings and open the profile
'''

import webbrowser
import time

brave_path=f"C:/Users/karan/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path)) #https://chatgpt.com/share/69ddc7a7-42e4-8324-b3ba-a79cc39f405b
CONTEST_494_LINK=f"https://leetcode.com/contest/weekly-contest-494/ranking"
CONTEST_495_LINK=f"https://leetcode.com/contest/weekly-contest-495/ranking"
CONTEST_496_LINK=f"https://leetcode.com/contest/weekly-contest-496/ranking"

def getContestLdLink(contest,rank):
    rank= rank -1 #ranks start with 1 , but our calculation fits for starting from 0
    ld_pg= int(rank / 25) + 1
    index= rank % 25
    return f"https://leetcode.com/contest/weekly-contest-{contest}/ranking/{ld_pg}/region=global_v2"

links=[CONTEST_494_LINK,CONTEST_495_LINK,CONTEST_496_LINK]

def navigate(rank,contest,user_slug):
    rank= rank -1 #ranks start with 1 , but our calculation fits for starting from 0
    ld_pg= int(rank / 25) + 1
    index= rank % 25
    print(f'leaderd board page = {ld_pg}')
    print(f'index = {index}')
    link=""
    if(contest==494):
        link=links[0]
    elif(contest==495):
        link=links[1]
    elif(contest==496):
        link=links[2]
    else:
        print('contest does not exist')
        return
    complete_link=f'{link}/{ld_pg}/region=global_v2'
    webbrowser.get('brave').open_new_tab(complete_link) #contest link
    time.sleep(2)
    webbrowser.get('brave').open_new_tab(f'https://leetcode.com/u/{user_slug}') #profile link
def getProfileLink(user_slug):
    return f'https://leetcode.com/u/{user_slug}'

if __name__ == '__main__':
    while(True):
        rank=int(input("enter rank :"))
        if(rank == -1): break
        contest=int(input('enter contest :'))
        #first 60 users of contest 494 only
        # contest=494
        user_slug=input('user_slug : ')
        navigate(rank,contest,user_slug)




# webbrowser.open_new_tab(CONTEST_494_LINK)