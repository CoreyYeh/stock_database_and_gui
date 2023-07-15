# 建立資料庫
# 爬證交所歷史股價、櫃買歷史股價、證交所歷史三大法人、櫃買歷史三大法人、goodinfo大盤、goodinfo櫃買

# 爬蟲套件
import requests as req
import pandas as pd
from io import StringIO
from fake_useragent import UserAgent
ua = UserAgent(use_external_data=True)
from time import sleep
from bs4 import BeautifulSoup as bs
from datetime import date

# MySQL套件
import pymysql
from sqlalchemy import create_engine

# 其他套件
import random


# 設定西元日期
def dc_date(start='today',over='today'):
    # 起始日期
    start_date = pd.to_datetime(f'{start}').date()
    # 日期寫入的格式 : 2023-01-01

    # 結束日期
    end_date = pd.to_datetime(f'{over}').date()

    # 生成日期範圍
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    return date_range

#     # 輸出日期範圍
#     for date in date_range:
#         datestr = date.strftime('%Y%m%d')
#         print(datestr)


# 連線資料庫，儲存資料
def link_database(table_name,df,mode):
    engine = create_engine('mysql+pymysql://root:0608@localhost:3306/stock_database')

    # 存入MyQL
    df.to_sql(f'{table_name}', engine, if_exists='append', index=False)

    # 排序
    if mode == 1:
        
        # 檢查重複項
        check_repeat = pd.read_sql(f'select * from {table_name}', engine)
        check_repeat = check_repeat.dropna(subset=['交易日期']).drop_duplicates(['證券代號','交易日期'], keep='last')

        # 排序
        check_repeat = check_repeat.sort_values(['證券代號','交易日期'], ascending=[True, False])
        
    elif mode == 2:
        
        # 檢查重複項
        check_repeat = pd.read_sql(f'select * from {table_name}', engine)
        check_repeat = check_repeat.dropna(subset=['交易日期']).drop_duplicates(['交易日期'], keep='last')

        # 排序
        check_repeat = check_repeat.sort_values(['交易日期'], ascending= False)     
        
    else:
        pass

    # 備份到csv
    check_repeat.to_csv(f'{table_name}_backup.csv',encoding = "utf_8_sig")

    # 檢查完回存
    check_repeat.to_sql(f'{table_name}', engine, if_exists='replace', index=False)


    
    # 關閉通道
    engine.dispose()


# 把資料排序
def data_resort(table_name,mode):
    engine = create_engine('mysql+pymysql://root:0608@localhost:3306/stock_database')
    
    # 排序
    if mode == 1:
        
        # 檢查重複項
        check_repeat = pd.read_sql(f'select * from {table_name}', engine)
        check_repeat = check_repeat.dropna(subset=['交易日期']).drop_duplicates(['證券代號','交易日期'], keep='last')

        # 排序
        check_repeat = check_repeat.sort_values(['證券代號','交易日期'], ascending=[True, False])
        
    elif mode == 2:
        
        # 檢查重複項
        check_repeat = pd.read_sql(f'select * from {table_name}', engine)
        check_repeat = check_repeat.dropna(subset=['交易日期']).drop_duplicates(['交易日期'], keep='last')

        # 排序
        check_repeat = check_repeat.sort_values(['交易日期'], ascending= False)     
        
    else:
        pass
    
    # 檢查完回存
    check_repeat.to_sql(f'{table_name}', engine, if_exists='replace', index=False)
    
    # 關閉通道
    engine.dispose()



