# generates contest info for a particular contest in a csv file
'''
output contains -> ContestName, startTimeStamp,TotalAttendees, Q1credit , Q2 credit, Q3 Credit, Q4 credit

'''

import json
import csv

CONTEST=494

ld1Path=f'contest_{CONTEST}/leaderboard/leaderboard_1.json' #this file should be present
input=open(ld1Path,'r')

contest_info=json.load(input)
output_csv=open(f'dataset/weekly_contest{CONTEST}_info.csv','w',encoding='utf-8')
writer=csv.writer(output_csv)

writer.writerow([
'ContetName',
'StartTimeStamp',
'TotalParticipants'
'Q1Credit',
'Q2Credit',
'Q3Credit',
'Q4Credit',
]
)

cName=f'contest{CONTEST}'
startTime=contest_info['time']
total_participants=contest_info['user_num']
q1_credit=contest_info['questions'][0]['credit']
q2_credit=contest_info['questions'][1]['credit']
q3_credit=contest_info['questions'][2]['credit']
q4_credit=contest_info['questions'][3]['credit']

writer.writerow([cName,startTime,total_participants,q1_credit,q2_credit,q3_credit,q4_credit])
output_csv.close()

