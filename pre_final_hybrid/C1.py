import pandas as pd
import json

# Load dataset
df = pd.read_csv("training_data_final.csv")


# Time Taken (seconds)


# values to subtract for each contestid
subtract_map = {
    1: 1774146600,
    2: 1774751400,
    3: 1775356200
}

# subtract numeric values based on contestid
df["time_taken"] = df["FinishTimeStamp"] - df["contest_id"].map(subtract_map)


# Total Fail Count


fail_cols = ["Q1FailCnt", "Q2FailCnt", "Q3FailCnt", "Q4FailCnt"]

df[fail_cols] = df[fail_cols].fillna(0)

df["total_fail"] = df[fail_cols].sum(axis=1).astype(int)


# Rating after first contest


def first_rating(history):

    try:
        history = json.loads(history)
        return history[0]["rating"]
    except:
        return None

df["rating_first"] = df["ContestHistory"].apply(first_rating)


# Total Active Days


import json
import pandas as pd

def active_days(history):

    try:
        if pd.isna(history):
            return 0

        # convert string to list
        history = json.loads(history)

        if len(history) == 0:
            return 0

        # sort by contest start time
        history = sorted(
            history,
            key=lambda x: x["contest"]["startTime"]
        )

        first = history[0]["contest"]["startTime"]
        last = history[-1]["contest"]["startTime"]

        duration = last - first

        # convert seconds to days
        return duration / (60*60*24)

    except Exception as e:
        return 0

df["active_days"] = df["ContestHistory"].apply(active_days)


# Final Feature Selection

df = df.rename(columns={
    "User_slug": "Username",
    "CountryName": "Country",
    "RankingP": "Profile_rank",
    "TotalQsAcc": "Total_solved",
    "EasyQsAcc": "Easy",
    "MedQsAcc": "Medium",
    "HardQsAcc": "Hard",
    "CurrRating": "CurrRating"
})

df = df.drop(columns=[
    "ContestHistory",
    "Q1TimeStamp",
    "Q2TimeStamp",
    "Q3TimeStamp",
    "Q4TimeStamp",
    "Q1FailCnt",
    "Q2FailCnt",
    "Q3FailCnt",
    "Q4FailCnt"
], errors="ignore")
# round numeric columns
numeric_cols = df.select_dtypes(include=["float64", "float32"]).columns

for col in numeric_cols:
    df[col] = df[col].round().astype("Int64")

features = df[[
    "Rank",
    "Username",
    "Score",
    "CurrConSolved",
    "time_taken",
    "total_fail",
    "Country",
    "Profile_rank",
    "PostViewCnt",
    "Reputation",
    "Total_solved",
    "Easy",
    "Medium",
    "Hard",
    "ContestCnt",
    "CurrRating",
    "rating_first",
    "GlobalRank",
    "active_days",
    "contest_id"
]]
# Save dataset
features.to_csv("training_data.csv", index=False)

print("Dataset Ready")