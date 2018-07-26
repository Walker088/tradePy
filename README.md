# tradePy

## Introduction
## Usage
For now the project only support the crawler to fetch the daily transaction tick data from [TAIWAN FUTURES EXCHANGE](http://www.taifex.com.tw/chinese/3/3_1_2.asp).
### txCrawler.py
txCrawler.py is used to download the transaction datas from [TAIWAN FUTURES EXCHANGE](http://www.taifex.com.tw/).
You can simply checkout the usage by *-h* flag:

	chmod +x txCrawler.py
	./txCrawler.py -h

**The program has two parameters:**

#### 1. Daily K-Line dada
You can download all the datas from the date of 1998/7/22 by "--dkData" parameter.

	./txCrawler.py --dkData all

#### 2. Tick data
You can download the recent 30 days of tick data by "--tickData" parameter.

	./txCrawler.py --tickData all

## Future Works
I will trying to implement some strategy or algorithm to the data l've collect and share to you guys here later, just tell me with the issue function if there's any problem with the project.
