#main app for interaction

import fetch




while(True):
    input_rk=int(input("enter input rank : "))
    input_cn=int(input("enter input contest : "))

    data=fetch.getUserDetails(input_rk,input_cn)
    # fetch.showUserDetails(data)

    # pass data to model 
    #prediction = model(data)
    #print( prediction)

    