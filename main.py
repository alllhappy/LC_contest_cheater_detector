import requests
import pandas as pd

contest = "weekly-contest-495"

rows = []

for page in range(1,5):   # first 4 pages

    url = f"https://leetcode.com/contest/api/ranking/{contest}/?pagination={page}&region=global_v2"
    
    response = requests.get(url)
    # data = response.json()
    print(response.text)
    
    # users = data['total_rank']
    # print(users)

#     for user in users:
#         rows.append({
#             "username": user['username'],
#             "rank": user['rank'],
#             "score": user['score'],
#             "finish_time": user['finish_time']
#         })

# df = pd.DataFrame(rows)

# print(df.head())