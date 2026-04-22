'''
file to genearate clean csv data of a contest
from its messy leaderboard and user data
from API calls
'''

import csv
import json
import os
import logging
import config
import dataset_extraction.fetch.util.mapping as mp


# CONTEST='496' #variable
USER_ON_SINGLE_PAGE=25
def generateCSV(contest):
    folderPath= config.ROOT_DIR /"dataset"/f'contest_{contest}'
    logging.basicConfig(filename= folderPath/f'{contest}_jsToCsvLog.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG,force=True)
    logging.info(f'STARTING PROCESS FOR JSON DATA TO CSV conversion for contest - {contest}')
    ldPath=folderPath/'leaderboard'

    #initialisation of csv file and its writer object
    output_csv=open(folderPath/f'weekly_contest{contest}.csv','w',encoding='utf-8') #reason of encoding in ch10 automation book
    writer=csv.writer(output_csv)

    #header row total 31 features
    writer.writerow([
        'Rank',
        'User_slug',
        'Score',
        'CurrConSolved',
        'FinishTimeStamp',
        'Q1TimeStamp',
        'Q2TimeStamp',
        'Q3TimeStamp',
        'Q4TimeStamp',
        'Q1FailCnt',
        'Q2FailCnt',
        'Q3FailCnt',
        'Q4FailCnt',
        'UserName',
        'CountryName',
        'RankingP',
        'PostViewCnt',
        'Reputation',
        'TotalQsAcc',
        'TotalQsSub',
        'EasyQsAcc',
        'EasyQsSub',
        'MedQsAcc',
        'MedQsSub',
        'HardQsAcc',
        'HardQsSub',
        'ContestCnt',
        'CurrRating',
        'GlobalRank',
        'topPercentage',
        'ContestHistory'
        ]
    )

    cn_count=0 #chinese user count --> will give us error
    o_count=0 # other type of unknowsn errors+special character user slug --> will give us error
    total_count=0 #how many users we process both correct or error
    for f in os.listdir(ldPath): # f is just string name of file
        if(f.endswith('.json')) :
            name=f
            number=name[12:-5] #string type 
            #depends on file name instead of page number from 0 to 400
            #as long as any leaderboard file & corresponding pg file is present fully with all 25 users, code will not break
            print(f'curr ld file {f} | file number {number}')
            pg_path=folderPath/'user'/f'pg_{number}'
            currLdPath=ldPath/f
            ld_file=open(currLdPath,'r')
            ld=json.load(ld_file)
            #now processing by number
            for curr in range(0,USER_ON_SINGLE_PAGE):
                total_count+=1
                try :
                    user_path=pg_path/f'{curr}.json' #can give error if user is missing
                    user_file=open(user_path,'r')
                    user=json.load(user_file)['data']
                    qid=[
                        str(ld['questions'][0]['question_id']),
                        str(ld['questions'][1]['question_id']),
                        str(ld['questions'][2]['question_id']),
                        str(ld['questions'][3]['question_id']),
                    ]
                    currRow=mp.makeRow(ld,user,curr,qid)
                    writer.writerow(currRow)
                except TypeError:
                    cn_count+=1
                    logging.error(f"error at pg {number}  with user {curr} -->  MP CHINESE USER")
                except Exception as e:
                    o_count+=1
                    logging.error(f"error at pg {number}  with user {curr}") #like username in special chars
                    logging.error(e)



    output_csv.close()   
    logging.debug(f'total users processed  = {total_count}')
    logging.debug(f'total number of china users = {cn_count}')
    logging.debug(f'total number of unknows errors = {o_count}')
    logging.debug(f'total number of erros combined = {cn_count+o_count}')

    logging.info(f"successful in contest {contest} csv file generation with error % = {round(((cn_count+o_count)/total_count)*100)} %")

if __name__ == "__main__":
    contest=496
    generateCSV(contest)

            
            



        