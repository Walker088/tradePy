#!/usr/bin/env python3
from time import gmtime, strftime, sleep
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests, zipfile, io
import calendar
import sys, os
import csv
import re
import progressbar
import argparse

# savin downloaded file to the folder with .csv format
def writeCsv(csvLst, fileName, path="data/unassigned/"):
    os.makedirs(path, exist_ok=True)
    with open (path+fileName, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        for index in range(len(csvLst)):
            csvFile.write(csvLst[index]+'\n')

def checkFormat(csvStr):
    # using to check if there's any date info in the line
    txDataRegex = re.compile(r'\d{4}/(\d){1,2}/\d{1,2}')
    return txDataRegex.search(csvStr)

def checkSavedData():
    # using to check the last saved year of data from the data folder
    fileLst = list(os.walk('./data/'))
    # os.walk will return [(dirPath, dirNames, fileNames)]
    fileNames = [fileName for fileName in fileLst[0][2]]
    intFileNames = [int(intName[:4]) for intName in fileNames]
    return max(intFileNames)

# the major function of the program,
# used to send POST and GET requests to
# http://www.taifex.com and get the trading logs back
def requestData(datestart, dateend, folder="data/dkData/"):
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
    res = requests.get(fileAddr)
    res.encoding = "big5"
    csvStr = (res).text
    csvLst = csvStr.split('\r\n')
    # if the downloaded format isn't right then print the result and redo the process
    if checkFormat(csvStr)==None:
        sleep(5)
        requestData(datestart, dateend)
    else:
        writeCsv(csvLst, fileName, folder)

# used to crawl the website with predefined times of loop
def getdkData(amtFlag,startYear=1998):
    currentYear = int(strftime("%Y", gmtime()))
    monthes = ['01','02','03','04','05','06','07','08','09','10','11','12']
    bar = progressbar.ProgressBar(maxval=currentYear+2-startYear, \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
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
        bar.update(year-startYear+1)
        sleep(0.1)
    bar.finish() 

def getAvaDates(baseUrl="https://www.taifex.com.tw/chinese/3/dl_3_1_3.asp"):
    res = requests.get(baseUrl)
    res.encoding = "utf-8"
    dateRegex = re.compile(r'^(\d+/\d+/\d+)$')

    bsObj = bs(res.text, "html.parser")
    dateLst = [ date.text.strip() for date in bsObj.findAll("table", {"class":"table_c"})[1] \
                                                   .findAll("td") if dateRegex.search(date.text.strip()) != None ]
    return [date.replace("/", "_") for date in dateLst]

def getTickData(amtFlag):
    baseUrl = "https://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/Daily_"
    avaDates = getAvaDates()
    bar = progressbar.ProgressBar(maxval=len(avaDates), \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for d in range(len(avaDates)):
        fileName, folder = avaDates[d]+".csv", "./data/tickData/"
        res = requests.get(baseUrl+avaDates[d]+".zip")
        z = zipfile.ZipFile(io.BytesIO(res.content))
        z.extractall("./data/rawTickData/")
        bar.update(d+1)
        sleep(0.1)
    bar.finish()

def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dkData", help="Day K-line data, all: download all the data; update: downloal new data", type=str)
    parser.add_argument("--tickData", help="Tick data, all: download all the data; update: downloal new data", type=str)
    return parser.parse_args()

# the entry point of the program
def main():
    args = initArgs()
    if (args.dkData):
        getdkData(args.dkData)
    elif (args.tickData):
        getTickData(args.dkData)
    else:
        print("plz try ./txCrawler.py --dkData or ./txCrawler.py --tickData")
    print ('Congradulation! Now you got all the TX datas!')

if __name__=="__main__":
    main()
