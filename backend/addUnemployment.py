import csv
import os
import requests

# url to http trigger
URL = 'http://127.0.0.1:9090/unemployment'

# file to open
FILENAME =os.getcwd() + "/backend/res/salm.csv"

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
            
            # assign 0 value to null fields
            if column == 'null':
                record[header[index].strip()] = 0
            else :
                record[header[index].strip()] = column
        
        # call restful api to index the document
        res = requests.post(URL + "/" + record['fid'],json=record)
        
        print(res.content)