# 證交所歷史股價
def twse_price_crawler(start='today',over='today'):
    # user-agent
    global ua
    
    # 用日期控制迴圈
    date_range = dc_date(start,over)
    for date in date_range:
        datestr = date.strftime('%Y%m%d')
        
        # 要求
        url = f"https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={datestr}&type=ALLBUT0999&response=csv&_=1686993522510"
        my_headers = {
            "user-agent":ua.random
        }
        
        res = req.get(url,headers = my_headers)
        #res.encoding = "utf-8"
        
        # 確認是不是開盤日
        if res.text == "":
            print(f"上市股價，非交易日，沒有資料 {datestr}")
            continue
        
        # 資料清理
        # step 1
        lines = res.text.split("\n")
        newlines = []
        index_newlines = []
        for i in lines:
            if len(i.split('",')) > 10:
                newlines.append(i)
        
        # step 2
        df = pd.read_csv(StringIO("\n".join(newlines).replace("=","")))
        
        # step 3
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",",""))
        df.set_index(['證券代號', '證券名稱'], inplace = True)
        
        # step 4
        df = df.apply(lambda s: pd.to_numeric(s, errors = "coerce"))
        df = df[df.columns[df.isnull().sum() != len(df)]]
        
        # step 5
        df.insert(df.columns.get_loc("漲跌價差"),"振幅",df["最高價"]-df["最低價"])
        df["振幅"] = df["振幅"].round(2)
        
        # step 6
        df = df.reset_index()
        trade_date = date.strftime('%Y/%m/%d')
        df.insert(df.columns.get_loc("證券代號"),"交易日期",trade_date)
        df.insert(df.columns.get_loc("成交股數"),"市場類別","上市")
        
        # 匯入資料庫
        link_database("twse_price",df,1)
        
        # 睡一下
        # i = random.randint(6,15)
        sleep(1)
        
        print(f"上市股價，載入完成 {trade_date}")
    
    print("全部完成")


# 櫃買歷史股價
def otc_price_crawler(start='today',over='today'):
    # user-agent
    global ua
    
    # 用日期控制迴圈
    date_range = dc_date(start,over)
    for date in date_range:
        taiwan_year = str(date.year - 1911)
        datestr = date.strftime('%Y/%m/%d')
        taiwan_date = datestr.replace(datestr[:4],taiwan_year)
        
        # 要求
        url = f"https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_download.php?l=zh-tw&d={taiwan_date}&se=EW&_=1687053290902"
        my_headers = {
            "user-agent":ua.random
        }
        
        res = req.get(url,headers = my_headers)
        #res.encoding = "utf-8"
        
        # 確認是不是開盤日
        if res.text == f'上櫃股票每日收盤行情(不含定價) \r\n產業類別:所有證券(不含權證、牛熊證) \r\n資料日期:{taiwan_date}\r\n共0筆':
            print(f"上櫃股價，非交易日，沒有資料 {datestr}")
            continue
        
        # 資料清理
        # step 1
        lines = res.text.split("\n")
        newlines = ['"證券代號","證券名稱","收盤價","漲跌價差","開盤價","最高價","最低價","成交股數","成交金額(元)","成交筆數","最後買價","最後買量(千股)","最後賣價","最後賣量(千股)","發行股數","次日漲停價","次日跌停價"\r']
        for line in lines:
            if len(line.split('",')) > 10:
                newlines.append(line)
        
        # step 2
        df = pd.read_csv(StringIO("\n".join(newlines)))
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",",""))
        df = df.apply(lambda s: s.str.replace("統一�琤肮黕篾","統一恒生科期N"))
        df = df.apply(lambda s: s.str.replace("�矬�","恒耀"))
        df = df.apply(lambda s: s.str.replace("立��","立碁"))
        df = df.apply(lambda s: s.str.replace("宏�硌穈T","宏碁資訊"))
        df = df.apply(lambda s: s.str.replace("安�硌穈T","安碁資訊"))
        df = df.apply(lambda s: s.str.replace("安��","安碁"))
        
        # step 3
        df.set_index(["證券代號","證券名稱"], inplace = True)

        
        # step 4
        df = df.apply(lambda s: pd.to_numeric(s,errors = "coerce"))
        
        # step 5
        df.insert(df.columns.get_loc("開盤價"),"振幅",df["最高價"]-df["最低價"])
        df["振幅"] = df["振幅"].round(2)
        
        # step 6
        df = df.reset_index()
        df.insert(df.columns.get_loc("證券代號"),"交易日期",datestr)
        df.insert(df.columns.get_loc("收盤價"),"市場類別","上櫃")
        
        # 匯入資料庫
        link_database("otc_price",df,1)
        
        # 睡一下
        # i = random.randint(6,15)
        sleep(1)
        
        print(f"上櫃股價，載入完成 {datestr} = {taiwan_date}")
    
    print("全部完成")


