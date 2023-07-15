# 連線資料庫，選取想要的資料呈現

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


# 資料更新
def get_last_update_date(engine):
    twse_price_df = pd.read_sql(f"select * from twse_price LIMIT 1", engine)
    twes_price_last_update_date = twse_price_df.at[0,"交易日期"]

    otc_price_df = pd.read_sql(f"select * from otc_price LIMIT 1", engine)
    otc_price_last_update_date = otc_price_df.at[0,"交易日期"]

    twse_corporation_df = pd.read_sql(f"select * from twse_corporation_net_buy_sell LIMIT 1", engine)
    twes_corporation_last_update_date = twse_corporation_df.at[0,"交易日期"]

    otc_corporation_df = pd.read_sql(f"select * from otc_corporation_net_buy_sell LIMIT 1", engine)
    otc_corporation_last_update_date = otc_corporation_df.at[0,"交易日期"]

    twse_index_df = pd.read_sql(f"select * from twse_index LIMIT 1", engine)
    twes_index_last_update_date = twse_index_df.at[0,"交易日期"]

    otc_index_df = pd.read_sql(f"select * from otc_index LIMIT 1", engine)
    otc_index_last_update_date = otc_index_df.at[0,"交易日期"]

    future_twse_index_df = pd.read_sql(f"select * from future_twse_index LIMIT 1", engine)
    future_twes_index_last_update_date = future_twse_index_df.at[0,"交易日期"]

    return [twes_price_last_update_date,otc_price_last_update_date,twes_corporation_last_update_date,otc_corporation_last_update_date,twes_index_last_update_date,otc_index_last_update_date,future_twes_index_last_update_date]

# 上市櫃公司資料呈現
def show_price_data(id,engine):
    if id.isdigit() == True:
        df = pd.read_sql(f"select * from twse_price WHERE `證券代號` = {id}", engine) # ,index_col=['交易日期'], parse_dates=['交易日期']
        
        is_empty = df.empty
        if is_empty == True:
            df = pd.read_sql(f"select * from otc_price WHERE `證券代號` = {id}", engine)

        df['交易日期'] = pd.to_datetime(df['交易日期'])
        df['交易日期'] = df['交易日期'].dt.date
        
        sid = id
        sname = df.at[1,"證券名稱"]
        stype = df.at[1,"市場類別"]

    else:
        df = pd.read_sql(f"select * from twse_price WHERE `證券名稱` = '{id}'", engine)
        is_empty = df.empty
        if is_empty == True:
            df = pd.read_sql(f"select * from otc_price WHERE `證券名稱` = '{id}'", engine)

        df['交易日期'] = pd.to_datetime(df['交易日期'])
        df['交易日期'] = df['交易日期'].dt.date
        
        sid = df.at[1,"證券代號"]
        sname = id
        stype = df.at[1,"市場類別"]
            
    if stype == "上市":
        df.drop(df.columns[[1,2,3,5,6,13,14,15,16]], axis=1, inplace=True)
    else:
        df.drop(df.columns[[1,2,3,11,12,13,14,15,16,17,18,19]], axis=1, inplace=True)
    
    last_date = df.at[0,"交易日期"]
    last_open = df.at[0,"開盤價"]
    last_high = df.at[0,"最高價"]
    last_low = df.at[0,"最低價"]
    last_close = df.at[0,"收盤價"]
    last_amount = df.at[0,"成交股數"]
    last_amount = int(last_amount / 1000)

    index_df = df.set_index('交易日期', inplace = False)

    last_text = f"最後交易日：{last_date}\n\n開盤價：{last_open}  |  最高價：{last_high}  |  最低價：{last_low}  |  收盤價：{last_close}\n\n成交量(張數)：{last_amount}"
    stock_text = f"證券代號：{sid}  |  證券名稱：{sname}  |  市場類別：{stype}"

    return [df,stock_text,last_text,stype,index_df]


# 大盤指數呈現
def show_index(market,engine):
    df = pd.read_sql(f"select * from {market}", engine)
    if market == "twse_index":
        index_type = "加權指數"
    elif market == "otc_index":
        index_type = "櫃買指數"
    else:
        index_type = "台指近月"

    last_date = df.at[0,"交易日期"]
    last_open = df.at[0,"開盤價"]
    last_high = df.at[0,"最高價"]
    last_low = df.at[0,"最低價"]
    last_close = df.at[0,"收盤價"]
    try:
        last_amount = df.at[0,"成交量(億元)"]
        last_item = "成交量(億元)"
    except:
        last_amount = df.at[0,"振幅"]
        last_item = "振幅"
    
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df['交易日期'] = df['交易日期'].dt.date

    index_df = df.set_index('交易日期', inplace = False)

    last_text = f"最後交易日：{last_date}\n\n開盤價：{last_open}  |  最高價：{last_high}  |  最低價：{last_low}  |  收盤價：{last_close}\n\n{last_item}：{last_amount}"
    index_text = f"大盤指數：{index_type}"

    return [df,index_text,last_text,index_df]

# 個股三大法人資料呈現
def show_corporation(id,engine):
    if id.isdigit() == True:
        df = pd.read_sql(f"select * from twse_corporation_net_buy_sell WHERE `證券代號` = {id}", engine) # ,index_col=['交易日期'], parse_dates=['交易日期']
        
        is_empty = df.empty
        if is_empty == True:
            df = pd.read_sql(f"select * from otc_corporation_net_buy_sell WHERE `證券代號` = {id}", engine)
            # 刪掉otc資料的某些欄位
            df.drop(df.columns[[1,2,3,4,5,7,8,10,11,13,14,16,17]], axis=1, inplace=True)
        else:
            # 刪掉twse資料的某些欄位
            df.drop(df.columns[[1,2,3,4,5,7,8,10,11,14,15,16,17]], axis=1, inplace=True)
    else:
        df = pd.read_sql(f"select * from twse_corporation_net_buy_sell WHERE `證券名稱` = '{id}'", engine)
        is_empty = df.empty
        if is_empty == True:
            df = pd.read_sql(f"select * from otc_corporation_net_buy_sell WHERE `證券名稱` = '{id}'", engine)
            # 刪掉otc資料的某些欄位
            df.drop(df.columns[[1,2,3,4,5,7,8,10,11,13,14,16,17]], axis=1, inplace=True)
        else:
            # 刪掉twse資料的某些欄位
            df.drop(df.columns[[1,2,3,4,5,7,8,10,11,14,15,16,17]], axis=1, inplace=True)

    
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df['交易日期'] = df['交易日期'].dt.date

    index_df = df.set_index('交易日期', inplace = False)
    
    return [df,index_df]

def show_market_index_corporation(market,engine):
    df = pd.read_sql(f"select * from {market}", engine) # ,index_col=['交易日期'], parse_dates=['交易日期']
    df.drop(df.columns[[1,2,3,4,5,6,7,8,9,10]], axis=1, inplace=True)

    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df['交易日期'] = df['交易日期'].dt.date

    index_df = df.set_index('交易日期', inplace = False)

    return [df,index_df]    