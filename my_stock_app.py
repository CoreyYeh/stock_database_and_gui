# QT 介面設計

# 爬蟲套件
import requests as req
import pandas as pd
from io import StringIO
from fake_useragent import UserAgent
ua = UserAgent(use_external_data=True)
from time import sleep
from bs4 import BeautifulSoup as bs
from datetime import date
from datetime import datetime

# MySQL套件
import pymysql
from sqlalchemy import create_engine

# 使用封包
import stock_data_crawler.main_crawler as craw
import stock_data_crawler.use_stock_data as use
from stock_data_crawler.plot_candles import plot_candles

# 其他
import threading
import multiprocessing as mp
import random
from tqdm import tqdm
from io import BytesIO

# 資料視覺化
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("Qt5Agg")  # 使用 Qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 技術指標
from talib import abstract
import mplfinance as mpf

# pyqt
import PyQt5
#from PyQt5 import QtGui
#from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 導入ui介面程式
from my_stock_app_mainwindow import Ui_Dialog    #從mainwindow.py裡的東西import過來
import sys


# 資料顯示介面設定
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])

        return None


# 主畫面
class MainWindow(QMainWindow):    #這邊用來設定按鈕的動作具體要做些甚麼(function)
    def __init__(self):    
        super(MainWindow, self).__init__()    #透過繼承，繼承父類別button_setting的所有屬性與方法
        #先找到 MainWindow 的父類別 button_setting ，並用button_setting的初始化方法來初始化子類別 MainWindow
        #super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 最大化顯示視窗
        self.showMaximized()

        # 隱藏介面
        self.ui.label_target.hide()
        self.ui.radioButton_market.hide()
        self.ui.radioButton_stock.hide()
        self.ui.label_stock.hide()
        self.ui.lineEdit_stock.hide()
        self.ui.pushButton_search.hide()
        self.ui.label_stock_mode.hide()
        self.ui.radioButton_mode_search.hide()
        self.ui.radioButton_mode_select.hide()
        self.ui.radioButton_mode_test.hide()
        self.ui.label_market_index.hide()
        self.ui.radioButton_twse_index.hide()
        self.ui.radioButton_otc_index.hide()
        self.ui.radioButton_future_index.hide()
        self.ui.tableView_stock_data.hide()
        self.ui.label_search_result.hide()
        self.ui.label_search_result_2.hide()
        self.ui.checkBox_corporation.hide()
        self.ui.tableView_stock_data_2.hide()
        self.ui.pushButton_update.hide()
        #self.ui.graphicsView_stock_price.hide()
        self.ui.dateEdit_start.hide()
        self.ui.dateEdit_end.hide()
        self.ui.pushButton_go.hide()
        self.ui.label_date_to_date.hide()
        self.ui.comboBox_ma.hide()
        self.ui.checkBox_ema.hide()
        self.ui.comboBox_technical_index_1.hide()
        self.ui.comboBox_technical_index_2.hide()
        self.ui.checkBox_BBANDS.hide()

        # 資料庫連線設定
        self.engine = create_engine('mysql+pymysql://root:0608@localhost:3306/stock_database')

        # 登入設定
        self.ui.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.ui.pushButton_login.clicked.connect(self.login)

        # 更新資料設定
        self.ui.pushButton_update.clicked.connect(self.data_update)

        # 搜尋設定
        self.ui.pushButton_search.clicked.connect(self.search)

        # 介面設定
        #self.tableview = QTableView()
        #self.model = TableModel(df)

        # radiobutton分組
        # 模式分組
        self.group1 = QButtonGroup(self)
        self.group1.addButton(self.ui.radioButton_mode_search)
        self.group1.addButton(self.ui.radioButton_mode_select)
        self.group1.addButton(self.ui.radioButton_mode_test)

        # 選擇大盤或個股分組
        self.group2 = QButtonGroup(self)
        self.group2.addButton(self.ui.radioButton_market)
        self.group2.addButton(self.ui.radioButton_stock)

        # 大盤指數分組
        self.group3 = QButtonGroup(self)
        self.group3.addButton(self.ui.radioButton_twse_index)
        self.group3.addButton(self.ui.radioButton_otc_index)
        self.group3.addButton(self.ui.radioButton_future_index)

        # 選擇模式時
        self.ui.radioButton_mode_search.clicked.connect(self.mode_search)
        self.ui.radioButton_mode_select.clicked.connect(self.mode_select)
        self.ui.radioButton_mode_test.clicked.connect(self.mode_test)

        # 選擇大盤或個股時
        self.ui.radioButton_market.clicked.connect(self.choose_market)
        self.ui.radioButton_stock.clicked.connect(self.choose_stock)

        # 選取三大法人時
        self.ui.checkBox_corporation.clicked.connect(self.check_corporation)

        # 選擇日期
        self.ui.pushButton_go.clicked.connect(self.get_start_and_end_date)

        # 資料視覺化介面 >>> 股價走勢
        # self.graphicsView_stock_price.setGeometry(QtCore.QRect(970, 80, 921, 451))
        #self.scene = QGraphicsScene(self)
        #self.view = QGraphicsView(self.scene)
        self.grview = QGraphicsView(self)  # 加入 QGraphicsView
        self.grview.setGeometry(840, 70, 1051, 911)    # 設定 QGraphicsView 位置與大小
        self.scene = QGraphicsScene()      # 加入 QGraphicsScene
        self.scene.setSceneRect(840, 70, 1051, 911)
        self.grview.hide()

        # 技術指標設定
        self.ui.comboBox_technical_index_1.addItems(["指標1","STOCH","RSI","MACD","ADX","OBV","MOM"])
        self.ui.comboBox_technical_index_2.addItems(["指標2","STOCH","RSI","MACD","ADX","OBV","MOM"])

        # 設定下拉式選單 >>> MA
        self.ui.comboBox_ma.addItems(["5 MA","10 MA","20 MA","60 MA","120 MA","240 MA","360 MA"])

    def login(self):
        password = self.ui.lineEdit_password.text()
        if password == "0608":
            self.ui.label_start.hide()
            self.ui.lineEdit_password.hide()
            self.ui.pushButton_login.hide()

            self.ui.pushButton_search.show()
            self.ui.label_stock_mode.show()
            self.ui.radioButton_mode_search.show()
            #self.ui.radioButton_mode_select.show()
            #self.ui.radioButton_mode_test.show()
            self.ui.pushButton_update.show()

            # 先抓出最後交易日
            last_trade_date = use.get_last_update_date(self.engine)
            last_date_str = last_trade_date[0]
            # 將字串轉換成 QDate 物件
            last_Qdate = QDate.fromString(last_date_str, 'yyyy/MM/dd')
            
            # 將最後交易日設定為預設的結束日期
            self.ui.dateEdit_end.setDate(last_Qdate)
            # 將最後交易日設為最新的日期上限
            self.ui.dateEdit_end.setMaximumDate(last_Qdate)

            # 最後交易日往回推 90 天，作為預設的起始日期
            begin_date = last_Qdate.addDays(-90)
            self.ui.dateEdit_start.setDate(begin_date)

            # 將這兩個日期存起來作為預設
            self.default_begin_date = begin_date.toString('yyyy-MM-dd')
            self.default_end_date = last_Qdate.toString('yyyy-MM-dd')

        else:
            x = "密碼錯誤"
            message = QMessageBox()
            message.setWindowTitle("登入問題")
            message.setText(x)
            message.setIcon(3)
            message.exec()
            self.ui.lineEdit_password.clear()
    
    def data_update(self):
        result = use.get_last_update_date(self.engine)
        # result = [twes_price_last_update_date,otc_price_last_update_date,twes_corporation_last_update_date,otc_corporation_last_update_date,twes_index_last_update_date,otc_index_last_update_date,future_twes_index_last_update_date]
        
        date_list = []
        for item in result:
            #item_str = item.strftime('%Y-%m-%d')
            #print(item)
            
            # 將字串轉換為日期格式
            date_object = datetime.strptime(item, "%Y/%m/%d")

            # 將日期格式轉換為指定的日期字串格式
            formatted_date = date_object.strftime("%Y-%m-%d")

            date_list.append(formatted_date)
        
        # 呼叫爬蟲函式更新資料
        craw.twse_price_crawler(start=date_list[0])
        craw.otc_price_crawler(start=date_list[1])
        craw.twse_corporation_crawler(start=date_list[2])
        craw.otc_corporation_crawler(start=date_list[3])
        craw.market_index_crawler(start=date_list[4],over='today',mode='twse')
        craw.market_index_crawler(start=date_list[5],over='today',mode='otc')
        #craw.future_twse_index_crawler()

        # 抓出最後交易日
        last_trade_date = use.get_last_update_date(self.engine)
        last_date_str = last_trade_date[0]
        # 將字串轉換成 QDate 物件
        last_Qdate = QDate.fromString(last_date_str, 'yyyy/MM/dd')
            
        # 將最後交易日設定為預設的結束日期
        self.ui.dateEdit_end.setDate(last_Qdate)
        # 將最後交易日設為最新的日期上限
        self.ui.dateEdit_end.setMaximumDate(last_Qdate)

        # 最後交易日往回推 90 天，作為預設的起始日期
        begin_date = last_Qdate.addDays(-90)
        self.ui.dateEdit_start.setDate(begin_date)

        # 將這兩個日期存起來作為預設
        self.default_begin_date = begin_date.toString('yyyy-MM-dd')
        self.default_end_date = last_Qdate.toString('yyyy-MM-dd')

        # 完成通知
        x = "更新完成！"
        message = QMessageBox()
        message.setWindowTitle("資料更新")
        message.setText(x)
        message.setIcon(1)
        message.exec()
    
    # 股價走勢圖產生介面
    def show_data_photo(self,series):
        # 清空先前的圖片
        self.scene.clear()

        # 清除原有的圖表
        plt.clf()

        # 設定圖表的大小
        width = int(self.grview.width() / 100)
        height = int(self.grview.height() / 100)
        plt.figure(figsize=(width, height))

        # 先畫出圖形
        #plt.rcParams["figure.figsize"] = (10,4)
        series.plot()
        plt.title(f'{self.stockid}')
        plt.xlabel('date')
        plt.ylabel('value')
        #plt.show()

        # 保存圖表為圖片
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        image_buffer.seek(0)

        #image_buffer.truncate(0)

        # 創建 QPixmap 並設置圖片
        pixmap = QPixmap()
        pixmap.loadFromData(image_buffer.getvalue())

        # 設定 QGraphicsScene 的範圍
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        # 關閉圖片暫存
        image_buffer.close()

        # 在 QGraphicsScene 中添加圖片
        self.scene.addPixmap(pixmap)
        self.grview.setScene(self.scene)
    
    # 確認日期是否為預設值，每次搜尋的時候要讓日期回到預設值(跟GO按鈕不同)
    def check_date_default_or_not(self):
        self.selected_begin_date = self.ui.dateEdit_start.date().toString('yyyy-MM-dd')
        self.selected_end_date = self.ui.dateEdit_end.date().toString('yyyy-MM-dd')
        if self.selected_begin_date != self.default_begin_date:
            self.selected_begin_date = self.default_begin_date
            # 把日期調回預設
            begin_date_str = self.selected_begin_date
            begin_Qdate = QDate.fromString(begin_date_str, 'yyyy-MM-dd')
            self.ui.dateEdit_start.setDate(begin_Qdate)

        if self.selected_end_date != self.default_end_date:
            self.selected_end_date = self.default_end_date
            end_date_str = self.selected_end_date
            end_Qdate = QDate.fromString(end_date_str, 'yyyy-MM-dd')
            self.ui.dateEdit_end.setDate(end_Qdate)
         
    
    # 為了讓K線圖正確顯示要先做資料清洗
    def before_trans_k_bar(self,k_df):
        k_df = k_df.sort_values(by='交易日期', ascending=True)
        try:
            k_df["成交股數"] = k_df["成交股數"] / 1000
        except:
            pass

        k_df.rename(columns={'交易日期':'date'}, inplace = True)

        try:
            k_df.rename(columns={'成交股數':'volume'}, inplace = True)
        except:
            pass

        k_df.rename(columns={'最高價':'high'}, inplace = True)
        k_df.rename(columns={'最低價':'low'}, inplace = True)
        k_df.rename(columns={'開盤價':'open'}, inplace = True)
        k_df.rename(columns={'收盤價':'close'}, inplace = True)
        k_df['date'] = pd.to_datetime(k_df['date'])
        k_df['date'] = k_df['date'].dt.date
        k_df.set_index('date', inplace = True)
        k_df.index = pd.DatetimeIndex(k_df.index)

        return k_df       
    
    # 顯示K線圖
    def show_k_bar(self,k_df):
        # 清空先前的圖片
        self.scene.clear()

        # 清除原有的圖表
        plt.clf()

        # 設定圖表的大小
        #width = int(self.grview.width() / 100)
        #height = int(self.grview.height() / 100)
        #plt.figure(figsize=(width, height))

        # 繪圖
            
        #df.index = df.index.date
        # k_df = k_df.sort_values(by='交易日期', ascending=True)
        # k_df["成交股數"] = k_df["成交股數"] / 1000
        # k_df.rename(columns={'交易日期':'date'}, inplace = True)
        # k_df.rename(columns={'成交股數':'volume'}, inplace = True)
        # k_df.rename(columns={'最高價':'high'}, inplace = True)
        # k_df.rename(columns={'最低價':'low'}, inplace = True)
        # k_df.rename(columns={'開盤價':'open'}, inplace = True)
        # k_df.rename(columns={'收盤價':'close'}, inplace = True)
        # k_df = k_df.iloc[:, :-3]
        # k_df['date'] = pd.to_datetime(k_df['date'])
        # k_df['date'] = k_df['date'].dt.date
        # k_df.set_index('date', inplace = True)
        # k_df.index = pd.DatetimeIndex(k_df.index)

        # 抓出現在下拉式選單的選項
        ma_text = self.ui.comboBox_ma.currentText()
        ma_text = int(ma_text.replace(" MA",""))

        # 確認現在是SMA還是EMA
        if self.ui.checkBox_ema.isChecked() == True:
            SMA = abstract.EMA(k_df,timeperiod=ma_text)
        else:
            SMA = abstract.SMA(k_df,timeperiod=ma_text)

        RSI = abstract.RSI(k_df)
        STOCH = abstract.STOCH(k_df)
        MACD = abstract.MACD(k_df)
        ADX = abstract.ADX(k_df)
        OBV = abstract.OBV(k_df)
        MOM = abstract.MOM(k_df)

        # 檢查哪個技術指標被選取
        technicals_index_list = []
        technicals_index_str = []
        technical_1 = self.ui.comboBox_technical_index_1.currentText()
        technical_2 = self.ui.comboBox_technical_index_2.currentText()
        if technical_1 != "指標1":
            technicals_index_str.append(technical_1)
        if technical_2 != "指標2":
            technicals_index_str.append(technical_2)

        for item in technicals_index_str:
            if item == "STOCH":
                technicals_index_list.append(STOCH)
            elif item == "RSI":
                technicals_index_list.append(RSI)
            elif item == "MACD":
                technicals_index_list.append(MACD)
            elif item == "ADX":
                technicals_index_list.append(ADX)
            elif item == "OBV":
                technicals_index_list.append(OBV)
            else:
                technicals_index_list.append(MOM)           

        # 如果顯示的是 指標1/2 就不用繪出技術分析圖
        # 確認布林通道是否有被勾選
        if self.ui.checkBox_BBANDS.isChecked() == True:
            BBANDS = abstract.BBANDS(k_df,timeperiod=ma_text)
            plot_candles(
                        # 起始時間、結束時間
                        start_time=self.selected_begin_date,
                        end_time=self.selected_end_date,
                                
                        # 股票的資料
                        pricing=k_df, 
                        title='Candles', 
                        
                        # 是否畫出成交量？
                        volume_bars=True, 
                        
                        # 將某些指標（如SMA）跟 K 線圖畫在一起
                        overlays=[SMA,BBANDS], 
                        
                        # 將某些指標（如RSI, STOCH）單獨畫在獨立的畫格中
                        technicals = technicals_index_list,
                        
                        # 重新命名額外的畫格名稱（跟指標名稱一樣就可以囉！）
                        technicals_titles=technicals_index_str
                        )
        else:
            plot_candles(
                        # 起始時間、結束時間
                        start_time=self.selected_begin_date,
                        end_time=self.selected_end_date,
                                
                        # 股票的資料
                        pricing=k_df, 
                        title='Candles', 
                        
                        # 是否畫出成交量？
                        volume_bars=True, 
                        
                        # 將某些指標（如SMA）跟 K 線圖畫在一起
                        overlays=[SMA], 
                        
                        # 將某些指標（如RSI, STOCH）單獨畫在獨立的畫格中
                        technicals = technicals_index_list,
                        
                        # 重新命名額外的畫格名稱（跟指標名稱一樣就可以囉！）
                        technicals_titles=technicals_index_str
                        )

        # 保存圖表為圖片
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        image_buffer.seek(0)

        #image_buffer.truncate(0)

        # 創建 QPixmap 並設置圖片
        pixmap = QPixmap()
        pixmap.loadFromData(image_buffer.getvalue())

        # 設定 QGraphicsScene 的範圍
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        # 關閉圖片暫存
        image_buffer.close()

        # 在 QGraphicsScene 中添加圖片
        self.scene.addPixmap(pixmap)
        self.grview.setScene(self.scene)

        """
        mc = mpf.make_marketcolors(up='r',down='g',inherit=True)
        s  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mc)
        kwargs = dict(type='candle', mav=(5,20,60), volume=True, figratio=(1000,800), figscale=0.75, title='Stock Chart', style=s)
        
        # 保存圖表為圖片
        image_buffer = BytesIO()
        mpf.plot(k_df, **kwargs, savefig=dict(fname=image_buffer, format='png'), closefig=True)
        image_buffer.seek(0)

        # 創建 QPixmap 並設置圖片
        pixmap = QPixmap()
        pixmap.loadFromData(image_buffer.getvalue())
                
        # 設定 QGraphicsScene 的範圍
        self.scene.setSceneRect(0, 0, 1000, 800)

        # 關閉圖片暫存
        image_buffer.close()

        # 在 QGraphicsScene 中添加圖片
        self.scene.addPixmap(pixmap)
        self.grview.setScene(self.scene)
        """

    def search(self):
        # 顯示結果介面
        self.ui.tableView_stock_data.show()
        self.ui.label_search_result.show()
        self.ui.label_search_result_2.show()
        #self.ui.graphicsView_stock_price.show()
        self.grview.show()
        self.ui.dateEdit_start.show()
        self.ui.dateEdit_end.show()
        self.ui.label_date_to_date.show()
        self.ui.pushButton_go.show()
        self.ui.comboBox_ma.show()
        self.ui.checkBox_ema.show()
        self.ui.comboBox_technical_index_1.show()
        self.ui.comboBox_technical_index_2.show()
        self.ui.checkBox_BBANDS.show()

        # 讓MA線回到預設值
        ma_default = self.ui.comboBox_ma.currentText()
        ma_index = self.ui.comboBox_ma.findText('5 MA')
        if ma_default != "5 MA":
            self.ui.comboBox_ma.setCurrentIndex(ma_index)
        
        # 讓EMA的勾選消失
        if self.ui.checkBox_ema.isChecked() == True:
            self.ui.checkBox_ema.setChecked(False)
        
        # 確認布林通道是否有被勾選，讓布林通道的勾選消失
        if self.ui.checkBox_BBANDS.isChecked() == True:
            self.ui.checkBox_BBANDS.setChecked(False)
        
        # 確認指標是否為 指標1/2 ，讓其回到該選項
        index_1_default = self.ui.comboBox_technical_index_1.currentText()
        find_index_1 = self.ui.comboBox_technical_index_1.findText('指標1')
        if index_1_default != '指標1':
            self.ui.comboBox_technical_index_1.setCurrentIndex(find_index_1)

        index_2_default = self.ui.comboBox_technical_index_2.currentText()
        find_index_2 = self.ui.comboBox_technical_index_2.findText('指標2')
        if index_2_default != '指標2':
            self.ui.comboBox_technical_index_2.setCurrentIndex(find_index_2)        

        # 先確認是要查詢哪個  >>> 用哪個radiobutton被選取來判斷
        # 如果大盤被選取，查詢大盤
        if self.ui.radioButton_market.isChecked() == True:
            # 判斷是哪個大盤指數被選取
            checkedButton = self.group3.checkedButton()
            self.market = checkedButton.text()
            if self.market == "加權指數":
                self.market = "twse_index"
            elif self.market == "櫃買指數":
                self.market = "otc_index"
            else:
                self.market = "future_twse_index"

            # 抓出資料，使用封包內的函數
            result = use.show_index(self.market,self.engine)

            # 匯入tableview視窗
            self.ui.label_search_result.setText(result[1])
            self.ui.label_search_result_2.setText(result[2])
            self.model = TableModel(result[0])
            self.ui.tableView_stock_data.setModel(self.model)

            # 顯示股價走勢
            # 資料清洗
            self.index_k_df = result[0].copy()
            if self.market == "future_twse_index":
                self.index_k_df = self.index_k_df.drop("振幅", axis=1)
                self.index_k_df.rename(columns={'成交量':'volume'}, inplace = True)
            else:
                self.index_k_df = self.index_k_df.drop(['漲跌幅', '漲跌幅(%)', '振幅', '振幅(%)',"成交均張","外資買賣超(億元)","投信買賣超(億元)","自營買賣超(億元)","合計買賣超(億元)","融資餘額(億元)","融資增減(億元)","融券餘額(億元)","融券增減(億元)"], axis=1)
                self.index_k_df.rename(columns={'成交量(億元)':'volume'}, inplace = True)

            self.index_k_df = self.before_trans_k_bar(self.index_k_df)
            self.check_date_default_or_not()
            self.show_k_bar(self.index_k_df)

            # 增加三大法人選項
            if self.market == "future_twse_index":
                self.ui.checkBox_corporation.hide()
                self.ui.tableView_stock_data_2.hide()
            
            else:
                self.ui.checkBox_corporation.show()

                # 將三大法人資料匯入
                self.check_corporation()

        # 如果個股被選取，查詢股票
        elif self.ui.radioButton_stock.isChecked() == True:
            self.stockid = self.ui.lineEdit_stock.text()

            # 使用封包內的函數
            result = use.show_price_data(self.stockid,self.engine)

            # 將股票的市場類別存起來
            self.market_type = result[3]

            # 匯入tableview視窗
            self.ui.label_search_result.setText(result[1])
            self.ui.label_search_result_2.setText(result[2])
            self.model = TableModel(result[0])
            self.ui.tableView_stock_data.setModel(self.model)

            # 顯示股價走勢
            #self.show_data_photo(result[4]['收盤價'])

            # 技術指標
            # 預設顯示K線圖
            # # 先抓出最後交易日
            # last_trade_date = use.get_last_update_date(self.engine)
            
            # last_date_str = last_trade_date[0]
            # # 將字串轉換成 QDate 物件
            # last_Qdate = QDate.fromString(last_date_str, 'yyyy/MM/dd')
            # # 將最後交易日設定為預設的結束日期
            # self.ui.dateEdit_end.setDate(last_Qdate)
            # # 將最後交易日設為最新的日期上限
            # self.ui.dateEdit_end.setMaximumDate(last_Qdate)

            # # 最後交易日往回推 60 天，作為預設的起始日期
            # begin_date = last_Qdate.addDays(-60)
            # self.ui.dateEdit_start.setDate(begin_date)

            # 呼叫執行K線圖與技術指標的函式
            # 先從 起始日期 跟 結束日期 抓出要代入的日期
            # self.selected_begin_date = self.ui.dateEdit_start.date().toString('yyyy-MM-dd')
            # self.selected_end_date = self.ui.dateEdit_end.date().toString('yyyy-MM-dd')
            # if self.selected_begin_date != self.default_begin_date:
            #     self.selected_begin_date = self.default_begin_date
            #     # 把日期調回預設
            #     begin_date_str = self.selected_begin_date
            #     begin_Qdate = QDate.fromString(begin_date_str, 'yyyy-MM-dd')
            #     self.ui.dateEdit_start.setDate(begin_Qdate)

            # if self.selected_end_date != self.default_end_date:
            #     self.selected_end_date = self.default_end_date
            #     end_date_str = self.selected_end_date
            #     end_Qdate = QDate.fromString(end_date_str, 'yyyy-MM-dd')
            #     self.ui.dateEdit_end.setDate(end_Qdate)

            self.check_date_default_or_not()
            self.k_df = result[0].copy()
            if self.market_type == "上市":
                self.k_df = self.k_df.drop(['振幅', '漲跌價差','本益比'], axis=1)
            else:
                self.k_df = self.k_df.drop(['漲跌價差', '振幅'], axis=1)
            self.k_df = self.before_trans_k_bar(self.k_df)
            self.show_k_bar(self.k_df)

            # 增加三大法人選項
            self.ui.checkBox_corporation.show()

            # 將三大法人資料匯入
            self.check_corporation()
        
        # 完成通知
        y = "查詢完成！"
        message = QMessageBox()
        message.setWindowTitle("資料查詢")
        message.setText(y)
        message.setIcon(1)
        message.exec()

    # 選取三大法人
    def check_corporation(self):
        if self.ui.checkBox_corporation.isChecked():
            # 三大法人視窗顯示
            self.ui.tableView_stock_data_2.show()
            # 抓出資料
            # 如果目前是個股的模式被選取
            if self.ui.radioButton_stock.isChecked():
                self.stockid = self.ui.lineEdit_stock.text()
                corporation_result = use.show_corporation(self.stockid,self.engine)
                # 顯示到介面上
                self.model = TableModel(corporation_result[0])
                self.ui.tableView_stock_data_2.setModel(self.model)
            
            # 如果目前是大盤的模式被選取
            else:
                if self.market == "future_twse_index":
                    self.ui.tableView_stock_data_2.hide()
                    self.ui.checkBox_corporation.setChecked(False)
                    self.ui.checkBox_corporation.hide()
                else:
                    market_index_corporation_result = use.show_market_index_corporation(self.market,self.engine)

                    # 顯示到介面上
                    self.model = TableModel(market_index_corporation_result[0])
                    self.ui.tableView_stock_data_2.setModel(self.model)
        else:
            self.ui.tableView_stock_data_2.hide()

        # if self.stockid.isdigit() == True:
        #     df = pd.read_sql(f"select * from twse_price WHERE `證券代號` = {self.stockid}", self.engine)
        #     is_empty = df.empty
        #     if is_empty == True:
        #         df = pd.read_sql(f"select * from otc_price WHERE `證券代號` = {self.stockid}", self.engine)
        #     sid = self.stockid
        #     sname = df.at[1,"證券名稱"]
        #     stype = df.at[1,"市場類別"]

        # else:
        #     df = pd.read_sql(f"select * from twse_price WHERE `證券名稱` = '{self.stockid}'", self.engine)
        #     is_empty = df.empty
        #     if is_empty == True:
        #         df = pd.read_sql(f"select * from otc_price WHERE `證券名稱` = '{self.stockid}'", self.engine)
        #     sid = df.at[1,"證券代號"]
        #     sname = self.stockid
        #     stype = df.at[1,"市場類別"]
            
        #df.drop(df.columns[[1,2,3,5,6,13,14,15,16]], axis=1, inplace=True)
        # self.ui.label_search_result.setText(f"證券代號：{sid}  |  證券名稱：{sname}  |  市場類別：{stype}")
        # self.model = TableModel(df)
        # self.ui.tableView_stock_data.setModel(self.model)
        #self.tableview.setModel(self.model)
        #self.setCentralWidget(self.tableview)
        #self.tableview.show()
    
    # 設定清空 radio button 的函數
    def clear_selection(self,group):
        # 取消單選限制
        group.setExclusive(False)

        # 獲取當前被選取的 RadioButton
        checkedButton = group.checkedButton()

        # 如果有被選取的 RadioButton，將其設置為未選取狀態
        if checkedButton is not None:
            checkedButton.setChecked(False)

        # 恢復單選限制
        group.setExclusive(True)
    
    # 選擇查詢模式
    def mode_search(self):
        self.ui.label_target.show()
        self.ui.radioButton_market.show()
        self.ui.radioButton_stock.show()
        # 清空其他選擇
        self.clear_selection(self.group2)
        self.clear_selection(self.group3)
    
    # 選擇選股模式
    def mode_select(self):
        self.ui.label_target.hide()
        self.ui.radioButton_market.hide()
        self.ui.radioButton_stock.hide()
        self.ui.label_market_index.hide()
        self.ui.radioButton_twse_index.hide()
        self.ui.radioButton_otc_index.hide()
        self.ui.radioButton_future_index.hide()
        self.ui.label_stock.hide()
        self.ui.lineEdit_stock.hide()
        # 清空其他選擇
        self.clear_selection(self.group2)
        self.clear_selection(self.group3)
    
    # 選擇回測模式
    def mode_test(self):
        self.ui.label_target.hide()
        self.ui.radioButton_market.hide()
        self.ui.radioButton_stock.hide()
        self.ui.label_market_index.hide()
        self.ui.radioButton_twse_index.hide()
        self.ui.radioButton_otc_index.hide()
        self.ui.radioButton_future_index.hide()
        self.ui.label_stock.hide()
        self.ui.lineEdit_stock.hide()
        # 清空其他選擇
        self.clear_selection(self.group2)
        self.clear_selection(self.group3)
    
    # 選擇查詢大盤
    def choose_market(self):
        self.ui.label_market_index.show()
        self.ui.radioButton_twse_index.show()
        self.ui.radioButton_otc_index.show()
        self.ui.radioButton_future_index.show()
        self.ui.label_stock.hide()
        self.ui.lineEdit_stock.hide()
        # 清空其他選擇
        self.clear_selection(self.group3)
        self.ui.lineEdit_stock.clear()

    # 選擇查詢股票
    def choose_stock(self):
        self.ui.label_stock.show()
        self.ui.lineEdit_stock.show()
        self.ui.label_market_index.hide()
        self.ui.radioButton_twse_index.hide()
        self.ui.radioButton_otc_index.hide()
        self.ui.radioButton_future_index.hide()
        # 清空其他選擇
        self.clear_selection(self.group3)
    
    def get_start_and_end_date(self):
        # 抓出現在選定的日期範圍，然後跑出K線圖
        self.selected_begin_date = self.ui.dateEdit_start.date().toString('yyyy-MM-dd')
        self.selected_end_date = self.ui.dateEdit_end.date().toString('yyyy-MM-dd')

        # 如果大盤被選取，就跑大盤的K線圖
        if self.ui.radioButton_market.isChecked() == True:
            self.show_k_bar(self.index_k_df)
        else:
            self.show_k_bar(self.k_df)
    
    # 執行所選取的技術指標
    # def run_technicals_index(self):
    #     ma_text = self.ui.comboBox_ma.currentText()
    #     print(ma_text)



    def app_close(self):
        self.engine.dispose() # close database
        self.close() # close app




def main_app():
    # 啟動式
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())  




if __name__ == "__main__":
    main_app()