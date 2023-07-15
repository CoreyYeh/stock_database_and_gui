import pandas as pd
import pymysql
from sqlalchemy import create_engine

df = pd.read_csv("future_index.csv", index_col=['交易日期'])
df = df.reset_index()
df['交易日期'] = pd.to_datetime(df['交易日期'])
df['交易日期'] = df['交易日期'].dt.strftime('%Y/%m/%d')
df.set_index(['交易日期'], inplace = True)
df = df.apply(lambda s: pd.to_numeric(s, errors = "coerce"))
df = df.reset_index()
df["振幅"] = df["最高價"] - df["最低價"]
df["振幅"] = df["振幅"].round(2)

engine = create_engine('mysql+pymysql://root:0608@localhost:3306/stock_database')

df.to_sql('future_twse_index', engine, if_exists='append', index=False)
# 檢查重複項
check_repeat = pd.read_sql('select * from future_twse_index', engine)
check_repeat = check_repeat.dropna(subset=['交易日期']).drop_duplicates(['交易日期'], keep='last')

# 排序
check_repeat = check_repeat.sort_values(['交易日期'], ascending= False) 

# 備份到csv
check_repeat.to_csv('future_twse_index_backup.csv',encoding = "utf_8_sig")

# 檢查完回存
check_repeat.to_sql('future_twse_index', engine, if_exists='replace', index=False)

engine.dispose()