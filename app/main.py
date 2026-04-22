#main app for interaction
'''
command to run from project root : python -m app.main
'''
import app.fetch.fetch as ft
import logging
from model.model_v1 import helpers
import config
import app.display.display as disp

def rule_low_active(df): #Near-zero active time with high score
    return (df['active_days'] < 50) & (df['Score'] >= 10)

def rule_new_account_top_rank(df): #new user high rank
    return (df["ContestCnt"] <= 5) & (df["Rank"] < 200)

def rule_perfect_solve(df):
    return (df['total_fail'] == 0) & (df['Score'] >= 15) & (df['ContestCnt'] <= 5)

def rule_weak_profile(df): #Weak profile but top contest rank
    return (df['Total_solved'] < 200) & (df['Rank'] < 200)

def rule_low_solved_high_rating(df): #Low solved count but high rating
    return (df['Total_solved'] < 100) & (df['CurrRating'] > 1900)

def rule_zero_rating_jump(df):
    return (df['rating_jump'] == 0) & (df['CurrRating'] > 1500)

def rule_ghost_profile(df):
    return (df['Total_solved'] < 50) & (df['Rank'] < 5000) 

from model.model_v1 import test
app_folder_path= config.ROOT_DIR/'app'
output=open(app_folder_path/'output.txt','a',encoding='UTF-8')
logging.basicConfig(filename=app_folder_path/'error_log.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG,force=True)


def findCheatersInRange(CONTEST,START_RANK,END_RANK):
    total=0
    errors=0
    for i in range(START_RANK,END_RANK+1):
        try:
            data=ft.getUserDetails(i,CONTEST)
            # print(data)
            ipToModel=helpers.extract_features(data)
            # print(ipToModel)
            response=test.predict_user(ipToModel)
            # print(response)
            if(response['label']!='CLEAN'):
                total+=1
                print(f"Rank : {i} , username : {data[1]} , output = {response['label']}")
                output.write(f"Rank : {i} , username : {data[1]} , output = {response['label']} \n")
        except Exception as e:
            #most errors are due to chinese users
            errors+=1
            logging.error(f'error in rank {i}')
            logging.error(e)

    print(f"total cheaters are :{total}")
    print(f"total candiadates having error : {errors}")
    output.write(f"total cheaters are :{total} \n")
    output.write(f"total candiadates having error : {errors}")
    output.write('\n')
    

if __name__ == '__main__':
    disp.printWelcome()
    contest=int(input('enter contest number : '))
    start_rank=int(input('enter Start Rank : '))
    end_rank=int(input('enter End Rank : '))

    output.write('\n')    
    output.write(f'Finding cheaters in {contest} in between {start_rank} to {end_rank} ranks \n')
    findCheatersInRange(contest,start_rank,end_rank)
    output.close()
    disp.printExit()