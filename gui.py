from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QHeaderView, QMessageBox
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from ui import Ui_MainWindow  # 導入 Qt Designer 生成的 UI
import remain 
import sys
import re

# 設置全局變數
input_text = ""

def handle_button_click():
    remain.start_processing()

#錯誤訊息：找不到教授
def show_error_message1(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("錯誤")
    msg_box.setText(f"找不到教授 {message} 的歷史記錄")
    msg_box.exec()

#錯誤訊息：錯誤
def show_error_message2(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("錯誤")
    msg_box.setText(message)
    msg_box.exec()

# 創建主視窗
def init_gui():
   global ui
   app = QApplication(sys.argv)  # 初始化應用程序
   main_window = QMainWindow()

   # 使用 ui_main_window.py 中生成的 setupUi 函數來設置主視窗的 UI
   ui = Ui_MainWindow()
   ui.setupUi(main_window)
   
   # 設置按鈕的點擊事件
   ui.pushButton.clicked.connect(read_input)
   ui.pushButton.clicked.connect(handle_button_click)

   # 顯示主視窗
   main_window.show()

   # 啟動應用程序的事件循環
   sys.exit(app.exec())

# 讀取輸入框的內容
def read_input():
    global input_text
    input_text = ui.lineEdit.text()
        

# 將結果顯示在表格中
def display_result(result):
    # 將一維列表轉換為二維列表，每行包含兩個元素
    result_2d = [result[i:i+2] for i in range(0, len(result), 2)]
    for i in range(len(result_2d)):
        for j in range(len(result_2d[i])):
            result_2d[i][j] = str(result_2d[i][j]).strip('[\']')   # 去除['']

    num_rows = len(result_2d)
    num_cols = len(result_2d[0]) if result_2d else 0

    table = ui.tableWidget
    table.setRowCount(num_rows)
    table.setColumnCount(num_cols)
    font = table.font()
    font.setPointSize(12)
    table.setFont(font)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    # 輸出表格
    for i, row in enumerate(result_2d):
        for j, item in enumerate(row):
            table_item = QTableWidgetItem()
            table_item.setFlags(table_item.flags() | Qt.ItemFlag.ItemIsEditable)
            table_item.setText(str(item).replace('\n', '<br>'))
            table.setItem(i, j, table_item)


# 調用 init_gui() 函數
init_gui()