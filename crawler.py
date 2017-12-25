#!/usr/bin/env python3
from time import gmtime, strftime, sleep
import requests
import calendar
import sys, os
import csv
import re
# savin downloaded file to the folder with .csv format
def writeCsv(csvLst, fileName, path="data/"):
    os.makedirs(path, exist_ok=True)
    with open (path+fileName, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(['交易日期','契約','到期月份','開盤價','最高價','最低價','收盤價','漲跌價','漲跌%','成交量','成交價','結算價','未沖銷契約數','最後最佳買價','最後最佳賣價','歷史最高價','歷史最低價','是否因訊息面暫停交易','交易時段','價差對單式委託成交量'])
        for index in range(1,len(csvLst)):
            csvFile.write(csvLst[index]+'\n')
    print ("finished",fileName)
def checkFormat(csvStr):
    # using to check if there 's any date info in the line
    txDataRegex = re.compile(r'\d{4}/(\d){1,2}/\d{1,2}')
    return txDataRegex.search(csvStr)
def checkSavedData():
    # using to check the last saved year of data from the data folder
    fileLst = list(os.walk('./data/'))
    # os.walk will return [(dirPath, dirNames, fileNames)]
    fileNames = [fileName for fileName in fileLst[0][2]]
    intFileNames = [int(intName[:4]) for intName in fileNames]
    return max(intFileNames)
def decodeToUtf8():
    # using to transform the origin response data to utf8
    pass
# the major function of the program,
# used to send POST and GET requests to
# http://www.taifex.com and get the trading logs back
def requestData(datestart, dateend):
    fileName = datestart[:4]+datestart[5:7]+'.csv'
    params = {
            "datestart"    : datestart,
            "dateend"      : dateend,
            "COMMODITY_ID" : "TX",
            "his_year"     : "2016"
            }
    r = requests.post("http://www.taifex.com.tw/chinese/3/3_1_2dl.asp", data=params)
    # after the POST request the page will redirect to another page
    # our file's addr. is stored in the middle header
    dictHeader = dict(r.history[0].headers)
    fileAddr = "http://www.taifex.com.tw"+dictHeader["Location"]
    csvStr = (requests.get(fileAddr)).text
    csvLst = csvStr.split('\r\n')
    # if the downloaded format isn't right then print the result and redo the process
    if checkFormat(csvStr)==None:
        print ("didn't download data",datestart[:7])
        print ("take 5s rest to send request again")
        sleep(5)
        requestData(datestart, dateend)
    else:
        writeCsv(csvLst, fileName)
# used to crawl the website with predefined times of loop
def crawler(startYear=1998):
    currentYear = int(strftime("%Y", gmtime()))
    monthes = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for year in range(startYear,currentYear+1):
        if year==1998:
            for month in monthes[6:]:
                lastDay = calendar.monthrange(year,int(month))[1]
                datestart = str(year)+"/"+month+"/"+"01"
                dateend   = str(year)+"/"+month+"/"+str(lastDay)
                requestData(datestart, dateend)
            continue
        for month in monthes:
            lastDay = calendar.monthrange(year,int(month))[1]
            datestart = str(year)+"/"+month+"/"+"01"
            dateend   = str(year)+"/"+month+"/"+str(lastDay)
            requestData(datestart, dateend)
# the entry point of the program
def main():
    if (len(sys.argv)<2):
        crawler()
    else:
        if sys.argv[1]=='--update':
            startYear = checkSavedData()
            crawler(startYear)
        elif checkFormate(sys.argv[1]!=None):
            # input parameter is year
            crawler(sys.argv[1])
    print ('Congradulation! Now you got all the TX datas!')
if __name__=="__main__":
    main()
