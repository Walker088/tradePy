#!/usr/bin/env python3
import pandas as pd
import numpy as np
import logging, logging.config
import TxStrategys as ts
import argparse

logging.config.fileConfig('./config/backtest.conf')
log = logging.getLogger("root")

def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

def make_int(text):
    return int(text.strip('" '))

def make_float(text):
    return float((text.strip('" ')))

def readTxData():
    txdf = pd.read_csv('./data/rawTickData/Daily_2018_06_14.csv',
                       encoding='big5', sep=r',', low_memory=False,
                       converters = {
                           '成交日期' : make_int,
                           '商品代號' : strip,
                           '到期月份(週別)' : strip,
                           '成交時間' : make_int,
                           '成交價格' : make_float,
                           '成交數量(B+S)' : make_int,
                           '近月價格' : strip,
                           '遠月價格' : strip,
                           '開盤集合競價 ' : strip 
                       })
    txdf = txdf.astype({
                        '成交日期' : int,
                        '商品代號' : str,
                        '到期月份(週別)' : str,
                        '成交時間' : int,
                        '成交價格' : float,
                        '成交數量(B+S)' : int,
                        '近月價格' : str,
                        '遠月價格' : str,
                        '開盤集合競價 ' : str 
                    })
    txdf = txdf[txdf['商品代號']=='TX']
    txdf = txdf[txdf['成交時間'] >= 84500]
    txdf = txdf[txdf['成交時間'] <= 134500]
    log.info(txdf.columns)
    log.info(txdf.head(5))

def main():
    readTxData()

if __name__=="__main__":
    main()
