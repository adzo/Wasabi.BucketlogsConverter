from turtle import title
import pandas as pd
import os
lines=[]
linesnew=[]
# directory = os.getcwd()
# filename = input()
# filelocation = directory+'/'+filename
with open(r"/Users/gowtham/Desktop/testing/logs",'r') as fp:
    lines =fp.readlines()

with open(r"/Users/gowtham/Desktop/testing/logs",'w') as fp:
    for number,line in enumerate(lines):
        if number not in [0,1]:
            fp.write(line)
current_list = list()
with open(r"/Users/gowtham/Desktop/testing/logs_new",'w') as fp:
    fp.write("BucketOwner Bucket Time RemoteIP Requester RequestId Operation Key Request-URI HttpStatus ErrorCode BytesSent ObjectSize TotalTime Turn-AroundTime Referrer User-Agent VersionId \n")
    for number,line in enumerate(lines):
        if(number == 0 or number == 1):
            continue
        li = list()
        # splitting lines with "" and making its a  single string
        line=line.split('"')
        first_text = line[0]
        # first index split
        first_text = first_text.split(' ')
        first_text[2] = first_text[2]+' '+first_text[3]
        del first_text[3]
        del first_text[-1]
        for val in first_text:
            li.append(val)
        second_text = line[1]
        li.append(second_text)
        middle_values = line[-5]
        middle_values = middle_values.split(' ')
        del middle_values[0]
        for val in middle_values:
            li.append(val)
        last_text = line[-2]
        li.append(last_text)
        li.append(line[-1])
        current_list.append(li)
titles = 'BucketOwner Bucket Time RemoteIP Requester RequestId Operation Key Request-URI HttpStatus ErrorCode BytesSent ObjectSize TotalTime Turn-AroundTime Referrer User-Agent VersionId'
titles = titles.split(' ')
data = pd.DataFrame(current_list, columns = titles)
data.to_csv(r"/Users/gowtham/Desktop/testing/logs_csv.csv")
os.remove ("/Users/gowtham/Desktop/testing/logs")
os.remove ("/Users/gowtham/Desktop/testing/logs_new")
