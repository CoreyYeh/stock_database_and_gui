# stock_database_and_gui<br>
這個專案主要是以爬蟲方式將網路上的股價以及相關資訊抓取下來，透過pandas進行資料清理之後，再儲存到MySQL內。接著再運用Qt designer以及pyqt5製作一個簡易的看盤軟體。<br>
1. stock_data_crawler 是一個封包後的資料夾，裡面負責主要的爬蟲程式，K線圖程式，gui資料呈現整理。<br>
2. set_database.py 運用封包內的爬蟲程式檔，建立資料庫的程式檔。<br>
3. import_future_index_from_csv.py 將資料不經由gui直接匯入資料庫的程式。<br>
4. my_stock_app.ui 從qt designer生成gui的.ui檔。<br>
5. my_stock_app_mainwindow.py 將.ui檔轉換成.py檔所生成。<br>
6. my_stock_app.py 設定gui的功能的程式檔。<br><br>

成品展示：https://drive.google.com/file/d/1xsC7_tc8eatlq1_x9fscsVJqkAfWF9Yf/view?usp=sharing

## stock_data_crawler
stock_data_crawler是一個封包後的資料夾，裡面的主要分成抓取資料的爬蟲主程式main_crawler.py、繪製K線圖plot_candles.py、以及資料呈現的use_stock_data.py三個。<br>
其中，plot_candles.py是使用finlab網路課程所授之繪圖程式碼，非本人親自撰寫。<br><br>

__爬蟲主程式 main_crawler.py__<br/><br>

* def dc_date(start='today',over='today')<br>
設定想要抓取的資料範圍，透過pandas的pd.date_range生成日期範圍並回傳出去，預設值是今天。<br><br>

* def link_database(table_name,df,mode)<br>
負責連線mysql資料庫，並儲存資料，同時會檢查重複項、將重複項刪除，再按照所輸入的mode進行不同的排序，mode=1則按照'證券代號','交易日期'排序，mode=2則按照'交易日期'排序，最後再另存一份倒csv檔備份。<br>
其中，table_name是將要儲存到資料庫的table名稱。<br><br>

* def twse_price_crawler(start='today',over='today')<br>
爬取證交所的上市股價資料。使用時須輸入想要抓取的資料日期範圍，預設值為今日，首先會呼叫dc_date，將輸入的日期範圍代入，生成list的日期範圍，再用requests.get方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br><br>

* def otc_price_crawler(start='today',over='today')<br>
爬取櫃買中心的上櫃股價資料。使用時須輸入想要抓取的資料日期範圍，預設值為今日，首先會呼叫dc_date，將輸入的日期範圍代入，生成list的日期範圍，再用requests.get方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br><br>

* def twse_corporation_crawler(start='today',over='today')<br>
爬取證交所的上市股票的三大法人買賣超資料。使用時須輸入想要抓取的資料日期範圍，預設值為今日，首先會呼叫dc_date，將輸入的日期範圍代入，生成list的日期範圍，再用requests.get方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br><br>

* def otc_corporation_crawler(start='today',over='today')<br>
爬取櫃買中心的上櫃股票的三大法人買賣超資料。使用時須輸入想要抓取的資料日期範圍，預設值為今日，首先會呼叫dc_date，將輸入的日期範圍代入，生成list的日期範圍，再用requests.get方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br><br>

* def market_index_crawler(start='today',over='today',mode='twse')<br>
爬取goodinfo的大盤資料。使用時須輸入想要抓取的資料日期範圍，預設值為今日，首先會呼叫dc_date，將輸入的日期範圍代入，生成list的日期範圍，再用requests.get方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br>
其中，mode預設為抓取加權股價指數的相關資訊，若是將mode設定為otc，則是抓取櫃買指數的相關資訊<br><br>

* def future_twse_index_crawler()<br>
爬取期交所的台指近月盤後資料。使用時不須輸入想要抓取的資料日期範圍，首先會呼叫dc_date，因為沒有輸入的日期範圍，所以dc_date的預設就已今日執行，生成list的日期範圍，再用requests.get以及beautifulsoup方法進行爬蟲，將爬取下的資料匯入pandas，再進行資料清理、格式設定，最後再呼叫
link_database函式，將資料匯入資料庫。<br>
其中，因為台指期分成很多不同期數，因此沒有直接的台指近月資料，故以beautifulsoup抓取最上方一筆資料，即為台指近月的最新資料，所以這部分無法透過設定日期範圍來抓取大量資料，只能抓取最新值。<br><br>

