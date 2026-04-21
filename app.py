#main app for interaction

import fetch
import joblib
import logging
from pre_final_hybrid import helpers
import pandas as pd

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
'''
if __name__ == "__main__":
    from pre_final_hybrid import test
    while(True):
        input_rk=int(input("enter input rank : "))
        input_cn=int(input("enter input contest : "))

        if(input_rk == -1) :
            break
        data=fetch.getUserDetails(input_rk,input_cn)
        ipToModel=helpers.extract_features(data)
        print(ipToModel)

        response=test.predict_user(ipToModel)
        print(response['label'])

        # pass data to model 
        #prediction = model(data)
        #print( prediction)

'''

from pre_final_hybrid import test
logging.basicConfig(filename=f'classify_497.txt',format=' %(asctime)s -  %(levelname)s -  %(message)s',level=logging.DEBUG)
total=0
errors=0

START_RANK=1
END_RANK=2
CONTEST=498
for i in range(START_RANK,END_RANK+1):
    try:
        data=fetch.getUserDetails(i,CONTEST)
        # print(data)
        ipToModel=helpers.extract_features(data)
        # print(ipToModel)
        response=test.predict_user(ipToModel)
        # print(response)
        if(response['label']!='CLEAN'):
            total+=1
            print(f"Rank : {i} , username : {data[1]} , output = {response['label']}")
    except Exception as e:
        #most errors are due to chinese users
        errors+=1
        logging.error(f'error in rank {i}')
        logging.error(e)

print(f"total cheaters are :{total}")
print(f"total candiadates having error : {errors}")