# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_stock_app.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        self.label_start = QtWidgets.QLabel(Dialog)
        self.label_start.setGeometry(QtCore.QRect(750, 340, 391, 81))
        self.label_start.setStyleSheet("font: 75 24pt \"微軟正黑體\";")
        self.label_start.setAlignment(QtCore.Qt.AlignCenter)
        self.label_start.setObjectName("label_start")
        self.pushButton_login = QtWidgets.QPushButton(Dialog)
        self.pushButton_login.setGeometry(QtCore.QRect(850, 540, 191, 51))
        self.pushButton_login.setStyleSheet("font: 75 20pt \"微軟正黑體\";")
        self.pushButton_login.setObjectName("pushButton_login")
        self.lineEdit_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_password.setGeometry(QtCore.QRect(820, 440, 251, 61))
        self.lineEdit_password.setStyleSheet("font: 75 18pt \"微軟正黑體\";")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_stock = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_stock.setGeometry(QtCore.QRect(200, 120, 161, 41))
        self.lineEdit_stock.setStyleSheet("font: 75 16pt \"微軟正黑體\";")
        self.lineEdit_stock.setObjectName("lineEdit_stock")
        self.label_stock = QtWidgets.QLabel(Dialog)
        self.label_stock.setGeometry(QtCore.QRect(20, 120, 171, 41))
        self.label_stock.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.label_stock.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_stock.setObjectName("label_stock")
        self.pushButton_search = QtWidgets.QPushButton(Dialog)
        self.pushButton_search.setGeometry(QtCore.QRect(620, 80, 161, 41))
        self.pushButton_search.setStyleSheet("font: 75 16pt \"微軟正黑體\";\n"
"color: rgb(0, 85, 255);")
        self.pushButton_search.setObjectName("pushButton_search")
        self.label_stock_mode = QtWidgets.QLabel(Dialog)
        self.label_stock_mode.setGeometry(QtCore.QRect(20, 20, 171, 41))
        self.label_stock_mode.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.label_stock_mode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_stock_mode.setObjectName("label_stock_mode")
        self.radioButton_mode_search = QtWidgets.QRadioButton(Dialog)
        self.radioButton_mode_search.setGeometry(QtCore.QRect(200, 20, 131, 41))
        self.radioButton_mode_search.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_mode_search.setObjectName("radioButton_mode_search")
        self.radioButton_mode_select = QtWidgets.QRadioButton(Dialog)
        self.radioButton_mode_select.setGeometry(QtCore.QRect(330, 20, 131, 41))
        self.radioButton_mode_select.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_mode_select.setObjectName("radioButton_mode_select")
        self.radioButton_mode_test = QtWidgets.QRadioButton(Dialog)
        self.radioButton_mode_test.setGeometry(QtCore.QRect(460, 20, 131, 41))
        self.radioButton_mode_test.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_mode_test.setObjectName("radioButton_mode_test")
        self.label_market_index = QtWidgets.QLabel(Dialog)
        self.label_market_index.setGeometry(QtCore.QRect(20, 120, 171, 41))
        self.label_market_index.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.label_market_index.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_market_index.setObjectName("label_market_index")
        self.radioButton_twse_index = QtWidgets.QRadioButton(Dialog)
        self.radioButton_twse_index.setGeometry(QtCore.QRect(200, 120, 131, 41))
        self.radioButton_twse_index.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_twse_index.setObjectName("radioButton_twse_index")
        self.radioButton_otc_index = QtWidgets.QRadioButton(Dialog)
        self.radioButton_otc_index.setGeometry(QtCore.QRect(330, 120, 131, 41))
        self.radioButton_otc_index.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_otc_index.setObjectName("radioButton_otc_index")
        self.radioButton_future_index = QtWidgets.QRadioButton(Dialog)
        self.radioButton_future_index.setGeometry(QtCore.QRect(460, 120, 131, 41))
        self.radioButton_future_index.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_future_index.setObjectName("radioButton_future_index")
        self.tableView_stock_data = QtWidgets.QTableView(Dialog)
        self.tableView_stock_data.setGeometry(QtCore.QRect(20, 390, 791, 271))
        self.tableView_stock_data.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView_stock_data.setObjectName("tableView_stock_data")
        self.label_search_result = QtWidgets.QLabel(Dialog)
        self.label_search_result.setGeometry(QtCore.QRect(20, 190, 621, 41))
        self.label_search_result.setStyleSheet("font: 75 12pt \"微軟正黑體\";\n"
"color: rgb(0, 0, 173);")
        self.label_search_result.setObjectName("label_search_result")
        self.radioButton_market = QtWidgets.QRadioButton(Dialog)
        self.radioButton_market.setGeometry(QtCore.QRect(200, 70, 131, 41))
        self.radioButton_market.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_market.setObjectName("radioButton_market")
        self.radioButton_stock = QtWidgets.QRadioButton(Dialog)
        self.radioButton_stock.setGeometry(QtCore.QRect(330, 70, 131, 41))
        self.radioButton_stock.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.radioButton_stock.setObjectName("radioButton_stock")
        self.label_target = QtWidgets.QLabel(Dialog)
        self.label_target.setGeometry(QtCore.QRect(20, 70, 171, 41))
        self.label_target.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.label_target.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_target.setObjectName("label_target")
        self.label_search_result_2 = QtWidgets.QLabel(Dialog)
        self.label_search_result_2.setGeometry(QtCore.QRect(20, 240, 791, 141))
        self.label_search_result_2.setStyleSheet("font: 75 12pt \"微軟正黑體\";\n"
"color: rgb(0, 0, 173);")
        self.label_search_result_2.setObjectName("label_search_result_2")
        self.checkBox_corporation = QtWidgets.QCheckBox(Dialog)
        self.checkBox_corporation.setGeometry(QtCore.QRect(20, 670, 121, 31))
        self.checkBox_corporation.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.checkBox_corporation.setObjectName("checkBox_corporation")
        self.tableView_stock_data_2 = QtWidgets.QTableView(Dialog)
        self.tableView_stock_data_2.setGeometry(QtCore.QRect(20, 710, 791, 271))
        self.tableView_stock_data_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView_stock_data_2.setObjectName("tableView_stock_data_2")
        self.pushButton_update = QtWidgets.QPushButton(Dialog)
        self.pushButton_update.setGeometry(QtCore.QRect(620, 20, 161, 41))
        self.pushButton_update.setStyleSheet("font: 75 16pt \"微軟正黑體\";\n"
"color: rgb(255, 0, 0);")
        self.pushButton_update.setObjectName("pushButton_update")
        self.label_date_to_date = QtWidgets.QLabel(Dialog)
        self.label_date_to_date.setGeometry(QtCore.QRect(1010, 20, 41, 41))
        self.label_date_to_date.setStyleSheet("font: 75 16pt \"微軟正黑體\";")
        self.label_date_to_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date_to_date.setObjectName("label_date_to_date")
        self.dateEdit_start = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_start.setGeometry(QtCore.QRect(840, 20, 171, 41))
        self.dateEdit_start.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.dateEdit_start.setMinimumDate(QtCore.QDate(2019, 3, 23))
        self.dateEdit_start.setDate(QtCore.QDate(2023, 1, 1))
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.dateEdit_end = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_end.setGeometry(QtCore.QRect(1050, 20, 171, 41))
        self.dateEdit_end.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.dateEdit_end.setMinimumDate(QtCore.QDate(2019, 3, 23))
        self.dateEdit_end.setDate(QtCore.QDate(2023, 1, 1))
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.pushButton_go = QtWidgets.QPushButton(Dialog)
        self.pushButton_go.setGeometry(QtCore.QRect(1830, 20, 71, 41))
        self.pushButton_go.setStyleSheet("font: 75 14pt \"微軟正黑體\";\n"
"color: rgb(0, 170, 0);")
        self.pushButton_go.setObjectName("pushButton_go")
        self.comboBox_ma = QtWidgets.QComboBox(Dialog)
        self.comboBox_ma.setGeometry(QtCore.QRect(1240, 20, 101, 41))
        self.comboBox_ma.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.comboBox_ma.setCurrentText("")
        self.comboBox_ma.setObjectName("comboBox_ma")
        self.checkBox_ema = QtWidgets.QCheckBox(Dialog)
        self.checkBox_ema.setGeometry(QtCore.QRect(1360, 20, 91, 41))
        self.checkBox_ema.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.checkBox_ema.setObjectName("checkBox_ema")
        self.comboBox_technical_index_1 = QtWidgets.QComboBox(Dialog)
        self.comboBox_technical_index_1.setGeometry(QtCore.QRect(1570, 20, 111, 41))
        self.comboBox_technical_index_1.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.comboBox_technical_index_1.setCurrentText("")
        self.comboBox_technical_index_1.setObjectName("comboBox_technical_index_1")
        self.comboBox_technical_index_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_technical_index_2.setGeometry(QtCore.QRect(1700, 20, 111, 41))
        self.comboBox_technical_index_2.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.comboBox_technical_index_2.setCurrentText("")
        self.comboBox_technical_index_2.setObjectName("comboBox_technical_index_2")
        self.checkBox_BBANDS = QtWidgets.QCheckBox(Dialog)
        self.checkBox_BBANDS.setGeometry(QtCore.QRect(1450, 20, 111, 41))
        self.checkBox_BBANDS.setStyleSheet("font: 75 12pt \"微軟正黑體\";")
        self.checkBox_BBANDS.setObjectName("checkBox_BBANDS")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "my_stock_app"))
        self.label_start.setText(_translate("Dialog", "-- START --"))
        self.pushButton_login.setText(_translate("Dialog", "LOGIN"))
        self.label_stock.setText(_translate("Dialog", "股票代號/名稱 ："))
        self.pushButton_search.setText(_translate("Dialog", "查詢"))
        self.label_stock_mode.setText(_translate("Dialog", "功能模式 ："))
        self.radioButton_mode_search.setText(_translate("Dialog", "查詢模式"))
        self.radioButton_mode_select.setText(_translate("Dialog", "選股模式"))
        self.radioButton_mode_test.setText(_translate("Dialog", "回測模式"))
        self.label_market_index.setText(_translate("Dialog", "大盤指數 ："))
        self.radioButton_twse_index.setText(_translate("Dialog", "加權指數"))
        self.radioButton_otc_index.setText(_translate("Dialog", "櫃買指數"))
        self.radioButton_future_index.setText(_translate("Dialog", "台指近月"))
        self.label_search_result.setText(_translate("Dialog", "name"))
        self.radioButton_market.setText(_translate("Dialog", "大盤"))
        self.radioButton_stock.setText(_translate("Dialog", "個股"))
        self.label_target.setText(_translate("Dialog", "大盤 / 類股 ："))
        self.label_search_result_2.setText(_translate("Dialog", "today_price"))
        self.checkBox_corporation.setText(_translate("Dialog", "三大法人"))
        self.pushButton_update.setText(_translate("Dialog", "更新"))
        self.label_date_to_date.setText(_translate("Dialog", "～"))
        self.dateEdit_start.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.dateEdit_end.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.pushButton_go.setText(_translate("Dialog", "GO"))
        self.checkBox_ema.setText(_translate("Dialog", "EMA"))
        self.checkBox_BBANDS.setText(_translate("Dialog", "BBANDS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
