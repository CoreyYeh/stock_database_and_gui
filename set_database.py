# 建立資料庫，主程式

# 爬蟲套件
import requests as req
import pandas as pd
from io import StringIO
from fake_useragent import UserAgent
ua = UserAgent(use_external_data=True)
from time import sleep
from bs4 import BeautifulSoup as bs

# MySQL套件
import pymysql
from sqlalchemy import create_engine

# 使用封包
import stock_data_crawler.main_crawler as craw

# 其他
import threading
import multiprocessing as mp
import random

if __name__=='__main__':
    # 總共有四個爬蟲程式要跑
    num_process = 4
    function_list = [craw.twse_price_crawler,craw.otc_price_crawler,craw.twse_corporation_crawler,craw.otc_corporation_crawler]
    process_list = []

    # 透過 multiprocessing 執行
    for i in range(num_process):
        process_list.append(mp.Process(target = function_list[i], args = ('2020-03-23','2023-06-20',)))
        process_list[i].start()

    # 關閉
    for i in range(num_process):
        process_list[i].join()
    
    print("finish all")