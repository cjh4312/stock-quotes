# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtWidgets import QWidget,QGridLayout,QLabel,QFrame,QTextEdit,QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QTextCharFormat,QTextCursor,QFont
import globalVariable

class BaseInformation():
    def __init__(self,parent):
        self.parent=parent
        super().__init__()
        self.isKC=False
        self.base_information(self.parent.stock_code,self.parent.name)
        self.buy_sell_information()
        self.initLabel(self.parent.ui.statusbar)
        self.text_count=14

    def base_information(self,code,name):
        #基本信息显示初始化
        self.base_information_widget=QWidget()
        #self.base_information_widget.setMaximumHeight(150)
        base_information_layout=QGridLayout()
        base_information_layout.setSpacing(2)
        base_information_layout.setContentsMargins(10,0,0,0)
        self.base_information_widget.setLayout(base_information_layout)
        self.code_label=QLabel(code)
        self.name_label=QLabel(name)
        self.code_label.setStyleSheet("QLabel{font:bold;color:blue}")
        self.name_label.setStyleSheet("QLabel{font:bold 26px;font-family:微软雅黑;color:red}")
        base_information_layout.addWidget(self.code_label,0,0,2,1)
        base_information_layout.addWidget(self.name_label,0,1,2,3)

        self.base_info=locals()
        base_info_name=['现价','涨幅','换手','成交额','总股本','总市值','PE(静)','A股上涨',
                    '今开','最高','最低','成交量(手)','流通股','','PE(动)','A股下跌']
        base_info_var=['self.now_price','self.pctChg','self.turn','self.amount','self.Issued_Capital',\
                'self.total_captial','self.pe_static','rise','self.open','self.high','self.low',\
                'self.volume','self.Negotiable_Capital','self.earnings','self.pe','self.fall']
        base_info_data_var=['self.now_price_data','self.pctChg_data','self.turn_data','self.amount_data',\
                'self.Issued_Capital_data','self.total_captial_data','self.pe_static_data',\
                'self.rise_data','self.open_data','self.high_data','self.low_data','self.volume_data',\
                'self.Negotiable_Capital_data','self.earnings_data','self.pe_data','self.fall_data']
        for i in range(16):
            self.base_info[base_info_var[i]]=QLabel(base_info_name[i])
            #self.base_info[base_info_var[i]].setMaximumHeight(20)
            self.base_info[base_info_var[i]].setStyleSheet("QLabel{font:bold;font-family:微软雅黑}")
            self.base_info[base_info_data_var[i]]=QLabel()
            #self.base_info[base_info_data_var[i]].setMaximumHeight(20)

            if (i>=2 and i<=6) or (i>=11 and i<=14):
                self.base_info[base_info_data_var[i]].setStyleSheet("QLabel{font:bold 14px;color:blue}")
            elif i==7:
                self.base_info[base_info_data_var[i]].setStyleSheet("QLabel{font:bold 14px;color:red}")
            elif i==15:
                self.base_info[base_info_data_var[i]].setStyleSheet("QLabel{font:bold 14px;color:green}")
            else:
                self.base_info[base_info_data_var[i]].setStyleSheet("QLabel{font:bold 14px}")
            if i<8:
                base_information_layout.addWidget(self.base_info[base_info_var[i]],i+2,0)
                base_information_layout.addWidget(self.base_info[base_info_data_var[i]],i+2,1)
            else:
                base_information_layout.addWidget(self.base_info[base_info_var[i]],i-6,2)
                base_information_layout.addWidget(self.base_info[base_info_data_var[i]],i-6,3)

    def flash_base_information_click(self,cur_item,data,name):
        #now_close=data.iat[cur_item,2]
        pre_close=data.iat[cur_item,16]
        self.code_label.setText(str(data.iat[cur_item,0]))
        self.name_label.setText(name)
        if data.iat[cur_item,3]<0:
            self.base_info['self.now_price_data'].setPalette(globalVariable.pegreen)
            self.base_info['self.pctChg_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.now_price_data'].setPalette(globalVariable.pered)
            self.base_info['self.pctChg_data'].setPalette(globalVariable.pered)
        self.base_info['self.now_price_data'].setText(str(data.iat[cur_item,2]))
        self.base_info['self.pctChg_data'].setText(f"{data.iat[cur_item,3]}%")
        if data.iat[cur_item,13]<pre_close:
            self.base_info['self.high_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.high_data'].setPalette(globalVariable.pered)
        self.base_info['self.high_data'].setText(f"{data.iat[cur_item,13]}({round((data.iat[cur_item,13]-pre_close)*100/pre_close,2)}%)")
        if data.iat[cur_item,14]<pre_close:
            self.base_info['self.low_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.low_data'].setPalette(globalVariable.pered)
        self.base_info['self.low_data'].setText(f"{data.iat[cur_item,14]}({round((data.iat[cur_item,14]-pre_close)*100/pre_close,2)}%)")
        if data.iat[cur_item,15]<pre_close:
            self.base_info['self.open_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.open_data'].setPalette(globalVariable.pered)
        self.base_info['self.open_data'].setText(f"{data.iat[cur_item,15]}({round((data.iat[cur_item,15]-pre_close)*100/pre_close,2)}%)")

        self.base_info['self.volume_data'].setText(globalVariable.format_conversion(data.iat[cur_item,12]))
        self.base_info['self.amount_data'].setText(globalVariable.format_conversion(data.iat[cur_item,5]))
        self.base_info['self.turn_data'].setText(f"{data.iat[cur_item,4]}%")
        self.base_info['self.pe_data'].setText(str(data.iat[cur_item,7]))

    def buy_sell_information(self):
        A={1:'一',2:'二',3:'三',4:'四',5:'五'}
        self.time_share_widget=QWidget()
        self.time_share_widget.setMaximumHeight(250)
        time_share_layout=QGridLayout()
        self.time_share_widget.setLayout(time_share_layout)
        self.buy_sell_Var=locals()
        for i in range(1,6):
            self.buy_sell_Var[f"self.sell{i}"]=QLabel(f'卖{A[i]}')
            self.buy_sell_Var[f'self.sell{i}'].setStyleSheet("QLabel{font:bold;color:black;font-family:微软雅黑}")
            self.buy_sell_Var[f'self.sell_price{i}']=QLabel()
            self.buy_sell_Var[f'self.sell_num{i}']=QLabel()
            self.buy_sell_Var[f'self.sell_num{i}'].setAlignment(Qt.AlignRight)
            self.buy_sell_Var[f'self.buy{i}']=QLabel('买'+A[i])
            self.buy_sell_Var[f'self.buy{i}'].setStyleSheet("QLabel{font:bold;color:blue;font-family:微软雅黑}")
            self.buy_sell_Var[f'self.buy_price{i}']=QLabel()
            self.buy_sell_Var[f'self.buy_num{i}']=QLabel()
            self.buy_sell_Var[f'self.buy_num{i}'].setAlignment(Qt.AlignRight)
        self.buy_sell_Var['self.sell5'].setMaximumWidth(30)

        self.time_share_tick=QTextEdit()
        self.time_share_tick.setMinimumHeight(240)
        self.time_share_tick.setMinimumWidth(300)
        self.time_share_tick.setReadOnly(True)
        h_line=QFrame()
        h_line.setStyleSheet("QFrame{background:yellow;min-height:0px}")
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        for i in range(0,5):
            time_share_layout.addWidget(self.buy_sell_Var[f'self.sell{5-i}'],i,0)
            time_share_layout.addWidget(self.buy_sell_Var[f'self.sell_price{5-i}'],i,1)
            time_share_layout.addWidget(self.buy_sell_Var[f'self.sell_num{5-i}'],i,2)
            time_share_layout.addWidget(self.buy_sell_Var[f'self.buy{i+1}'],6+i,0)
            time_share_layout.addWidget(self.buy_sell_Var[f'self.buy_price{i+1}'],6+i,1)
            time_share_layout.addWidget(self.buy_sell_Var[f'self.buy_num{i+1}'],6+i,2)
        time_share_layout.addWidget(h_line,5,0,1,3)
        time_share_layout.addWidget(self.time_share_tick,0,3)
        #time_share_layout.addWidget(self.tableView.view3,0,3,10,3)

    def flash_base_information_find(self,data_len,code,name,data):
        self.code_label.setText(code)
        self.name_label.setText(name)
        pre_close=data.loc[data_len-1,'close']-data.loc[data_len-1,'pctVal']
        if data.loc[data_len-1,'pctChg']<0:
            self.base_info['self.pctChg_data'].setPalette(globalVariable.pegreen)
            self.base_info['self.now_price_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.pctChg_data'].setPalette(globalVariable.pered)
            self.base_info['self.now_price_data'].setPalette(globalVariable.pered)
        self.base_info['self.pctChg_data'].setText(f"{data.loc[data_len-1,'pctChg']}%")
        self.base_info['self.now_price_data'].setText(str(data.loc[data_len-1,'close']))
        if data.loc[data_len-1,'high']<pre_close:
            self.base_info['self.high_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.high_data'].setPalette(globalVariable.pered)
        self.base_info['self.high_data'].setText(f"{data.loc[data_len-1,'high']}({round((data.loc[data_len-1,'high']-pre_close)*100/pre_close,2)}%)")
        if data.loc[data_len-1,'low']<pre_close:
            self.base_info['self.low_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.low_data'].setPalette(globalVariable.pered)
        self.base_info['self.low_data'].setText(f"{data.loc[data_len-1,'low']}({round((data.loc[data_len-1,'low']-pre_close)*100/pre_close,2)}%)")
        if data.loc[data_len-1,'open']<pre_close:
            self.base_info['self.open_data'].setPalette(globalVariable.pegreen)
        else:
            self.base_info['self.open_data'].setPalette(globalVariable.pered)
        self.base_info['self.open_data'].setText(f"{data.loc[data_len-1,'open']}({round((data.loc[data_len-1,'open']-pre_close)*100/pre_close,2)}%)")
        self.base_info['self.volume_data'].setText(globalVariable.format_conversion(data.loc[data_len-1,'volume']))
        self.base_info['self.amount_data'].setText(globalVariable.format_conversion(data.loc[data_len-1,'amount']))
        if globalVariable.getValue()==2 or globalVariable.getValue()==5:
            self.base_info['self.turn_data'].setText('')
            self.base_info['self.pe_data'].setText('')
            return
        self.base_info['self.turn_data'].setText(f"{data.loc[data_len-1,'turn']}%")

    def flash_time_share_tick_data(self,price,pre_close,line_len,price_len,flag_direction,flag_pos,time_share_data):
        self.isThreadRealTimeRunning=False
        self.time_share_tick.clear()
        if len(time_share_data)==0:
            return
        self.time_share_tick.setTextColor(QColor("black"))
        self.time_share_tick.setFontWeight(1)
        self.time_share_tick.append(time_share_data)
        self.time_share_tick.moveCursor(QTextCursor.End)
        fmt=QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        cursor=self.time_share_tick.textCursor()
        l=14
        if self.text_count<14:
            l=self.text_count
        for i in range(self.text_count-l,self.text_count):
                if price[i]<pre_close:
                    fmt.setForeground(QColor(0,191,0))
                elif price[i]>pre_close:
                    fmt.setForeground(QColor("red"))
                else:
                    fmt.setForeground(QColor("black"))
                cursor.setPosition(line_len[i]+12,QTextCursor.MoveAnchor);
                cursor.setPosition(line_len[i]+12+price_len[i],QTextCursor.KeepAnchor);
                cursor.mergeCharFormat(fmt)
                if flag_direction[i]==1:
                    fmt.setForeground(QColor(0,191,0))
                elif flag_direction[i]==2:
                    fmt.setForeground(QColor("red"))
                if flag_pos[i+1]==0:
                    continue
                cursor.setPosition(flag_pos[i+1],QTextCursor.MoveAnchor);
                cursor.setPosition(flag_pos[i+1]-1,QTextCursor.KeepAnchor);
                cursor.mergeCharFormat(fmt)

    def setIndex(self,sender,isAsia,worldIndexData):
        self.base_info['self.Issued_Capital_data'].setText('')
        self.base_info['self.Negotiable_Capital_data'].setText('')
        self.base_info['self.total_captial_data'].setText('')
        self.base_info['self.pe_data'].setText('')
        self.base_info['self.pe_static_data'].setText('')
        self.base_info['self.earnings_data'].setText('')
        for i in range(0,10,2):
            self.buy_sell_Var[f'self.sell_price{5-i//2}'].setText('')
            self.buy_sell_Var[f'self.sell_num{5-i//2}'].setText('')
            self.buy_sell_Var[f'self.buy_price{5-i//2}'].setText('')
            self.buy_sell_Var[f'self.buy_num{5-i//2}'].setText('')
        if isAsia:
            for i in range(3):
                if sender==self.createVar[f'self.index{i}']:
                    if i==2:
                        if self.createVar['self.index2'].text()==worldIndexData.loc[i,'f14']:
                            stock_code=worldIndexData.loc[i,'f12']
                            name=worldIndexData.loc[i,'f14']
                        else:
                            stock_code=worldIndexData.loc[16,'f12']
                            name=worldIndexData.loc[16,'f14']
                    else:
                        stock_code=worldIndexData.loc[i,'f12']
                        name=worldIndexData.loc[i,'f14']
                    return stock_code,name

            for i in range(3,8):
                if sender==self.createVar[f'self.index{i}']:
                    stock_code=worldIndexData.loc[i,'f12']
                    name=worldIndexData.loc[i,'f14']
                    break
        else:
            for i in range(8):
                if sender==self.createVar[f'self.index{i}']:
                    stock_code=worldIndexData.loc[i+8,'f12']
                    name=worldIndexData.loc[i+8,'f14']
                    break
        if sender==self.createVar[f'self.index{8}']:
            if self.createVar[f'self.index{8}'].text()=='小型道指':
                stock_code='103.YM00Y'
                name='小型道指当月连续'
            elif self.createVar[f'self.index{8}'].text()=='A50期指':
                stock_code='104.CN00Y'
                name='A50期指当月连续'
        self.time_share_tick.clear()
        self.code_label.setText(stock_code)
        self.name_label.setText(name)
        return stock_code,name

    def initLabel(self,statusbar):
        self.createVar=locals()
        self.circle=QLabel()
        if globalVariable.isZhMarketDay():
            self.circle.setStyleSheet(globalVariable.circle_green_SheetStyle)
        else:
            self.circle.setStyleSheet(globalVariable.circle_red_SheetStyle)
        statusbar.addWidget(self.circle)

        for i in range(9):
            self.createVar[f'self.index{i}']=QPushButton()
            self.createVar[f'self.index{i}'].setStyleSheet("QPushButton{font:bold;font-family:微软雅黑;}")
            self.createVar[f'self.indexData{i}']=QLabel()
            self.createVar[f'self.indexData{i}'].setStyleSheet("QLabel{font:bold;font-size:14px;}")
            statusbar.addWidget(self.createVar[f'self.index{i}'])
            statusbar.addWidget(self.createVar[f'self.indexData{i}'])

    def flashLabel(self,offset,worldIndexData):
        for i in range(8):
            if (globalVariable.marketNum==1 or globalVariable.marketNum==3) and i==2 and self.isKC:
                self.createVar[f'self.index{i}'].setText(worldIndexData.loc[16,'f14'])
                if worldIndexData.loc[16,'f3']=='-' or worldIndexData.loc[16,'f3']>=0:
                    self.createVar[f'self.indexData{i}'].setPalette(globalVariable.pered)
                else:
                    self.createVar[f'self.indexData{i}'].setPalette(globalVariable.pegreen)
                self.createVar[f'self.indexData{i}'].setText(f"{worldIndexData.loc[16,'f2']}  {worldIndexData.loc[16,'f3']}%")
                self.isKC=False
            else:
                self.createVar[f'self.index{i}'].setText(worldIndexData.loc[i+offset,'f14'])
                if worldIndexData.loc[i+offset,'f3']=='-' or worldIndexData.loc[i+offset,'f3']>=0:
                    self.createVar[f'self.indexData{i}'].setPalette(globalVariable.pered)
                else:
                    self.createVar[f'self.indexData{i}'].setPalette(globalVariable.pegreen)
                self.createVar[f'self.indexData{i}'].setText(f"{worldIndexData.loc[i+offset,'f2']}  {worldIndexData.loc[i+offset,'f3']}%")
                if i==2:
                    self.isKC=True
