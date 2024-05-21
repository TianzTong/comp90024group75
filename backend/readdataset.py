import csv
import os

URL = 'https://127.0.0.1:9090/affords'
FILENAME =os.getcwd() + "/backend/res/sgs.csv"
rows = []
with open(FILENAME, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        record = {}
        for index, column in enumerate(row):
            if(column == 'null'):
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
                
        print(record)
                
            
            
        rows.append(row)
        

        

