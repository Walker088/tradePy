#!/usr/bin/env python3

import requests
from pprint import pprint

params = {"datestart":"2017/9/01", 
          "dateend":"2017/9/30", 
          "COMMODITY_ID":"TX", 
          "his_year":"2016"}
r = requests.post("http://www.taifex.com.tw/chinese/3/3_1_2dl.asp", data=params) 
#print (r.history)
tmpDict = dict(r.history[0].headers)

#for resp in r.history:
#    print (resp.status_code,resp.headers)


fileAddr = "http://www.taifex.com.tw"+tmpDict["Location"]
g = requests.get(fileAddr)

pprint (tmpDict)
pprint (type(g.text))
with open("test.csv","w") as c:
    c.write(g.text)
