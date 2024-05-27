import csv
import os
import requests

# url to http trigger
URL = 'http://127.0.0.1:9090/asx'

# file to open
FILENAME =os.getcwd() + "/backend/res/asx.csv"

with open(FILENAME, 'r') as file:
    
    # read the csv file
    csvreader = csv.reader(file)
    
    # jump the first row as header
    header = next(csvreader)
    for row in csvreader:
        
        record = {}
        errorcode = -1
        # iterate each columns and create a dictionary with it
        for index, column in enumerate(row):
            
            # skip null records
            if column == 'null':
                errorcode = 1
                continue
            else :
                field = header[index].strip()
                
                # delete the comma for float numbers
                if field in ["Price", "Low", "High"]:
                    record[field] = float(column.replace(",", ""))
                
                # reset the date format
                elif field == '\ufeff"Date"':
                    curDate = column.split("/")
                    if len(curDate) != 3:
                        print("Date error!")
                        errorcode = 2
                        continue
                    record["Date"] = curDate[2] + "-" + curDate[1] + "-" + curDate[0]
                    
                # skip the open and vol column
                elif field in ["Open","Vol."]:
                    continue
                
                else:
                    record[header[index].strip()] = column
                
        # call restful api to index the document
        if errorcode == -1:
            res = requests.post(URL + "/" + record["Date"],json=record)
            
        print(res.content)