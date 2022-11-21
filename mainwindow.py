# This Python file uses the following encoding: utf-8
import sys,datetime,time
import pandas as pd
#import figureCanvas
import stockInformation,worldIndex,drawTimeShare,drawCandle,globalVariable,getDate,tableStock,baseInformation
import threadRealTime,threadDealTimeShare,threadNewsReport,threadGetCandle,threadTable,threadIndex
from PySide6.QtWidgets import QRadioButton,QMenu,QTextEdit,QApplication,QDateTimeEdit,QMainWindow,QMessageBox,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QComboBox
from PySide6.QtGui import QColor,QTextCharFormat,QTextCursor,QFont,QIcon,QAction,QCursor
from PySide6.QtCore import QThread,Qt,QTimer,QDateTime,QTime,QSettings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Stock')
        self.setWindowIcon(QIcon('logo.ico'))
        self.showMaximized()

        #变量初始化，类实例化
        self.init()
        #子线程初始化
        self.thread_init()
        #布局初始化
        self.main_layout_init()
        #信号槽初始化
        self.signal_slot()

    def init(self):
        self.cur_item=0
        self.my_cur_item=0
        self.rising_speed=0
        self.time_interval=500
        self.time_count=20
        self.time_share_data=''
        self.isclicked=False
        self.stock_code='600519'
        self.pre_code=self.stock_code
        self.name='贵州茅台'
        self.industry='白酒'
        self.pageDownNum=0
        self.preVerticalScrollBar=0
        self.isVerticalScrollBar=True
        self.price=[]
        self.price_len=[]
        self.flag_direction=[]
        self.flag_pos=[]
        self.line_len=[]
        #self.text_count=14
        self.pre_close=1
        self.now_close=1
        self.high_low_point=[0]*5
        self.adjustflag='0'
        self.period='101'
        self.find_first_row=0
        self.find_num=0
        self.time_share_chart_data=pd.DataFrame(columns=['Time','price','vol','direct','ave_price'])
        self.isF10=False
        self.isAsia=True
        self.freq='daily'
        self.isFlashBoard=False
        self.isNewsReportStop=True
        self.isHotKey=False
        self.whichDay=0
        self.fmt=QTextCharFormat()
        self.text1=''
        self.text=''
        self.isOpenNewsReport=True
        self.isBoard=False

        self.isThreadRealTimeRunning=False
        self.isThreadTimeShareRunning=False
        globalVariable._init()
        globalVariable.setValue(1)
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.downloadInfoTime=self.settings.value("General/curTime")

        self.data=getDate.GetData(self.stock_code,self.period,self.adjustflag)
        self.download_info=stockInformation.StockInformation()
        self.draw_time_share=drawTimeShare.DrawChart(self.high_low_point,self.time_share_chart_data)
        self.draw_candle=drawCandle.DrawChart(self.data.data)
        self.tableView=tableStock.TableStock()
        self.tableView.view.setFocusPolicy(Qt.NoFocus)
        self.tableView.view_rising_speed.setFocusPolicy(Qt.NoFocus)
        self.tableView.view_my_stock.setFocusPolicy(Qt.NoFocus)
        self.baseInformation=baseInformation.BaseInformation(self.stock_code,self.name,self.ui.statusbar)

    def main_layout_init(self):
        main_layout=QHBoxLayout()
        main_layout.setContentsMargins(2,0,0,0)
        main_layout.setSpacing(0)

        self.ui.frame.setLayout(main_layout)
        self.main2=QWidget()

        self.main2.setMaximumSize(520,946)
        self.tableView.view_rising_speed.setMinimumSize(520,530)
        self.tableView.view_my_stock.setMinimumSize(520,416)
        main_layout2=QVBoxLayout()
        main_layout2.setContentsMargins(0,0,0,0)
        main_layout2.setSpacing(0)
        self.main2.setLayout(main_layout2)

        #右侧布局
        self.right_widget=QWidget()
        self.right_widget.setMaximumSize(450,946)
        right_layout=QVBoxLayout()
        right_layout.setContentsMargins(0,0,0,0)
        right_layout.setSpacing(0)
        self.right_widget.setLayout(right_layout)

        self.freq_widget=QWidget()
        self.adjust_widget=QWidget()

        freq_layout=QHBoxLayout()
        freq_layout.setSpacing(0)
        adjust_layout=QHBoxLayout()
        adjust_layout.setSpacing(0)
        self.freq_widget.setLayout(freq_layout)
        self.adjust_widget.setLayout(adjust_layout)
        self.daily=QRadioButton('日线')
        self.daily.setChecked(True)
        self.weekly=QRadioButton('周线')
        self.monthly=QRadioButton('月线')
        self.no_adjust=QRadioButton('不复权')
        self.no_adjust.setChecked(True)
        self.split_adjusted=QRadioButton('前复权')
        self.back_adjusted=QRadioButton('后复权')
        freq_layout.addWidget(self.daily)
        freq_layout.addWidget(self.weekly)
        freq_layout.addWidget(self.monthly)
        adjust_layout.addWidget(self.no_adjust)
        adjust_layout.addWidget(self.split_adjusted)
        adjust_layout.addWidget(self.back_adjusted)

        self.second_widget=QWidget()
        self.navigation_widget=QWidget()
        self.second_widget.setWindowFlag(Qt.Popup)
        self.second_widget.move(200,100)
        self.second_widget.setMinimumSize(600,400)
        second_layout=QHBoxLayout()
        second_layout.setSpacing(0)
        navigation_layout=QVBoxLayout()
        navigation_layout.setSpacing(0)
        self.navigation_widget.setLayout(navigation_layout)
        self.second_widget.setLayout(second_layout)
        self.hot_key=QPushButton('热度关键词')
        self.business_analysis=QPushButton('经营分析')
        self.main_index=QPushButton('主要指标')
        self.asset_liability=QPushButton('资产负债表')
        self.Income=QPushButton('利润表')
        self.cash_flow=QPushButton('现金流量表')
        navigation_layout.addWidget(self.hot_key)
        navigation_layout.addWidget(self.main_index)
        navigation_layout.addWidget(self.business_analysis)
        navigation_layout.addWidget(self.asset_liability)
        navigation_layout.addWidget(self.Income)
        navigation_layout.addWidget(self.cash_flow)
        second_layout.addWidget(self.navigation_widget)
        second_layout.addWidget(self.tableView.view2)
        #查询小窗口
        self.find_small_window=QWidget()
        self.code_text=QLineEdit('')
        self.code_text.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.find_small_window.setWindowFlag(Qt.Popup)
        self.find_small_window.setGeometry(1465,627,300,370)
        find_window_layout=QVBoxLayout()
        find_window_layout.setContentsMargins(2,2,2,2)
        find_window_layout.setSpacing(0)
        self.find_small_window.setLayout(find_window_layout)
        find_window_layout.addWidget(self.code_text)
        self.find_text_list=QTextEdit()
        self.find_small_window.setLayout(find_window_layout)
        self.find_text_list.setReadOnly(True)
        find_window_layout.addWidget(self.find_text_list)

        #提示小窗口
        self.prompt_window=QWidget()
        self.prompt_text=QTextEdit()
        self.prompt_text.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.prompt_window.setWindowFlag(Qt.Popup)
        self.prompt_window.setGeometry(850,400,300,200)
        prompt_window_layout=QVBoxLayout()
        self.prompt_window.setLayout(prompt_window_layout)
        self.prompt_text.setReadOnly(True)
        prompt_window_layout.addWidget(self.prompt_text)

        self.right_widget_four=QWidget()
        right_layout_four=QVBoxLayout()
        self.right_widget_four.setLayout(right_layout_four)
        self.period_text=QComboBox()
        information=['即时','3日排行','5日排行','10日排行','20日排行']
        self.period_text.addItems(information)
        self.royalFlushPlateFlows=QPushButton('同花顺板块资金流')
        self.eastPlateFlows=QPushButton('东方财富板块资金流')
        self.newHigh_newLow=QPushButton('新高新低数量')
        self.stockHotRank=QPushButton('股票热度、淘股吧')
        self.dateEdit = QDateTimeEdit(self.curRecentMarketDay())

        self.yesterdayStrong=QPushButton('昨日强势股票')
        right_layout_four.addWidget(self.period_text)
        right_layout_four.addWidget(self.eastPlateFlows)
        right_layout_four.addWidget(self.royalFlushPlateFlows)
        right_layout_four.addWidget(self.newHigh_newLow)
        right_layout_four.addWidget(self.stockHotRank)
        right_layout_four.addWidget(self.yesterdayStrong)
        right_layout_four.addWidget(self.dateEdit)

        main_layout.addWidget(self.tableView.view,alignment=Qt.AlignTop)
        main_layout.addWidget(self.main2,alignment=Qt.AlignTop)

        main_layout2.addWidget(self.tableView.view_rising_speed)
        main_layout2.addWidget(self.tableView.view_my_stock)
        main_layout.addWidget(self.draw_candle.candle_widget)
        main_layout.addWidget(self.right_widget,alignment=Qt.AlignTop)
        main_layout.addWidget(self.right_widget_four)
        right_layout.addWidget(self.baseInformation.base_information_widget,alignment=Qt.AlignTop)
        right_layout.addWidget(self.baseInformation.time_share_widget,alignment=Qt.AlignTop)

        self.news_data=QTextEdit()
        self.baseInformation.time_share_tick.setReadOnly(True)

        self.news_data.setMaximumHeight(130)
        right_layout.addWidget(self.news_data)

        #self.right_layout.addWidget(self.code_text,alignment=Qt.AlignBottom)
        pushbuttom_layout=QHBoxLayout()
        right_layout.addLayout(pushbuttom_layout)
        pushbuttom_layout.addWidget(self.freq_widget)
        pushbuttom_layout.addWidget(self.adjust_widget)

        right_layout.addWidget(self.draw_time_share.time_share_widget,alignment=Qt.AlignTop)

        self.tableView.view.show()
        self.right_widget_four.hide()
        self.draw_candle.candle_widget.hide()

    def thread_init(self):
        self.thread = QThread()
        self.table_thread=threadTable.TableThread(self)
        self.table_thread.moveToThread(self.thread)
        self.table_thread._signal.connect(self.reflashTable)
        self.table_thread._signalErr.connect(self.errInfo)
        #self.table_thread._signal_draw.connect(self.draw_candle_chart)
        self.table_thread.start()
        #self.table_thread.finished.connect(self.table_thread.quit())

        self.worldIndex=worldIndex.WorldIndex()
        self.worldIndexData=self.worldIndex.getAllIndex()
        self.worldFuturesData=self.worldIndex.get_futures_data()
        #self.initLabel()

        self.thread2 = QThread()
        self.table_thread2=threadIndex.IndexThread(self)
        self.table_thread2.moveToThread(self.thread2)
        self.table_thread2.start()
        self.table_thread2.finished.connect(self.table_thread2.quit())

        self.thread3 = QThread()
        self.real_time_thread3=threadRealTime.RealTimeThread(self)
        self.real_time_thread3.moveToThread(self.thread3)
        #self.time_share_thread3.start()
        self.real_time_thread3.finished.connect(self.real_time_thread3.quit())
        self.real_time_thread3._signal.connect(self.flash_time_share_tick_data)

        self.thread4 = QThread()
        self.draw_time_share_thread4=threadDealTimeShare.DealTimeShareThread(self)
        self.draw_time_share_thread4.moveToThread(self.thread4)
        #self.draw_time_share_thread4.finished.connect(self.draw_time_share_thread4.quit())
        self.draw_time_share_thread4._signal.connect(self.draw_time_share_chart)

        self.thread5=QThread()
        self.news_report_thread5=threadNewsReport.NewsReport(self)
        self.news_report_thread5.moveToThread(self.thread5)
        #self.news_report_thread5.finished.connect(self.draw_time_share_thread4.quit())
        self.news_report_thread5._signal.connect(self.flash_news_report)

        self.thread6=QThread()
        self.get_candle_thread6=threadGetCandle.GetCandle(self)
        self.get_candle_thread6.moveToThread(self.thread6)
        #self.news_report_thread5.finished.connect(self.draw_time_share_thread4.quit())
        self.get_candle_thread6._signal.connect(self.draw_candle_chart)


    def signal_slot(self):
        #信号槽
        self.daily.clicked.connect(self.flag_init)
        self.weekly.clicked.connect(self.flag_init)
        self.monthly.clicked.connect(self.flag_init)
        self.no_adjust.clicked.connect(self.flag_init)
        self.split_adjusted.clicked.connect(self.flag_init)
        self.back_adjusted.clicked.connect(self.flag_init)
        self.tableView.view.doubleClicked.connect(self.double_clicked_stock_info)
        self.tableView.view_rising_speed.doubleClicked.connect(self.double_clicked_rising_speed_info)
        self.tableView.view_my_stock.doubleClicked.connect(self.double_clicked_my_stock_info)
        self.tableView.view2.doubleClicked.connect(self.double_clicked_stock_info2)
        self.tableView.view.clicked.connect(self.clicked_stock_item)
        self.tableView.view_rising_speed.clicked.connect(self.clicked_rising_speed_item)
        self.tableView.view_my_stock.clicked.connect(self.clicked_my_stock_item)
        self.tableView.view.horizontalHeader().sectionClicked.connect(self.horizontalHeader)
        #self.ui.download_d.triggered.connect(self.data.download_akshare_all_stock)
        self.ui.download_info.triggered.connect(self.download)
        self.ui.newsReport.triggered.connect(self.set_open_close_news_report)

        self.code_text.keyPressEvent=self.codeTextkeyPressEvent
        self.draw_candle._signal.connect(self.flash_old_candle_information)

        self.ui.zh_market.triggered.connect(self.setMarket)
        self.ui.us_market.triggered.connect(self.setMarket)
        self.ui.hk_market.triggered.connect(self.setMarket)
        self.ui.financial_flows.triggered.connect(self.financialFlows)
        self.royalFlushPlateFlows.clicked.connect(self.financialFlows)
        self.ui.pick_stocks.triggered.connect(self.tableView.pick_stocks)
        self.eastPlateFlows.clicked.connect(self.financialFlows)
        self.newHigh_newLow.clicked.connect(self.financialFlows)
        self.stockHotRank.clicked.connect(self.financialFlows)
        self.yesterdayStrong.clicked.connect(self.financialFlows)
        for i in range(9):
            self.baseInformation.createVar[f'self.index{i}'].clicked.connect(self.setIndex)

        self.tableView.view.verticalScrollBar().actionTriggered.connect(self.beforePageChanged)
        self.tableView.view.verticalScrollBar().valueChanged.connect(self.afterPageChanged)

        self.hot_key.clicked.connect(self.hot_keyword)
        self.business_analysis.clicked.connect(self.information)
        self.main_index.clicked.connect(self.information)
        self.asset_liability.clicked.connect(self.information)
        self.Income.clicked.connect(self.information)
        self.cash_flow.clicked.connect(self.information)
        self.ui.actF10.triggered.connect(self.information)
        self.ui.actF3.triggered.connect(self.hot_keyword)
        #鼠标右键
        self.tableView.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.view.customContextMenuRequested.connect(lambda:self.create_rightmenu1(1))
        self.tableView.view_rising_speed.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.view_rising_speed.customContextMenuRequested.connect(lambda:self.create_rightmenu1(2))
        self.tableView.view_my_stock.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.view_my_stock.customContextMenuRequested.connect(self.create_rightmenu2)

        sec = QTime.currentTime().second()
        msec= QTime.currentTime().msec()
        if sec%3==2 and msec>400:
            time.sleep(1)
        while(1):
            sec = QTime.currentTime().second()
            msec= QTime.currentTime().msec()
            if sec%3==2 and msec>400:
                break
        self.timer=QTimer()
        self.timer.timeout.connect(self.flashTableData)
        self.timer.start(self.time_interval)

    def draw_candle_chart(self):
        if len(self.data.data)!=0:
            self.draw_candle.init_idx(self.data.data)
            self.baseInformation.flash_base_information_find(len(self.data.data),self.stock_code,self.name,self.data.data)

    def flag_init(self):
        if self.stock_code[0:4]!='100.':
            if self.sender()==self.daily:
                self.period='101'
            elif self.sender()==self.weekly:
                self.period='102'
            elif self.sender()==self.monthly:
                self.period='103'
            elif self.sender()==self.no_adjust:
                self.adjustflag='0'
            elif self.sender()==self.split_adjusted:
                self.adjustflag='1'
            elif self.sender()==self.back_adjusted:
                self.adjustflag='2'
            if globalVariable.getValue()==3:
                self.find_init()
        else:
            if self.sender()==self.daily:
                self.period='101'
            elif self.sender()==self.weekly:
                self.period='102'
            elif self.sender()==self.monthly:
                self.period='103'
            if globalVariable.getValue()==3:
                self.data.get_other_index(self.stock_code,self.period)
                self.draw_candle_chart()

    #鼠标移动刷新基本信息，两个不同状态的刷新
    def flash_old_candle_information(self):
        self.baseInformation.flash_base_information_find(self.draw_candle.index+1,self.stock_code,self.name,self.data.data)
        if (globalVariable.marketNum==1 or globalVariable.marketNum==3) and self.stock_code[0:4]!='100.' and \
                self.stock_code[0:4]!='103.' and self.stock_code[0:4]!='104.':
            self.whichDay=len(self.draw_candle.data)-self.draw_candle.index-1
            if self.whichDay<5:
                self.draw_time_share_thread4.start()

    def flash_news_report(self):
        self.fmt.setForeground(QColor("red"))
        self.news_data.mergeCurrentCharFormat(self.fmt)
        self.news_data.append(self.text1)
        self.fmt.setForeground(QColor("black"))
        self.news_data.mergeCurrentCharFormat(self.fmt)
        self.news_data.append(self.text)
        self.news_data.moveCursor(QTextCursor.End)

    def flash_time_share_tick_data(self):
        #self.baseInformation.flash_time_share_tick_data(self.price,self.pre_close,self.line_len,self.price_len,self.flag_direction,self.flag_pos,self.time_share_data)
        self.isThreadRealTimeRunning=False
        self.baseInformation.time_share_tick.clear()
        if len(self.time_share_data)==0:
            return
        self.baseInformation.time_share_tick.setTextColor(QColor("black"))
        self.baseInformation.time_share_tick.setFontWeight(1)
        self.baseInformation.time_share_tick.append(self.time_share_data)
        self.baseInformation.time_share_tick.moveCursor(QTextCursor.End)
        fmt=QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        cursor=self.baseInformation.time_share_tick.textCursor()
        l=14
        if self.text_count<14:
            l=self.text_count
        for i in range(self.text_count-l,self.text_count):
                if self.price[i]<self.pre_close:
                    fmt.setForeground(QColor(0,191,0))
                elif self.price[i]>self.pre_close:
                    fmt.setForeground(QColor("red"))
                else:
                    fmt.setForeground(QColor("black"))
                cursor.setPosition(self.line_len[i]+12,QTextCursor.MoveAnchor);
                cursor.setPosition(self.line_len[i]+12+self.price_len[i],QTextCursor.KeepAnchor);
                cursor.mergeCharFormat(fmt)
                if self.flag_direction[i]==1:
                    fmt.setForeground(QColor(0,191,0))
                elif self.flag_direction[i]==2:
                    fmt.setForeground(QColor("red"))
                if self.flag_pos[i+1]==0:
                    continue
                cursor.setPosition(self.flag_pos[i+1],QTextCursor.MoveAnchor);
                cursor.setPosition(self.flag_pos[i+1]-1,QTextCursor.KeepAnchor);
                cursor.mergeCharFormat(fmt)

    def draw_time_share_chart(self):
        self.isThreadTimeShareRunning=False
        if len(self.time_share_chart_data)==0:
            return
        self.draw_time_share.init(self.high_low_point,self.time_share_chart_data)
    def errInfo(self):
        QMessageBox.information(self,"提示","东方只有即时、5日、10日",QMessageBox.Ok)

    #F10个股资料 F3热度关键词
    def information(self):
        self.isHotKey=False
        code=self.stock_code
        if(str(self.stock_code)[0] == '6'):
            code = f"SH{self.stock_code}"
        elif(str(self.stock_code)[0] in ['4','8']):
            code = f"BJ{self.stock_code}"
        elif(str(self.stock_code)[0] in ['0','3']):
            code = f"SZ{self.stock_code}"
        if self.ui.us_market.isChecked()==True or self.ui.hk_market.isChecked()==True:
            QMessageBox.information(self,"提示","只能查看中国股市",QMessageBox.Ok)
            return
        if self.sender()==self.business_analysis:
            self.tableView.get_main_business_com(code)
        elif self.sender()==self.main_index or self.isF10 or self.sender()==self.ui.actF10:
            self.isF10=False
            self.tableView.get_main_indicator(code)
        elif self.sender()==self.asset_liability:
            self.tableView.get_asset_liability(code)
        elif self.sender()==self.Income:
            self.tableView.get_Income(code)
        elif self.sender()==self.cash_flow:
            self.tableView.get_cash_flow(code)

        self.second_widget.setMinimumSize(1500,700)
        self.second_widget.setWindowTitle(code+self.name)
        self.tableView.reflashView2()
        self.second_widget.show()

    def hot_keyword(self):
        self.isHotKey=True
        if(str(self.stock_code)[0] == '6'):
            code = f"SH{self.stock_code}"
        elif(str(self.stock_code)[0] in ['4','8']):
            code = f"BJ{self.stock_code}"
        elif(str(self.stock_code)[0] in ['0','3']):
            code = f"SZ{self.stock_code}"
        if not self.ui.us_market.isChecked() and (not self.ui.hk_market.isChecked()):
            if code[0]=='S':
                self.tableView.get_stock_hot_keyword_em(code)
                self.second_widget.setMaximumSize(650,400)
            else:
                QMessageBox.information(self,"提示","只能查看沪深股市",QMessageBox.Ok)
                return
        else:
            QMessageBox.information(self,"提示","只能查看中国市场",QMessageBox.Ok)
            return
        self.second_widget.setWindowTitle(code+self.name)
        self.tableView.get_stock_hot_keyword_em(code)
        self.tableView.reflashView2()

        self.second_widget.show()

    #3个市场切换
    def setMarket(self):
        if self.sender()==self.ui.us_market:
            if self.ui.us_market.isChecked==True:
                return
            globalVariable.PreInterface=globalVariable.getValue()
            globalVariable.setValue(2)
            globalVariable.marketNum=2
            self.isAsia=False
            self.isclicked=True
            self.ui.zh_market.setChecked(False)
            self.ui.us_market.setChecked(True)
            self.ui.hk_market.setChecked(False)
            self.main2.hide()
        elif self.sender()==self.ui.zh_market:
            if self.ui.zh_market.isChecked==True:
                return
            globalVariable.PreInterface=globalVariable.getValue()
            globalVariable.setValue(1)
            globalVariable.marketNum=1
            self.isAsia=True
            self.isFlashBoard=False
            self.isclicked=True
            self.ui.us_market.setChecked(False)
            self.ui.zh_market.setChecked(True)
            self.ui.hk_market.setChecked(False)
            self.main2.show()
        elif self.sender()==self.ui.hk_market:
            if self.ui.hk_market.isChecked==True:
                return
            globalVariable.PreInterface=globalVariable.getValue()
            globalVariable.setValue(5)
            globalVariable.marketNum=5
            self.isAsia=True
            self.isclicked=True
            self.ui.us_market.setChecked(False)
            self.ui.zh_market.setChecked(False)
            self.ui.hk_market.setChecked(True)
            self.main2.hide()
        #print(globalVariable.getValue())
        self.baseInformation.code_label.setText(str(self.stock_code))
        self.baseInformation.name_label.setText(str(self.name))
        self.table_thread.start()
        self.table_thread2.start()
        self.draw_candle.candle_widget.hide()
        #self.graphicsView.hide()
        self.tableView.view.show()
        #self.tableView.setViewWidth()
        self.right_widget.show()

        self.right_widget_four.hide()

    #资金分析界面
    def financialFlows(self):
        self.ui.us_market.setChecked(False)
        self.ui.zh_market.setChecked(False)
        self.ui.hk_market.setChecked(False)
        self.draw_candle.candle_widget.hide()
        #self.graphicsView.hide()
        globalVariable.PreInterface=globalVariable.getValue()
        globalVariable.setValue(4)
        self.tableView.view.show()
        #self.tableView.setViewWidth()
        self.main2.hide()
        self.right_widget.hide()
        globalVariable.marketNum=3
        globalVariable.isBoardWidth=False
        self.dateEdit.setCurrentSection(QDateTimeEdit.DaySection)
        if self.sender()==self.ui.financial_flows:
            globalVariable.subCount=4
            self.isBoard=True
            self.table_thread.start()
        elif self.sender()==self.royalFlushPlateFlows:
            globalVariable.subCount=1
            self.isBoard=True
            self.table_thread.start()
        elif self.sender()==self.stockHotRank:
            globalVariable.subCount=2
            self.isBoard=False
            self.table_thread.start()
        elif self.sender()==self.yesterdayStrong:
            globalVariable.subCount=3
            self.isBoard=False
            self.table_thread.start()
        elif self.sender()==self.eastPlateFlows:
            globalVariable.subCount=4
            self.isBoard=True
            self.table_thread.start()
        elif self.sender()==self.newHigh_newLow:
            globalVariable.subCount=5
            self.isBoard=True
            self.table_thread.start()
        if globalVariable.marketNum==1:
            globalVariable.marketNum=3
            self.table_thread2.start()
        elif globalVariable.marketNum==2:
            globalVariable.marketNum=4
            self.table_thread2.start()
        elif globalVariable.marketNum==5:
            globalVariable.marketNum=6
            self.table_thread2.start()

        #self.stockAnalysis.view.show()
        self.right_widget_four.show()

    def setIndex(self):
        self.whichDay=0
        self.stock_code,self.name=self.baseInformation.setIndex(self.sender(),self.isAsia,self.worldIndexData)
        if self.stock_code[0:2]!='10':
            self.find()
            return
        self.draw_time_share_thread4.start()
        self.data.get_other_index(self.stock_code,self.period)
        self.draw_candle_chart()
        self.tableView.view.hide()
        self.main2.hide()
        self.draw_candle.candle_widget.show()
        self.draw_candle.candle_widget.setFocus()
        self.right_widget.show()
        self.right_widget_four.hide()
        globalVariable.PreInterface=globalVariable.getValue()
        globalVariable.setValue(3)

    def reflashTable(self):
        if globalVariable.getValue()!=3:
            self.tableView.reflashView()
            if globalVariable.getValue()==1:
                self.tableView.reflash_my_stock()
            self.tableView.view.setCurrentIndex(self.tableView.model.index(self.cur_item,0))
            self.tableView.view_rising_speed.setCurrentIndex(self.tableView.model_rising_speed.index(self.rising_speed,0))
            self.tableView.view_my_stock.setCurrentIndex(self.tableView.model_my_stock.index(self.my_cur_item,0))
            if self.isclicked:
                self.clicked_stock_item(self.item)
                self.isclicked=False

    #3大股市开市时间每5秒刷新一次数据
    def flashTableData(self):
        a=self.time_count%10
        if globalVariable.marketNum==1:
            if globalVariable.isZhMarketDay():
                if self.stock_code[0:4]!='100.' or self.stock_code[0:4]!='103.' or self.stock_code[0:4]!='104.':
                    if self.time_count%2==1:
                        self.isThreadRealTimeRunning=True
                        self.real_time_thread3.start()
                    if a==0:
                        self.isThreadTimeShareRunning=True
                        self.draw_time_share_thread4.start()
                        self.baseInformation.circle.setStyleSheet(globalVariable.circle_green_SheetStyle)
            else:
                if a==0:
                    self.baseInformation.circle.setStyleSheet(globalVariable.circle_red_SheetStyle)
                    t=str(datetime.datetime.now())
                    if not globalVariable.isWeekend() and t[0:10]>str(self.downloadInfoTime) and\
                                    ((t[11:16]>'08:30' and t[11:16]<'13:00') or t[11:16]>'15:05'):
                        self.download()
                        self.downloadInfoTime=t[0:10]
                        self.settings.setValue("General/curTime",self.downloadInfoTime)

        elif globalVariable.marketNum==5 and a==0:
            if globalVariable.isHKMarketDay():
                self.draw_time_share_thread4.start()
                self.baseInformation.circle.setStyleSheet(globalVariable.circle_green_SheetStyle)
            else:
                self.baseInformation.circle.setStyleSheet(globalVariable.circle_red_SheetStyle)
        elif globalVariable.marketNum==2 and a==0:
            if globalVariable.isUSMarketDay():
                self.draw_time_share_thread4.start()
                self.real_time_thread3.start()
                self.baseInformation.circle.setStyleSheet(globalVariable.circle_green_SheetStyle)
            else:
                self.baseInformation.circle.setStyleSheet(globalVariable.circle_red_SheetStyle)
        if ((globalVariable.getValue()==2 and globalVariable.isUSMarketDay()) \
                    or (globalVariable.getValue()==1 and globalVariable.isZhMarketDay()) \
                    or (globalVariable.getValue()==5 and globalVariable.isHKMarketDay()))\
                     and a==0:

            self.table_thread.start()
        if globalVariable.getValue()==3 and globalVariable.isZhMarketDay() and a==0 and \
            self.stock_code[0:4]!='100.' and self.stock_code[0:4]!='103.' and self.stock_code[0:4]!='104.':
            self.find()
        if not globalVariable.isWeekend() and a==0:
            self.table_thread2.start()
        if self.time_count==20:
            if self.isNewsReportStop:
                self.news_report_thread5.start()
            self.time_count=0
        self.time_count+=1

    ##另类的翻页功能，滚动条改变之前的数值
    def beforePageChanged(self):
        if self.isVerticalScrollBar==True:
            self.preVerticalScrollBar=self.tableView.view.verticalScrollBar().value()
    #滚动条改变之后的数值，根据差值设置翻页，设置当前选择项
    def afterPageChanged(self):
        if self.isVerticalScrollBar==True and globalVariable.getValue()!=3:
            self.backVerticalScrollBar=self.tableView.view.verticalScrollBar().value()
            if self.backVerticalScrollBar>self.preVerticalScrollBar:
                self.pageDownNum+=1
            elif self.backVerticalScrollBar<self.preVerticalScrollBar:
                self.pageDownNum-=1
            self.isVerticalScrollBar=False
        #print(self.pageDownNum,self.preVerticalScrollBar,self.backVerticalScrollBar)
            self.tableView.view.verticalScrollBar().setValue(self.pageDownNum*(self.tableView.view.verticalScrollBar().pageStep()-1))
            self.cur_item=self.cur_item%(self.tableView.view.verticalScrollBar().pageStep()-1)+self.pageDownNum*(self.tableView.view.verticalScrollBar().pageStep()-1)
            self.tableView.view.setCurrentIndex(self.tableView.model.index(self.cur_item,0))
        self.isVerticalScrollBar=True

    def mousePressEvent(self,event):
        if event.buttons () == Qt.RightButton:
            self.create_rightmenu1(3)

    #个股页面滚轮查询下一个上一个
    def wheelEvent(self,event):
        if globalVariable.getValue()==3:
            if event.angleDelta().y()>0:
                self.cur_item-=1
                if self.cur_item<0:
                    self.cur_item=0
                    return
            elif event.angleDelta().y()<0:
                self.cur_item+=1
                if self.cur_item>len(self.tableView.stock_data)-1:
                    self.cur_item=len(self.tableView.stock_data)-1
                    return
            self.stock_code=self.tableView.stock_data.iat[self.cur_item,0]
            self.name=self.tableView.stock_data.iat[self.cur_item,1]
            if globalVariable.marketNum==1 or globalVariable.marketNum==3:
                self.find_stock_name()
            #self.code_text.setText(self.stock_code)
            self.find()

    #点击表头排序
    def horizontalHeader(self,index):
        #表头排序初始化翻页开关，当前选择项为第一项，翻页基数值为0
        self.isVerticalScrollBar=False
        self.tableView.stock_sort(index)
        #self.tableView.view.horizontalHeader().setPalette(self.pered)
        self.cur_item=0
        self.pageDownNum=0
        self.tableView.view.setCurrentIndex(self.tableView.model.index(self.cur_item,0))
        self.isVerticalScrollBar=True

    #键盘事件 esc个股返回不同主界面，返回之前进入的主界面
    def alpha_find(self):
        self.find_data=pd.read_csv('list/abbreviation_list.csv',encoding='gbk',dtype={'symbol':str})
        self.find_text_list.clear()

        isEsc=False
        for row in range(len(self.find_data)):
            if self.find_data.loc[row,'abbreviation'][0:len(self.code_text.text())]==self.code_text.text():
                if self.find_data.loc[row,'symbol'][0:2]=='BK':
                    self.find_text_list.append(f"{format(self.find_data.loc[row,'abbreviation'], '<8')} {self.find_data.loc[row,'name']}({self.find_data.loc[row,'symbol']})-板块")
                elif self.find_data.loc[row,'symbol'][0:3]=='sh.' or \
                            self.find_data.loc[row,'symbol'][0:3]=='399':
                    self.find_text_list.append(f"{format(self.find_data.loc[row,'abbreviation'], '<8')} {self.find_data.loc[row,'name']}({self.find_data.loc[row,'symbol']})-指数")
                else:
                    self.find_text_list.append(f"{format(self.find_data.loc[row,'abbreviation'], '<8')} {self.find_data.loc[row,'name']}({self.find_data.loc[row,'symbol']})")
                self.row=self.row+1
                if self.row==1:
                    self.find_first_row=row
                isEsc=True
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=f"{self.find_data.loc[self.find_first_row,'name']}--({self.find_data.loc[self.find_first_row,'area']}){self.find_data.loc[self.find_first_row,'industry']}"
            else:
                isEsc=False
                if isEsc==False and self.row>0:
                    self.find_text_list.moveCursor(QTextCursor.Start)
                    self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                    self.find_num=0
                    self.fmt.setForeground(QColor("red"))
                    self.find_text_list.mergeCurrentCharFormat(self.fmt)
                    self.find_text_list.textCursor().insertText('>>>')
                    return
            if row==len(self.find_data)-1:
                self.find_text_list.moveCursor(QTextCursor.Start)
                self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                self.find_num=0
                self.fmt.setForeground(QColor("red"))
                self.find_text_list.mergeCurrentCharFormat(self.fmt)
                self.find_text_list.textCursor().insertText('>>>')

    def digit_find(self):
        self.find_data=pd.read_csv('list/stock_list.csv',encoding='gbk',dtype={'symbol':str})
        self.find_text_list.clear()
        isEsc=False
        for row in range(len(self.find_data)):
            if self.find_data.loc[row,'symbol'][0:len(self.code_text.text())]==self.code_text.text():
                self.find_text_list.append(f"{format(self.find_data.loc[row,'symbol'], '<15')}{self.find_data.loc[row,'name']}")
                self.row=self.row+1
                if self.row==1:
                    self.find_first_row=row
                isEsc=True
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=f"{self.find_data.loc[self.find_first_row,'name']}--({self.find_data.loc[self.find_first_row,'area']}){self.find_data.loc[self.find_first_row,'industry']}"
            else:
                isEsc=False
                if isEsc==False and self.row>0:
                    self.find_text_list.moveCursor(QTextCursor.Start)
                    self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                    self.find_num=0
                    self.fmt.setForeground(QColor("red"))
                    self.find_text_list.mergeCurrentCharFormat(self.fmt)
                    self.find_text_list.textCursor().insertText('>>>')
                    return
            if row==len(self.find_data)-1:
                self.find_text_list.moveCursor(QTextCursor.Start)
                self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                self.find_num=0
                self.fmt.setForeground(QColor("red"))
                self.find_text_list.mergeCurrentCharFormat(self.fmt)
                self.find_text_list.textCursor().insertText('>>>')

    def index_find(self):
        self.find_data=pd.read_csv('list/abbreviation_index_list.csv',encoding='gbk',dtype={'symbol':str})
        self.find_text_list.clear()

        isEsc=False
        for row in range(len(self.find_data)):
            if self.find_data.loc[row,'abbreviation'][0:len(self.code_text.text())-1]==self.code_text.text()[1:len(self.code_text.text())]:
                self.find_text_list.append(f"{format(self.find_data.loc[row,'abbreviation'], '<8')} {self.find_data.loc[row,'name']}({self.find_data.loc[row,'symbol']})")
                self.row=self.row+1
                if self.row==1:
                    self.find_first_row=row
                isEsc=True
                if self.find_data.loc[self.find_first_row,'symbol'][0:1]=='3':
                    self.find__code=self.find_data.loc[self.find_first_row,'symbol']
                else:
                    self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=self.find_data.loc[self.find_first_row,'name']
            else:
                isEsc=False
                if isEsc==False and self.row>0:
                    self.find_text_list.moveCursor(QTextCursor.Start)
                    self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                    self.find_num=0
                    self.fmt.setForeground(QColor("red"))
                    self.find_text_list.mergeCurrentCharFormat(self.fmt)
                    self.find_text_list.textCursor().insertText('>>>')
                    return
            if row==len(self.find_data)-1:
                self.find_text_list.moveCursor(QTextCursor.Start)
                self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                self.find_num=0
                self.fmt.setForeground(QColor("red"))
                self.find_text_list.mergeCurrentCharFormat(self.fmt)
                self.find_text_list.textCursor().insertText('>>>')

    def board_find(self):
        self.find_data=pd.read_csv('list/concept_industry_board.csv',encoding='gbk')
        self.find_text_list.clear()

        isEsc=False
        for row in range(len(self.find_data)):
            if self.find_data.loc[row,'abbreviation'][0:len(self.code_text.text())-1]==self.code_text.text()[1:len(self.code_text.text())]:
                self.find_text_list.append(f"{'{0:<20}'.format(self.find_data.loc[row,'abbreviation'])[0:20-len(self.find_data.loc[row,'abbreviation'])]}{self.find_data.loc[row,'name']}")
                self.row=self.row+1
                if self.row==1:
                    self.find_first_row=row
                isEsc=True
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=self.find_data.loc[self.find_first_row,'name']
            else:
                isEsc=False
                if isEsc==False and self.row>0:
                    self.find_text_list.moveCursor(QTextCursor.Start)
                    self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                    self.find_num=0
                    self.fmt.setForeground(QColor("red"))
                    self.find_text_list.mergeCurrentCharFormat(self.fmt)
                    self.find_text_list.textCursor().insertText('>>>')
                    return
            if row==len(self.find_data)-1:
                self.find_text_list.moveCursor(QTextCursor.Start)
                self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
                self.find_num=0
                self.fmt.setForeground(QColor("red"))
                self.find_text_list.mergeCurrentCharFormat(self.fmt)
                self.find_text_list.textCursor().insertText('>>>')
    def codeTextkeyPressEvent(self,e):
        key = e.key()
        #self.blockFormat = self.find_text_list.textCursor().blockFormat()
        self.blockFormat.setBackground(QColor(0,199,255))
        self.blockFormat.setForeground(QColor('black'))
        self.fmt.setForeground(QColor("black"))
        self.find_text_list.mergeCurrentCharFormat(self.fmt)
        #self.find_text_list.setFontWeight(QFont.Bold)
        if key >= 48 and key <= 57 or (key >=65 and key <=90):
            self.row=0
            self.code_text.setText(f"{self.code_text.text()}{e.text()}")
            if self.code_text.text()[0:1].isdigit():
                if len(self.code_text.text())<=3:
                    return
                self.digit_find()
            else:
                if self.code_text.text()[0:1]=='i':
                    self.index_find()
                elif self.code_text.text()[0:1]=='v':
                    self.board_find()
                else:
                    self.alpha_find()

        elif key==Qt.Key_Enter or key==Qt.Key_Return:
            self.find_num=0
            self.stock_code=self.find_code
            self.name=self.find_name
            self.find_init()

        elif key==Qt.Key_Escape:
            self.code_text.setText('')
            self.find_small_window.hide()

        elif key==Qt.Key_Backspace:
            self.row=0
            self.code_text.setText(self.code_text.text()[0:len(self.code_text.text())-1])
            if self.code_text.text()[0:1].isdigit():
                if len(self.code_text.text())<=3:
                    if len(self.code_text.text())==3:
                        self.find_text_list.clear()
                    return
                self.digit_find()
            else:
                if len(self.code_text.text())<1:
                    self.find_text_list.clear()
                    return
                if self.code_text.text()[0:1]=='i':
                    self.index_find()
                elif self.code_text.text()[0:1]=='v':
                    self.board_find()
                else:
                    self.alpha_find()

        elif key==Qt.Key_Down:
            self.find_num=self.find_num+1
            if self.find_num>self.row-1:
                self.find_num=self.row-1
                return
            self.find_first_row=self.find_first_row+1

            self.blockFormat.setBackground(QColor('white'))
            self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
            self.find_text_list.textCursor().deletePreviousChar()
            self.find_text_list.textCursor().deletePreviousChar()
            self.find_text_list.textCursor().deletePreviousChar()
            block=self.find_text_list.document().findBlockByNumber(self.find_num)
            self.find_text_list.setTextCursor(QTextCursor(block))
            self.fmt.setForeground(QColor("red"))
            self.find_text_list.mergeCurrentCharFormat(self.fmt)
            self.find_text_list.textCursor().insertText('>>>')
            self.blockFormat = self.find_text_list.textCursor().blockFormat()
            #self.find_text_list.setTextCursor(self.find_text_list.textCursor())
            self.blockFormat.setBackground(QColor(0,199,255))
            self.blockFormat.setForeground(QColor('red'))
            self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
            if self.code_text.text()[0:1]=='i':
                if self.code_text.text()[1:2]=='3':
                    self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                else:
                    self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=str(self.find_data.loc[self.find_first_row,'name'])
            elif self.code_text.text()[0:1]=='v':
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=self.find_data.loc[self.find_first_row,'name']
            else:
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=f"{self.find_data.loc[self.find_first_row,'name']}--({self.find_data.loc[self.find_first_row,'area']}){self.find_data.loc[self.find_first_row,'industry']}"

        elif key==Qt.Key_Up:
            self.find_num=self.find_num-1
            if self.find_num<0:
                self.find_num=0
                return
            self.find_first_row=self.find_first_row-1
            self.blockFormat = self.find_text_list.textCursor().blockFormat()
            self.blockFormat.setBackground(QColor('white'))
            self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
            self.find_text_list.textCursor().deletePreviousChar()
            self.find_text_list.textCursor().deletePreviousChar()
            self.find_text_list.textCursor().deletePreviousChar()
            block=self.find_text_list.document().findBlockByNumber(self.find_num)
            self.find_text_list.setTextCursor(QTextCursor(block))
            self.fmt.setForeground(QColor("red"))
            self.find_text_list.mergeCurrentCharFormat(self.fmt)
            self.find_text_list.textCursor().insertText('>>>')
            self.blockFormat = self.find_text_list.textCursor().blockFormat()
            self.blockFormat.setBackground(QColor(0,199,255))
            self.find_text_list.textCursor().setBlockFormat(self.blockFormat)
            if self.code_text.text()[0:1]=='i':
                if self.code_text.text()[1:2]=='3':
                    self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                else:
                    self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=str(self.find_data.loc[self.find_first_row,'name'])
            elif self.code_text.text()[0:1]=='v':
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=self.find_data.loc[self.find_first_row,'name']
            else:
                self.find_code=self.find_data.loc[self.find_first_row,'symbol']
                self.find_name=f"{self.find_data.loc[self.find_first_row,'name']}--({self.find_data.loc[self.find_first_row,'area']}){self.find_data.loc[self.find_first_row,'industry']}"

    def keyPressEvent(self, event):
        key = event.key()
        self.blockFormat = self.find_text_list.textCursor().blockFormat()
        self.blockFormat.setBackground(QColor(0,199,255))

        #self.find_text_list.setFontWeight(QFont.Bold)
        if key == Qt.Key_F10:
            self.isF10=True
            self.information()
        elif key==Qt.Key_F3:
            self.hot_keyword()

        elif key==Qt.Key_Enter or key==Qt.Key_Return:
            self.find_init()
        elif key==Qt.Key_PageDown:
            if globalVariable.getValue()==3:
                self.cur_item+=1
                if self.cur_item>len(self.tableView.stock_data)-1:
                    self.cur_item=len(self.tableView.stock_data)-1
                    return
                self.stock_code=self.tableView.stock_data.iat[self.cur_item,0]
                self.name=self.tableView.stock_data.iat[self.cur_item,1]
                if globalVariable.marketNum==1 or globalVariable.marketNum==3:
                    self.find_stock_name()
                #self.code_text.setText(self.stock_code)
                self.find()
        elif key==Qt.Key_PageUp:
            if globalVariable.getValue()==3:
                self.cur_item-=1
                if self.cur_item<0:
                    self.cur_item=0
                    return
                self.stock_code=self.tableView.stock_data.iat[self.cur_item,0]
                self.name=self.tableView.stock_data.iat[self.cur_item,1]
                if globalVariable.marketNum==1 or globalVariable.marketNum==3:
                    self.find_stock_name()
                #self.code_text.setText(self.stock_code)
                self.find()
        elif key >= 48 and key <= 57 or (key >=65 and key <=90) or key==42:
            if globalVariable.marketNum!=1 and globalVariable.marketNum!=3:
                return
            self.find_small_window.show()
            self.code_text.setText(event.text())
            self.find_text_list.clear()
            self.code_text.setFocus()
            self.row=0

            if not self.code_text.text()[0:1].isdigit():
                if self.code_text.text()[0:1]=='i':
                    self.index_find()
                elif self.code_text.text()[0:1]=='v':
                    self.board_find()
                else:
                    self.alpha_find()

        elif key==Qt.Key_Up:
            if globalVariable.getValue()==3:
                if len(self.draw_candle.data)<=120:
                    return
                self.draw_candle.idx_range=int(self.draw_candle.idx_range*0.8)
                if self.draw_candle.idx_range<50:
                    self.draw_candle.idx_range=50
                if self.draw_candle.idx_range>self.draw_candle.idx_start:
                    self.draw_candle.idx_range=self.draw_candle.idx_start
                self.draw_candle.init(self.data.data)
        elif key==Qt.Key_Down:
            if globalVariable.getValue()==3:
                if len(self.draw_candle.data)<=120:
                    return
                self.draw_candle.idx_range=int(self.draw_candle.idx_range*1.2)
                if self.draw_candle.idx_range>self.draw_candle.idx_start:
                    self.draw_candle.idx_range=self.draw_candle.idx_start
                if self.draw_candle.idx_start<len(self.draw_candle.data) and \
                                self.draw_candle.idx_range==self.draw_candle.idx_start:
                    self.draw_candle.idx_start=int(self.draw_candle.idx_start*1.2)
                    if self.draw_candle.idx_start>len(self.draw_candle.data):
                        self.draw_candle.idx_start=len(self.draw_candle.data)
                    self.draw_candle.idx_range=self.draw_candle.idx_start

                self.draw_candle.init(self.data.data)
        elif key==Qt.Key_Left:
            if globalVariable.getValue()==3:
                if len(self.draw_candle.data)<=120:
                    return
                self.draw_candle.idx_start=self.draw_candle.idx_start-self.draw_candle.idx_range//4
                if self.draw_candle.idx_start<self.draw_candle.idx_range:
                    self.draw_candle.idx_start=self.draw_candle.idx_range
                self.draw_candle.x_max=self.draw_candle.idx_start
                self.draw_candle.init(self.data.data)
        elif key==Qt.Key_Right:
            if globalVariable.getValue()==3:
                if len(self.draw_candle.data)<=120:
                    return
                self.draw_candle.idx_start=self.draw_candle.idx_start+self.draw_candle.idx_range//4
                if self.draw_candle.idx_start>len(self.draw_candle.data):
                    self.draw_candle.idx_start=len(self.draw_candle.data)
                self.draw_candle.x_max=self.draw_candle.idx_start
                self.draw_candle.init(self.data.data)
        elif key == Qt.Key_Escape:
            if globalVariable.PreInterface==4:
                if globalVariable.getValue()==3:
                    globalVariable.PreInterface=4
                    globalVariable.setValue(4)
                    #self.tableView.view.verticalScrollBar().setValue(self.cur_item-15)
                    self.tableView.view.setCurrentIndex(self.tableView.model.index(self.cur_item,0))

                    #self.draw_candle
                    self.draw_candle.candle_widget.hide()
                    #self.graphicsView.hide()
                    self.tableView.view.show()
                    self.right_widget.hide()
                    self.right_widget_four.show()

            elif globalVariable.getValue()==3:
                    #self.tableView.view.verticalScrollBar().setValue(self.cur_item-15)
                    globalVariable.PreInterface=globalVariable.getValue()
                    self.tableView.view.setCurrentIndex(self.tableView.model.index(self.cur_item,0))

                    self.draw_candle.candle_widget.hide()
                    #self.graphicsView.hide()
                    self.tableView.view.show()
                    self.right_widget.show()
                    self.right_widget_four.hide()
                    if self.ui.us_market.isChecked()==True:
                        globalVariable.setValue(2)
                    elif self.ui.zh_market.isChecked()==True:
                        globalVariable.setValue(1)
                        self.main2.show()
                    elif self.ui.hk_market.isChecked()==True:
                        globalVariable.setValue(5)

    def find_stock_name(self):
        stock=pd.read_csv('list/stock_list.csv',encoding='gbk',dtype={'symbol':str})
        n=len(stock)
        l=0
        r=n-1
        while l<=r:
            mid=(l+r)//2
            #print(stock.loc[mid].iloc[2])
            if stock.iat[mid,2]==self.stock_code:
                #self.stock_code=str(stock.loc[mid].iloc[0])
                if stock.iat[mid,2][0:1]=='4' or stock.iat[mid,2][0:1]=='8':
                    self.name=stock.iat[mid,3]
                else:
                    self.name=f"{stock.iat[mid,3]}--({stock.iat[mid,4]}){stock.iat[mid,5]}"
                return
            elif stock.iat[mid,2]>self.stock_code:
                r=mid-1
            else:
                l=mid+1

    def create_rightmenu1(self,param):
        #菜单对象
        self.stock_menu = QMenu(self)
        self.actionA = QAction(u'加入自选',self)#创建菜单选项对象
        self.stock_menu.addAction(self.actionA)#把动作A选项对象添加到菜单self.groupBox_menu上
        self.stock_menu.popup(QCursor.pos())#声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单 ,exec_,popup两个都可以
        self.actionA.triggered.connect(lambda:self.add_my_stock(param)) #将动作A触发时连接到槽函数

    def create_rightmenu2(self):
        #菜单对象
        self.stock_menu = QMenu(self)
        self.actionB = QAction(u'删除自选',self)#创建菜单选项对象
        #self.actionB.setShortcut('Del')#设置动作A的快捷键
        self.stock_menu.addAction(self.actionB)
        self.stock_menu.popup(QCursor.pos())#声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单 ,exec_,popup两个都可以，
        self.actionB.triggered.connect(self.del_my_stock)

    def add_my_stock(self,param):
        if param==3:
            for i in range(1,len(self.tableView.stock_data_copy)+1):
                if self.stock_code==self.tableView.stock_data_copy.loc[i,'代码']:
                    self.select_item=i-1
                    break
            for i in range(1,len(self.tableView.my_stock_data)+1):
                if self.tableView.my_stock_data.loc[i,'代码']==self.stock_code:
                    return
            self.tableView.my_stock_data.loc[len(self.tableView.my_stock_data)+1]=self.tableView.stock_data_copy.loc[self.select_item+1]
        elif param==1:
            for i in range(1,len(self.tableView.my_stock_data)+1):
                if self.tableView.my_stock_data.loc[i,'代码']==self.stock_code:
                    return
            if globalVariable.getValue()==4:
                w=0
                for i in range(1,len(self.tableView.stock_data_copy)+1):
                    if self.stock_code==self.tableView.stock_data_copy.loc[i,'代码']:
                        self.select_item=i-1
                        w=1
                        break
                if w==0:
                    return
                self.tableView.my_stock_data.loc[len(self.tableView.my_stock_data)+1]=self.tableView.stock_data_copy.loc[self.select_item+1]
            else:
                self.select_item=self.cur_item
                self.tableView.my_stock_data.loc[len(self.tableView.my_stock_data)+1]=self.tableView.stock_data.loc[self.select_item+1]
        elif param==2:
            for i in range(1,len(self.tableView.my_stock_data)+1):
                if self.tableView.my_stock_data.loc[i,'代码']==self.stock_code:
                    return
            self.tableView.my_stock_data.loc[len(self.tableView.my_stock_data)+1]=self.tableView.rising_speed_data.loc[self.rising_speed+1]
        self.tableView.my_stock_data.index = pd.RangeIndex(start=1, stop=len(self.tableView.my_stock_data)+1, step=1)
        self.tableView.reflash_my_stock()
        self.tableView.my_stock_data.to_csv('list/my_stock.csv',encoding='gbk')

    def del_my_stock(self):
        self.tableView.my_stock_data.drop(self.tableView.my_stock_data.index[[self.my_cur_item]],inplace=True)
        self.tableView.my_stock_data.index = pd.RangeIndex(start=1, stop=len(self.tableView.my_stock_data)+1, step=1)
        self.tableView.reflash_my_stock()
        self.tableView.my_stock_data.to_csv('list/my_stock.csv',encoding='gbk')

    #获取单击目标行，获取选择项的股票代码
    def clicked_stock_item(self,item):
        self.whichDay=0
        self.item=item

        #self.tableView.setStyleSheet('QTableView{gridline-color:red}')
        self.cur_item=item.row()
        if globalVariable.getValue()==4 and self.isBoard:
            self.stock_code=self.tableView.stock_data1.iat[self.cur_item,0]
        else:
            self.stock_code=self.tableView.stock_data.iat[self.cur_item,0]
            self.name=self.tableView.stock_data.iat[self.cur_item,1]
        self.stock_data=self.tableView.stock_data

        if globalVariable.getValue()==1:
            self.find_stock_name()
            self.baseInformation.flash_base_information_click(self.cur_item,self.stock_data,self.name)
            if self.isThreadTimeShareRunning:
                self.draw_time_share_thread4.wait()
            self.draw_time_share_thread4.start()
            if self.isThreadRealTimeRunning:
                self.real_time_thread3.wait()
            self.real_time_thread3.start()

        elif globalVariable.getValue()==2 or globalVariable.getValue()==5:
            self.draw_time_share_thread4.start()
            self.real_time_thread3.start()
            self.baseInformation.flash_base_information_click(self.cur_item,self.stock_data,self.name)
            self.baseInformation.base_info['self.Issued_Capital_data'].setText('')
            self.baseInformation.base_info['self.Negotiable_Capital_data'].setText('')
            self.baseInformation.base_info['self.total_captial_data'].setText(str(globalVariable.format_conversion(self.tableView.stock_data.iat[self.cur_item,8])))
            self.baseInformation.base_info['self.pe_static_data'].setText('')
            self.baseInformation.base_info['self.earnings_data'].setText('')

    def clicked_rising_speed_item(self,item):
        self.whichDay=0
        self.item=item
        self.rising_speed=item.row()
        self.stock_code=self.tableView.rising_speed_data.iat[self.rising_speed,0]
        self.name=self.tableView.rising_speed_data.iat[self.rising_speed,1]

        if self.isThreadTimeShareRunning:
            self.draw_time_share_thread4.wait()
        self.draw_time_share_thread4.start()
        if self.isThreadRealTimeRunning:
            self.real_time_thread3.wait()
        self.real_time_thread3.start()
        self.find_stock_name()
        self.stock_data=self.tableView.rising_speed_data
        self.baseInformation.flash_base_information_click(self.rising_speed,self.stock_data,self.name)

    def clicked_my_stock_item(self,item):
        self.whichDay=0
        self.item=item
        self.my_cur_item=item.row()
        self.stock_code=self.tableView.my_stock_data.iat[self.my_cur_item,0]
        self.baseInformation.code_label.setText(self.stock_code)
        self.find_stock_name()
        self.baseInformation.name_label.setText(self.name)
        if self.isThreadTimeShareRunning:
            self.draw_time_share_thread4.wait()
        self.draw_time_share_thread4.start()
        if self.isThreadRealTimeRunning:
            self.real_time_thread3.wait()
        self.real_time_thread3.start()

        self.stock_data=self.tableView.my_stock_data
        self.baseInformation.flash_base_information_click(self.my_cur_item,self.stock_data,self.name)

    def double_clicked_my_stock_info(self,item):
        self.whichDay=0
        self.item=item
        cur_item=item.row()
        self.stock_code=self.tableView.my_stock_data.iat[cur_item,0]
        self.find_init()

    def double_clicked_rising_speed_info(self,item):
        self.whichDay=0
        self.item=item
        cur_item=item.row()
        self.stock_code=self.tableView.rising_speed_data.iat[cur_item,0]

        self.find_init()
    #双击查询个股k线
    def double_clicked_stock_info(self,item):
        self.whichDay=0
        self.item=item
        self.cur_item=item.row()
        if (globalVariable.getValue()==4 and self.isBoard):
            self.stock_code=self.tableView.stock_data1.iat[self.cur_item,0]
            self.isBoard=False
        else:
            self.stock_code=self.tableView.stock_data.iat[self.cur_item,0]

        if globalVariable.getValue()==4:
            if globalVariable.subCount==1 or globalVariable.subCount==5:
                QMessageBox.information(self,"提示","只能查看东方板块个股",QMessageBox.Ok)
                return
        if self.ui.us_market.isChecked()==True or self.ui.hk_market.isChecked()==True:
            self.name=self.tableView.stock_data.iat[self.cur_item,1]
            self.industry=''
        if globalVariable.PreInterface==4 or globalVariable.getValue()==1:
            self.find_stock_name()
        if globalVariable.subCount==4:
            globalVariable.isBoardWidth=True
        self.find_init()

    def double_clicked_stock_info2(self,item):
        if self.isHotKey:
            self.stock_code=self.tableView.stock_data1.iat[item.row(),3]
            self.find_init()

    def find_init(self):
        self.find_small_window.hide()
        self.pre_code=self.stock_code
        if self.stock_code[0:2]=='BK':
            self.board_code=self.stock_code
            self.isFlashBoard=True
            globalVariable.subCount==4
            self.find_small_window.hide()
            self.tableView.get_industry_concept_board(self.stock_code)
            self.tableView.reflashView()
            self.stock_data=self.tableView.stock_data
            self.stock_code=self.stock_data.iat[0,0]
            self.draw_time_share_thread4.start()
            self.real_time_thread3.start()
            self.find_stock_name()
            self.baseInformation.flash_base_information_click(self.cur_item,self.stock_data,self.name)
            return
        if globalVariable.subCount==4:
            data=pd.read_csv('list/concept_industry_board.csv',encoding='gbk')
            for i in range(len(data)):
                if data.loc[i,'name']==self.stock_code:
                    self.tableView.get_industry_concept_board(data.loc[i,'symbol'])
                    self.tableView.reflashView()
                    return
        self.find()

    def find(self):
        self.tableView.view.hide()
        self.draw_candle.candle_widget.show()
        self.main2.hide()
        self.draw_candle.candle_widget.setFocus()
        #self.graphicsView.show()
        self.right_widget.show()
        self.right_widget_four.hide()
        globalVariable.PreInterface=globalVariable.getValue()
        globalVariable.setValue(3)

        self.whichDay=0
        self.draw_time_share_thread4.start()
        self.get_candle_thread6.start()
        if globalVariable.marketNum==1 or globalVariable.marketNum==3 or globalVariable.marketNum==2 or globalVariable.marketNum==4:
            self.real_time_thread3.start()

    def curRecentMarketDay(self):
        date=datetime.datetime.now()
        for i in range(15):
            time=date+datetime.timedelta(days=-i)
            if globalVariable.isMarketDay(time):
                break
        str=time.strftime("%Y%m%d %H:%M:%S")
        date=QDateTime.fromString(str, "yyyyMMdd hh:mm:ss").date()
        return date

    def set_open_close_news_report(self):
        self.isOpenNewsReport=not self.isOpenNewsReport
        self.ui.newsReport.setChecked(not self.isOpenNewsReport)

    def download(self):
        self.prompt_window.show()
        self.prompt_text.append('开始处理板块信息')
        self.download_info.deal_with_concept_industry()
        self.prompt_text.append('板块信息处理完毕')
        self.prompt_text.append('开始处理个股信息')
        self.download_info.deal_with_stock_list()
        self.prompt_text.append('个股信息处理完毕')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(12)
    app.setFont(font);
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
