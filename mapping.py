 #ld:dict , user:dict ,currU:int , qid : array
'''
function to make all the information of user in leaderboard into a list for CSV file genereation

'''
import json
def makeRow(ld,user,currU,qid):
    rank=-1
    d1=ld['total_rank'][currU]
    rank=d1['rank']
    userSlug=d1['user_slug']
    userName=d1['username']
    countryName=d1['country_name']  
    score=d1['score']
    finishTime=d1['finish_time']
    d1=ld['submissions'][currU] #fixed this bug
    arr=[None]*8
    problemSolved=0 #problem count in current
    for i in range(0,4):
        q_time=None
        q_fail_cnt=None
        try :
            q_time=d1[qid[i]]['date'] 
            q_fail_cnt=d1[qid[i]]['fail_count']
            if(d1[qid[i]]['status'] ==10):
                problemSolved+=1
        except :
            q_time=None
            q_fail_cnt=None

        arr[i]=q_time
        arr[4+i]=q_fail_cnt

    #6
    # print(problemSolved)

    #7,8,9,10,11,12,13,14
    # print(arr)

    currRow=[rank,userSlug,score,problemSolved,finishTime]
    for i in range(0,8):
        currRow.append(arr[i])

    currRow.append(userName)
    currRow.append(countryName)
    arr2=[None]*15

    #now data from pg file
    d1=user['matchedUser']['profile']
    currRow.append(d1['ranking']) #profile ranking ranking P
    currRow.append(d1['postViewCount'])
    currRow.append(d1['reputation'])

    #problem counts
    d1=user['matchedUser']['submitStats']['acSubmissionNum']
    for i in range(0,4):
        currRow.append(d1[i]['count'])
        currRow.append(d1[i]['submissions'])

    #now contestRankingInfo

    #check can be null or not
    d1=user['userContestRanking'] #if someone participated in contest then He will have this column
    currRow.append(d1['attendedContestsCount'])
    currRow.append(d1['rating'])
    currRow.append(d1['globalRanking'])
    currRow.append(d1['topPercentage'])

    d1=user['userContestRankingHistory']
    userHistory=json.dumps(d1)
    currRow.append(userHistory)
    return currRow