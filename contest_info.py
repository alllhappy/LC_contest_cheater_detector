# generates contest info for a particular contest in a csv file
'''
output contains -> ContestName, startTimeStamp,TotalAttendees, Q1credit , Q2 credit, Q3 Credit, Q4 credit
using directly api to retrieve this data. eliminated dependency of leaderboard files

'''

import json
import csv
import pandas as pd
from curl_cffi import requests
import json



CONTEST=496
def getContestInfo(contest):
    output_csv=open(f'dataset/weekly_contest{CONTEST}_info.csv','w',encoding='utf-8')
    contest_info_url=f'https://leetcode.com/contest/api/info/weekly-contest-{contest}/'
    writer=csv.writer(output_csv)

    writer.writerow([
        'Contest_slug',
        'StartTimeStamp',
        'Q1Credit',
        'Q2Credit',
        'Q3Credit',
        'Q4Credit',
    ]
    )

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
    try:
        response=session.get(contest_info_url,impersonate='chrome')
        # print(response.text)
        data=response.json()
        cName=data['contest']['title_slug']
        startTime=data['contest']['start_time']
        q1_credit=data['questions'][0]['credit']
        q2_credit=data['questions'][1]['credit']
        q3_credit=data['questions'][2]['credit']
        q4_credit=data['questions'][3]['credit']
        writer.writerow([str(cName),int(startTime),q1_credit,q2_credit,q3_credit,q4_credit])
    except:
        print("error could not retrieve contest info data")

    output_csv.close()

getContestInfo(CONTEST)

