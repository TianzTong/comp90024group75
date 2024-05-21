import csv
import os
import requests

# URL to http trigger for fission
URL = 'http://127.0.0.1:9090/afford'

# file url to open
FILENAME =os.getcwd() + "/backend/res/sgs.csv"

id = 1

with open(FILENAME, 'r') as file:
    
    # read the csv file
    csvreader = csv.reader(file)
    
    # jump the first row as header
    header = next(csvreader)
    
    for row in csvreader:
        record = {}
        errorcode = -1
        for index, column in enumerate(row):
            
            if(column == 'null'):
                errorcode = 1
                #print("null value detected")
                break
            
            if index == 0:
                record["2019q3"] = column
            elif index == 3:
                record["2019q2"] = column
            elif index == 4:
                record["2019q1"] = column
            elif index == 5:
                record["2020q1"] = column
            elif index == 6:
                record["2019q4"] = column
            elif index == 7:
                record["2020q3"] = column
            elif index == 8:
                record["state"] = column
            elif index == 9:
                record["2020q2"] = column
            elif index == 10:
                record["2021q2"] = column
            elif index == 11:
                record["2020q4"] = column
            elif index == 12:
                record["2021q1"] = column
        if errorcode == 1:
            continue
        res = requests.post(URL + "/" + str(id),json=record)
        id += 1
        print(res.content)
        
                
            
            
    
        

        

