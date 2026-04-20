#program to fetch single user details  to pass it directly to model. should return a list of containing all necessary 31 or 32 features.
import json
import mapping
from curl_cffi import requests
import logging
import time


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

# logging.basicConfig(filename=f'fetch_user_log.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG)

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
def getUserDetails(ip_rank,ip_contest): #both inputs are int
    #first whole leaderboard page
    #then corresponding user from that leaderboard page only no need to extract all users of that page
    CONTESTSLUG=''
    if(ip_contest>200) : #it is weekly
        CONTESTSLUG= f'weekly-contest-{ip_contest}'
    else : #it is biweekly
        CONTESTSLUG = f'biweekly-contest-{ip_contest}'

    #initalize the headers and seession
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

    ip_rank= ip_rank -1 #ranks start with 1 , but our calculation fits for starting from 0
    ld_pg= int(ip_rank / 25) + 1
    index= ip_rank % 25

    contest_ranking_url=f"https://leetcode.com/contest/api/ranking/{CONTESTSLUG}/?pagination={ld_pg}&region=global"
    response_ld=session.get(contest_ranking_url,impersonate='chrome')
    # if(response.status_code !=200):
    #     '''error handling'''
    #     # logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
    #     # logging.error(f"response was {response.txt}")
    #     return
    # else :
    #     try:
    #         data = response.json()
    #     except ValueError:
    #         '''errorr handling make in log file'''
    #         # logging.error(f"invalid JSON page : {i}")  #here if get a captcha page then html file will be loaded
    #         # logging.error(f"ERROR ON PAGE : {i} with status code {response.status_code()}")
    #         # logging.error(response.text)
    #         return
    response_ld_js=json.loads(response_ld.text)
    ip_user_slug=response_ld_js['total_rank'][index]['user_slug']
    variables= {
        'username' : ip_user_slug
    }

    payload = {
            "query": query,
            "variables": variables
        }
    time.sleep(1)
    response_us = session.post(graphql_url, json=payload,impersonate='chrome') #main line
    response_us_js=response_us.json()['data']
    qid=[
        str(response_ld_js['questions'][0]['question_id']),
        str(response_ld_js['questions'][1]['question_id']),
        str(response_ld_js['questions'][2]['question_id']),
        str(response_ld_js['questions'][3]['question_id']),
        ]
    return mapping.makeRow(response_ld_js,response_us_js,index,qid)



#testing
# print(getUserDetails(14,496))
    
    