# 證交所歷史每日三大法人爬蟲
def twse_corporation_crawler(start='today',over='today'):
    # user-agent
    global ua
    
    # 用日期控制迴圈
    date_range = dc_date(start,over)
    for date in date_range:
        datestr = date.strftime('%Y%m%d')
        
        # 要求
        url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={datestr}&selectType=ALLBUT0999&response=csv&_=1687087951796"
        my_headers = {
            "user-agent":ua.random
        }
        
        res = req.get(url,headers = my_headers)
        #res.encoding = "utf-8"
        
        # 確認是不是開盤日
        if res.text == '\r\n':
            print(f"上市三大法人，非交易日，沒有資料 {datestr}")
            continue
            
        # 資料清理
        # step 1
        lines = res.text.split("\n")
        newlines =[]
        for line in lines:
            if len(line.split('",')) > 10:
                newlines.append(line)
                
        # step 2
        df = pd.read_csv(StringIO("\n".join(newlines).replace("=","")))
        
        # step 3
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",",""))
        df.set_index(['證券代號', '證券名稱'], inplace = True)
        
        # step 4
        df = df.apply(lambda s: pd.to_numeric(s, errors = "coerce"))
        df = df[df.columns[df.isnull().sum() != len(df)]]
        
        # step 5
        df = df.reset_index()
        trade_date = date.strftime('%Y/%m/%d')
        df.insert(df.columns.get_loc("證券代號"),"交易日期",trade_date)
        df.insert(df.columns.get_loc("外陸資買進股數(不含外資自營商)"),"市場類別","上市")
        
        # 匯入資料庫
        link_database("twse_corporation_net_buy_sell",df,1)
        
        # 睡一下
        # i = random.randint(6,15)
        sleep(1)
        
        print(f"上市三大法人，載入完成 {trade_date}")
    
    print("全部完成")


# 櫃買歷史每日三大法人爬蟲
def otc_corporation_crawler(start='today',over='today'):
    # user-agent
    global ua
    
    # 用日期控制迴圈
    date_range = dc_date(start,over)
    for date in date_range:
        taiwan_year = str(date.year - 1911)
        datestr = date.strftime('%Y/%m/%d')
        taiwan_date = datestr.replace(datestr[:4],taiwan_year)
        
        # 要求
        url = f"https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_download.php?l=zh-tw&se=EW&t=D&d={taiwan_date}&_=1687094120925"
        my_headers = {
            "user-agent":ua.random
        }
        
        res = req.get(url,headers = my_headers)
        #res.encoding = "utf-8"
        
        # 確認是不是開盤日
        if res.text == '\r\n代號,名稱,外資及陸資(不含外資自營商)-買進股數,外資及陸資(不含外資自營商)-賣出股數,外資及陸資(不含外資自營商)-買賣超股數,外資自營商-買進股數,外資自營商-賣出股數,外資自營商-買賣超股數,外資及陸資-買進股數,外資及陸資-賣出股數,外資及陸資-買賣超股數,投信-買進股數,投信-賣出股數,投信-買賣超股數,自營商(自行買賣)-買進股數,自營商(自行買賣)-賣出股數,自營商(自行買賣)-買賣超股數,自營商(避險)-買進股數,自營商(避險)-賣出股數,自營商(避險)-買賣超股數,自營商-買進股數,自營商-賣出股數,自營商-買賣超股數,三大法人買賣超股數合計\r\n':
            print(f"上櫃三大法人，非交易日，沒有資料 {datestr}")
            continue
        
        # 資料清理
        # step 1
        lines = res.text.split("\n")
        newlines = ['證券代號,證券名稱,外資及陸資(不含外資自營商)-買進股數,外資及陸資(不含外資自營商)-賣出股數,外資及陸資(不含外資自營商)-買賣超股數,外資自營商-買進股數,外資自營商-賣出股數,外資自營商-買賣超股數,外資及陸資-買進股數,外資及陸資-賣出股數,外資及陸資-買賣超股數,投信-買進股數,投信-賣出股數,投信-買賣超股數,自營商(自行買賣)-買進股數,自營商(自行買賣)-賣出股數,自營商(自行買賣)-買賣超股數,自營商(避險)-買進股數,自營商(避險)-賣出股數,自營商(避險)-買賣超股數,自營商-買進股數,自營商-賣出股數,自營商-買賣超股數,三大法人買賣超股數合計\r']
        for line in lines:
            if len(line.split('",')) > 20 :
                newlines.append(line)
        
        # step 2
        df = pd.read_csv(StringIO("\n".join(newlines)))
        
        # step 3
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(",",""))
        df = df.apply(lambda s: s.str.replace("統一�琤肮黕篾","統一恒生科期N"))
        df = df.apply(lambda s: s.str.replace("�矬�","恒耀"))
        df = df.apply(lambda s: s.str.replace("立��","立碁"))
        df = df.apply(lambda s: s.str.replace("宏�硌穈T","宏碁資訊"))
        df = df.apply(lambda s: s.str.replace("安�硌穈T","安碁資訊"))
        df = df.apply(lambda s: s.str.replace("安��","安碁"))
        
        # step 4
        df.set_index(['證券代號', '證券名稱'], inplace = True)
        df = df.apply(lambda s: pd.to_numeric(s, errors = "coerce"))
        df = df[df.columns[df.isnull().sum() != len(df)]]
        
        # step 5
        df = df.reset_index()
        df.insert(df.columns.get_loc("證券代號"),"交易日期",datestr)
        df.insert(df.columns.get_loc("外資及陸資(不含外資自營商)-買進股數"),"市場類別","上櫃")
        
        # 匯入資料庫
        link_database("otc_corporation_net_buy_sell",df,1)
        
        # 睡一下
        # i = random.randint(6,15)
        sleep(1)
        
        print(f"上櫃三大法人，載入完成 {datestr} = {taiwan_date}")
    
    print("全部完成")


