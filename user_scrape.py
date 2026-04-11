# script to extract each user data according to leaderboard.json of that contest


from curl_cffi import requests
import json
import random
import logging
import time
import os

START_PAGE=int(input("Enter start page : "))
END_PAGE=int(input("Enter end page : "))

PAGE_WINDOW_SIZE=10
graphql_url = 'https://leetcode.com/graphql'




query = """
query userPublicProfile($username: String!) {

  matchedUser(username: $username) {
    username
    profile {
      ranking
      realName
      countryName
      postViewCount
      reputation
    }
    submitStats {
      acSubmissionNum{
        difficulty
        count
        submissions
      }
    }
  }

  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    topPercentage
  }
  
  userContestRankingHistory(username: $username) {
    attended
    trendDirection
    problemsSolved
    ranking
    rating
    contest{
      title
      startTime
    }
  }
}
"""

def giveRankList(page):
    jFile=open(f'contest_496/leaderboard/leaderboard_{page}.json', 'r')
    data=json.load(jFile)
    rankList=[] #rankList[i]= user_slug at rank i
    for i in range(0,24+1):
        rankList.append(data['total_rank'][i]['user_slug'])
    return rankList

logging.basicConfig(filename=f'496_user_log.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG)

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

isOk=True

k= int((END_PAGE-START_PAGE+1)/PAGE_WINDOW_SIZE)
logging.info(f"staring process for {START_PAGE} to {END_PAGE} in batches of {PAGE_WINDOW_SIZE}, total Batches = {k+1}")
for batch in range(0,k):
    curr_start_page = START_PAGE + batch*PAGE_WINDOW_SIZE
    curr_end_page= curr_start_page + PAGE_WINDOW_SIZE-1
    logging.info(f"starting process of {curr_start_page} to {curr_end_page}")
    for page in range(curr_start_page,curr_end_page+1):
        os.mkdir(f'contest_496/user/pg_{page}')
        rankList=giveRankList(page)
        for i in range(0,len(rankList)):
            variables = {
                "username": rankList[i]
            }

            payload = {
                "query": query,
                "variables": variables
            }
            
            response = session.post(graphql_url, json=payload,impersonate='chrome') #main line
            try:
                data=response.json()
                dump_file=dump_file=open(f"contest_496/user/pg_{page}/{i}.json",'w')
                json.dump(data,dump_file,indent=2)
            except:
                #html tag print respnonse in debug /critical error/ give page and index
                logging.critical(f"ERROR on page : {page} , rank : {i}") #rank will be b/w 0,24 of that page json file
                logging.critical(response.text)
                isOk=False
                break
            
            time.sleep(random.randint(1,5))

        if(isOk==False):
            logging.critical(f"terminating program at page : {page}")
            break
        logging.debug(f"SUCCESSFULLY FETCHED PAGE : {page}")
        time.sleep(random.randint(10,15))
    
    if(isOk==False):
        break
    time.sleep(random.randint(60,120))
        

if(isOk):
    logging.info(f"success in fetching all pages from {START_PAGE} to {END_PAGE}")