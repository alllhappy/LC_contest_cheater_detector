'''
Run this file from project root
input = contest number , rankRange
output = contest folder having final csv file of user details
command to run this file from project root : python -m dataset-extraction.fetch.main 
'''

#write imports from project root
from pathlib import Path
import config
import dataset_extraction.fetch.util.contest_info as ci
import dataset_extraction.fetch.util.leaderboard_scrape as ld
import dataset_extraction.fetch.util.user_scrape as us
import dataset_extraction.fetch.util.jsToCsv as jsToCsv




#first make directories
def createDir(contest):
    output_path_ld= (
        config.ROOT_DIR /'dataset'/f'contest_{contest}'/'leaderboard'
    )
    output_path_us=(   
        config.ROOT_DIR /'dataset'/f'contest_{contest}'/'user'
    )
    
    output_path_ld.mkdir(parents=True,exist_ok=True)
    output_path_us.mkdir(parents=True,exist_ok=True) #if already exists then do nothing

if __name__ == '__main__':
    CONTEST=int(input("enter contest number"))
    if(CONTEST > 200):
        CONTESTSLUG=f'weekly-contest-{CONTEST}'
    else:
        CONTESTSLUG=f'biweekly-contest-{CONTEST}'
    createDir(CONTEST)
    ci.getContestInfo(CONTEST)
    startRank = int(input('Enter Start Rank :'))
    endRank= int(input('Enter End Rank : '))
    startPg= int((startRank-1) / 25) + 1
    endPg= int((endRank-1)/25)  + 1
    ld.getLeaderBoardPage(startPg,endPg,CONTEST,CONTESTSLUG)
    us.getUsers(CONTEST,startPg,endPg)
    jsToCsv.generateCSV(CONTEST)
    

