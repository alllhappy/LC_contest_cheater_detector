#script for time caluclation

USERS_PER_CONTEST=10000

def  showTime(ts,rts): #delay time in sec or total Time for 1 query in sec  , per user
    #ts -> fetch time, rts -> random delay time upper bounds
    total_time=USERS_PER_CONTEST*(ts+rts) #in seconds
    total_time_hr=total_time/3600
    total_time_day=total_time_hr/24
    print(f"total time in hours {total_time_hr} || in days {total_time_day} ")







print(f"each user query time delay= fetch time + my random delay")

while(True):
    query_time=int(input("time for 1 query server side: "))
    random_time=int(input("time upper bound on random : "))
    showTime(query_time,random_time)