# 到 goodinfo 抓大盤指數
def market_index_crawler(start='today',over='today',mode='twse'):
    # user-agent
    global ua
    
    # 要求
    # 加權指數
    if mode == "twse":
        url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=%E5%8A%A0%E6%AC%8A%E6%8C%87%E6%95%B8&CHT_CAT2=DATE"
    
    # 櫃買
    if mode == "otc":
        url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=%E6%AB%83%E8%B2%B7%E6%8C%87%E6%95%B8&CHT_CAT2=DATE"

    my_headers = {
        "user-agent":ua.random
    }
    res = req.get(url,headers = my_headers)
    res.encoding = "utf-8"
    
    # 資料清理
    # step 1 : 只有第22個 dataframe 才是有大盤資料的表格
    df = pd.read_html(StringIO(res.text))
    df = df[21]
    
    # step 2 : 把原本網站載下來的column名稱刪掉
    df_data_only = df.reset_index(drop=True)
    
    # step 3 : 賦予新的欄位名稱
    df_data_only.columns = ["交易日期","開盤價","最高價","最低價","收盤價","漲跌幅","漲跌幅(%)","振幅(%)","成交量(億元)","成交均張","外資買賣超(億元)","投信買賣超(億元)","自營買賣超(億元)","合計買賣超(億元)","融資餘額(億元)","融資增減(億元)","融券餘額(億元)","融券增減(億元)"]
    df = df_data_only
    
    # step 4 : 再把表格中間不需要的欄位去掉
    df = df.drop(18)
    df = df.drop(19)
    df = df.drop(38)
    df = df.drop(39)
    df = df.drop(58)
    df = df.drop(59)
    
    # step 5 : 與start跟over的日期對照，抓出想要update的日期的資料
    date_range = dc_date(start,over)
    for date in date_range:
        datestr = date.strftime('%Y/%m/%d')
        short_date = datestr.replace(datestr[:5],"")
        condition = df["交易日期"].str.contains(short_date)
        
        # 確認日期的資料是否為空值
        if df[condition].index.empty == True:
            print(f"{mode} 非交易日，沒有資料 {datestr}")
            continue
            
        new_data = df[condition].copy()
        
        # 把資料轉成數字格式
        new_data.set_index(["交易日期"], inplace = True)
        new_data = new_data.apply(lambda s: pd.to_numeric(s,errors = "coerce"))
        new_data.insert(new_data.columns.get_loc("振幅(%)"),"振幅",new_data["最高價"] - new_data["最低價"])
        new_data["振幅"] = new_data["振幅"].round(2)
        new_data = new_data.reset_index()
        new_data["交易日期"] = datestr
        
        # 匯入資料庫
        link_database(f"{mode}_index",new_data,2)
        
        # 睡一下
        # i = random.randint(6,15)
        sleep(1)
        
        print(f"{mode} 載入完成 {datestr}")
    
    print("全部完成")


