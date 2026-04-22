

from datetime import datetime
from zoneinfo import ZoneInfo
import json

#function to calculate start time
def convert_to_8am_same_day(timestamp):
    ist = ZoneInfo("Asia/Kolkata")
    
    # convert timestamp to IST
    dt = datetime.fromtimestamp(timestamp, ist)
    
    # set time to 8:00 AM same day
    dt_8am = dt.replace(hour=8, minute=0, second=0, microsecond=0)
    
    # return unix timestamp
    return int(dt_8am.timestamp())



def extract_features(row):
    if(row[30]!='[]'):
        history = json.loads(row[30])
        history = sorted(history, key=lambda x: x["contest"]["startTime"])

        first_time = history[0]["contest"]["startTime"]
        last_time  = history[-1]["contest"]["startTime"]
    else:
        first_time=0
        last_time=0
        history=None

    start_time = convert_to_8am_same_day(row[5])

    new_user = {
        "Rank": row[0],
        "Username": row[1],
        "Score": row[2],
        "CurrConSolved": row[3],
        "time_taken": row[4] - start_time,
        "total_fail": (row[9] or 0) + (row[10] or 0) + (row[11] or 0) + (row[12] or 0),
        "Country": row[14],
        "Profile_rank": row[15],
        "PostViewCnt": row[16],
        "Reputation": row[17],
        "Total_solved": row[18],
        "Easy": row[20],
        "Medium": row[22],
        "Hard": row[24],
        "ContestCnt": row[26],
        "CurrRating": row[27],
        "rating_first": history[0]["rating"] if history is not None else 0,
        "GlobalRank": row[28],
        "active_days": (last_time - first_time) // 86400
    }

    return new_user
