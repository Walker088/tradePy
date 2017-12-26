# tradePy

## Introduction
## Usage
For now the project only support the crawler to fetch the daily transaction tick data from [TAIWAN FUTURES EXCHANGE](http://www.taifex.com.tw/chinese/3/3_1_2.asp).
#### 1. Crawler.py
Crawler.py is used to download all the transaction datas from [TAIWAN FUTURES EXCHANGE](http://www.taifex.com.tw/chinese/3/3_1_2.asp). if you wanna download all the datas from the date of 1998/7/22, which is the first open day of the market, you can simply enter the command below into any shell or command line tools you're family with.

	chmod +x crawler.py
	./crawler.py

If you were download the whole program from this site by the command like:

	git clone https://github.com/Walker088/tradePy.git

Then probably you there're some data exist in the **/data/** folder that you don't need to resend all the requests. The command below would be recommand:

	chmod +x crawler.py
	./crawler.py --update

If you don't want to download all the datas but only datas of specific year:

	./crawler.py 2017
	# ./crawler.py [year]

## Future Works
I will trying to implement some strategy or algorithm to the data l've collect and share to you guys here later, just tell me with the issue function if there's any problem with the project.
