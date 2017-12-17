#!/usr/bin/env python3
from time import gmtime, strftime
import requests
import calendar
import sys, os
import csv
# savin downloaded file to the folder with .csv format
def writeCsv(csvLst, fileName, path="data/"):
    os.makedirs(path, exist_ok=True)
    with open (path+fileName, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(['交易日期','契約','到期月份','開盤價','最高價','最低價','收盤價','漲跌價','漲跌%','成交量','成交價','結算價','未沖銷契約數','最後最佳買價','最後最佳賣價','歷史最高價','歷史最低價','是否因訊息面暫停交易','交易時段','價差對單式委託成交量'])
        for index in range(1,len(csvLst)):
            csvFile.write(csvLst[index]+'\n')
    print ("finished",fileName)
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
    writeCsv(csvLst, fileName)
# used to crawl the website with predefined times of loop
def crawler():
    currentYear = int(strftime("%Y", gmtime()))
    monthes = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for year in range(1998,currentYear+1):
        if year==1998:
            for month in monthes[6:]:
                lastDay = calendar.monthrange(year,int(month))[1]
                datestart = str(year)+"/"+str(month)+"/"+"01"
                dateend   = str(year)+"/"+str(month)+"/"+str(lastDay)
                requestData(datestart, dateend)
            continue
        for month in monthes:
            lastDay = calendar.monthrange(year,int(month))[1]
            datestart = str(year)+"/"+month+"/"+"01"
            dateend   = str(year)+"/"+month+"/"+str(lastDay)
            requestData(datestart, dateend)
# the entry point of the program
def main():
    crawler()

if __name__=="__main__":
    main()