# 期交所抓台指近月最新資料
def future_twse_index_crawler():
    global ua
    
    # 用日期控制迴圈
    date_range = dc_date()
    for date in date_range:
        datestr = date.strftime('%Y/%m/%d')

        # 要求
        url = "https://www.taifex.com.tw/cht/3/futDailyMarketReport"
        my_headers = {
            "user-agent":ua.random
        }

        res = req.post(url,headers = my_headers)
        res.encoding = "utf-8"

        # 煮湯
        soup = bs(res.text,"lxml")

        # 解析，抓第一項，因為第一項是台指近月，然後抓出每一筆
        data = soup.select_one('tr[bgcolor="ivory"]')
        open_price = data.select('td[align="right"]')[0].text
        high_price = data.select('td[align="right"]')[1].text
        low_price = data.select('td[align="right"]')[2].text
        close_price = data.select('td[align="right"]')[3].text
        quantity = data.select('td[align="right"]')[5].text

        # 建立一個暫存的 dataframe
        df = pd.DataFrame({
            "交易日期":[f"{datestr}"],
            "開盤價":[open_price],
            "最高價":[high_price],
            "最低價":[low_price],
            "收盤價":[close_price],
            "成交量":[quantity]
        })

        # 資料清理
        # step 1
        df['交易日期'] = pd.to_datetime(df['交易日期'])
        df['交易日期'] = df['交易日期'].dt.strftime('%Y/%m/%d')
        df.set_index(['交易日期'], inplace = True)
        df = df.apply(lambda s: pd.to_numeric(s, errors = "coerce"))
        df = df.reset_index()
        df["振幅"] = df["最高價"] - df["最低價"]
        df["振幅"] = df["振幅"].round(2)

        # 存入 MySQL
        link_database("future_twse_index",df,2)

        print(f"載入完成 {datestr}")


# 把過去一年的加權大盤資料匯入MySQL
def import_history_twse_index():
    df = pd.read_csv("twse_history_index.csv", index_col=['交易日期'])
    df = df.apply(lambda s: pd.to_numeric(s,errors = "coerce"))
    df = df.reset_index()
    
    df.insert(df.columns.get_loc("振幅(%)"),"振幅",df["最高價"] - df["最低價"])
    df["振幅"] = df["振幅"].round(2)
    
    link_database("twse_index",df,2)


# 把過去一年的 otc 大盤資料匯入MySQL
def import_history_otc_index():
    df = pd.read_csv("otc_history_index.csv", index_col=['交易日期'])
    df = df.apply(lambda s: pd.to_numeric(s,errors = "coerce"))
    df = df.reset_index()
    
    df.insert(df.columns.get_loc("振幅(%)"),"振幅",df["最高價"] - df["最低價"])
    df["振幅"] = df["振幅"].round(2)    
    
    link_database("otc_index",df,2)


# 把過去 3 年的 台指近 資料匯入MySQL
def import_history_future_twse_index():
    df = pd.read_csv("future_twse_index.csv", index_col=['交易日期'])
    df = df.apply(lambda s: pd.to_numeric(s,errors = "coerce"))
    df = df.reset_index()
    
    df["振幅"] = df["最高價"] - df["最低價"]
    df["振幅"] = df["振幅"].round(2)
    
    link_database("future_twse_index",df,2)