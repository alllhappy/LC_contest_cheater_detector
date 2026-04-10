#script to pull contest leaderboard data
#for  first 10000 users  till 400 pg

from curl_cffi import requests
import json
import random
import logging
import time

START_PAGE=int(input("enter Start PAGE : "))
END_PAGE=int(input("enter end page value : "))
CONSTESTSLUG="weekly-contest-496"
logging.basicConfig(filename=f'{CONSTESTSLUG}_leaderboard_log.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG)

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
    contest_ranking_url=f"https://leetcode.com/contest/api/ranking/{CONSTESTSLUG}/?pagination={i}&region=global"
    response=session.get(contest_ranking_url,impersonate='chrome')
    if(response.status_code !=200):
        logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
        logging.error(f"response was {response.txt}")
        break
    else :
        try:
            data = response.json()
            dump_file=open(f"contest_496/leaderboard_{i}.json",'w')
            json.dump(data,dump_file,indent=2)
            logging.debug(f"success for page {i}")
        except ValueError:
            logging.error(f"invalid JSON page : {i}")  #here if get a captcha page then html file will be loaded
            logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
            logging.error(response.text)
    time.sleep(random.randint(4,10))
            




