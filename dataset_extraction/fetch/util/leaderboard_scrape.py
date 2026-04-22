#script to pull contest leaderboard data
#for  first 10000 users  till 400 pg

from curl_cffi import requests
import json
import random
import logging
import time
import os
import config

def getLeaderBoardPage(START_PAGE,END_PAGE,CONTEST,CONTESTSLUG):

    output_path=(
        config.ROOT_DIR /'dataset'/f'contest_{CONTEST}' /'leaderboard'
    )
    output_path_log= config.ROOT_DIR /'dataset'/f'contest_{CONTEST}' / 'leaderboard_log.txt'
    logging.basicConfig(filename=output_path_log,format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG)
    # os.mkdir(f"{CONSTESTSLUG}_leaderboard")

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://leetcode.com/',
        'Content-Type': 'application/json',
        'Sec-Ch-Ua-Platform-Version':'19.0.0',
        'Sec-Ch-Ua-Platform':"Windows",
        'Sec-Ch-Ua-Model':"",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Bitness" : "64",
        "Sec-Ch-Ua-Arch":"x86"
    }
    session.headers.update(headers)

    for i in range(START_PAGE,END_PAGE+1):
        contest_ranking_url=f"https://leetcode.com/contest/api/ranking/{CONTESTSLUG}/?pagination={i}&region=global"
        response=session.get(contest_ranking_url,impersonate='chrome')
        if(response.status_code !=200):
            logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
            logging.error(f"response was {response.txt}")
            break
        else :
            try:
                data = response.json()
                output_path_ld= output_path / f'leaderboard_{i}.json'
                output_path_user= config.ROOT_DIR / 'dataset' / f'contest_{CONTEST}'/'user'/f'pg_{i}'
                output_path_user.mkdir(parents=True,exist_ok=True)
                dump_file=open(output_path_ld,'w')
                json.dump(data,dump_file,indent=2)
                logging.debug(f"success for page {i}")
                dump_file.close()
            except ValueError:
                logging.error(f"invalid JSON page : {i}")  #here if get a captcha page then html file will be loaded
                logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
                logging.error(response.text)
        
        time.sleep(random.randint(4,10))


#test
if __name__ == '__main__':
    START_PAGE=1
    END_PAGE=2
    CONTEST=496
    CONTESTSLUG="weekly-contest-496"
    getLeaderBoardPage(START_PAGE,END_PAGE,CONTEST,CONTESTSLUG)