* def import_history_twse_index()<br>
goodinfo有提供最多一年的大盤歷史資訊，因此先將該資料以.csv方式下載下來之後，再以python讀取並匯入mysql。<br><br>

* def import_history_otc_index()<br>
goodinfo有提供最多一年的otc歷史資訊，因此先將該資料以.csv方式下載下來之後，再以python讀取並匯入mysql。<br><br>

* def import_history_future_twse_index()<br>
因為XQ有提供長期的歷史資料，因此先在XQ上將台指近月的三年歷史資料匯出城.csv後，再用python讀取並匯入mysql。<br><br>

__gui上資料呈現 use_stock_data.py__<br/><br>
這部分主要是在處理將資料庫的資料讀取出來後，要在後續的gui上呈現多少(因為一開始在抓資料的時候接以大量跟完整性為主，但顯示在gui上時，以主要常見的內容為主)。<br><br>

* def get_last_update_date(engine)<br>
這個函式是在抓出每一個table最新一筆資料的日期是多少。<br><br>

* def show_price_data(id,engine)<br>
透過證券代號搜尋資料庫中的證券股價相關資料，並將股價資訊回傳。<br><br>

* def show_index(market,engine)<br>
透過所設定的市場搜尋加權股價指數或是otc指數或台指近月後回傳相關資料。<br><br>

* def show_corporation(id,engine)<br>
透過證券代號搜尋資料庫中的證券三大法人相關資料，並將股價資訊回傳。<br><br>

* def show_market_index_corporation(market,engine)<br>
透過所設定的市場搜尋資料庫中的市場三大法人相關資料，並將股價資訊回傳。<br><br>

__繪製K線圖 plot_candles.py__<br/><br>
使用finlab網路課程所授之繪圖程式碼，供gui介面顯示使用。<br><br>

## set_database.py
使用封包stock_data_crawler.main_crawler內的爬蟲程式，twse_price_crawler,otc_price_crawler,twse_corporation_crawler,otc_corporation_crawler，爬取上市股價、上櫃股價、上市三大法人、上櫃三大法人。<br>
使用multiprocessing方法進行執行。<br><br>

## my_stock_app.py
gui的設定主程式，主要有設定：
* def login(self) 登入頁面<br><br>

* def data_update(self) 更新資料<br>
資料更新，透過封包使用use_stock_data.py內的get_last_update_date函式，抓出最新的一筆資料日期。接著再呼叫main_crawler內的爬蟲程式，twse_price_crawler,otc_price_crawler,twse_corporation_crawler,otc_corporation_crawler，並將日期代入起始日，這樣即使中間漏掉好幾天沒更新資料也能自動補齊。<br>
<br>

* def show_data_photo(self,series)<br>
這部分主要是將生成的K線圖儲存成圖片，以便顯示在gui上。<br><br>

* def check_date_default_or_not(self)<br>
確認日期是否為預設值，每次搜尋的時候要讓日期回到預設值。<br><br>

* def before_trans_k_bar(self,k_df)<br>
為了讓K線圖正確顯示要先做資料清洗。將想要顯示的股價資料的dataframe代入，這個函式會將其資料格式轉換成能被plot_candles.py運用的格式。<br><br>

* def show_k_bar(self,k_df)<br>
顯示K線圖。此部分會先將gui上現有的圖片清除，再抓出抓出現在下拉式選單的選項哪個技術指標被勾選，接著再使用封包內的plot_candles，匯出K線圖與技術指標圖。<br><br>

* def search(self)<br>
顯示搜尋結果介面。清除上一次的搜尋結果，並將部分按鈕回歸預設，再確認哪些有被勾選，最後按照情況匯出股票資訊。<br><br>

* def check_corporation(self)<br>
如果三大法人的checkBox被勾選，就匯出三大法人資料。若沒被勾選就隱藏。<br><br>

* def main_app()<br>
gui啟動式。
