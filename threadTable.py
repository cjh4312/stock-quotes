# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread
import globalVariable

#import datetime

class TableThread(QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()
    _signalErr=Signal()
    _signal_draw=Signal()

    def __init__(self,parent):
        super(TableThread, self).__init__()
        self.parent=parent
        self.num=6

    def __del__(self):
        self.wait()

    def run(self):
        if globalVariable.getValue()==1:
            self.parent.tableView.get_zh_market()

            if self.parent.isFlashBoard:
                self.parent.tableView.get_industry_concept_board(self.parent.board_code)
                #self.parent.tableView.reflashView()
            self.parent.tableView.init_ui()

            for i in range(1,len(self.parent.tableView.my_stock_data)+1):
                for j in range(1,len(self.parent.tableView.stock_data_copy)+1):
                    if self.parent.tableView.my_stock_data.loc[i,'代码']==self.parent.tableView.stock_data_copy.loc[j,'代码']:
                        self.parent.tableView.my_stock_data.loc[i]=self.parent.tableView.stock_data_copy.loc[j]
                        break
            self.parent.tableView.my_stock_data.to_csv('list/my_stock.csv',encoding='gbk')

            self._signal.emit()
            if self.num==6:
                rise=0
                fall=0
                for j in range(1,len(self.parent.tableView.stock_data_copy)+1):
                    if self.parent.tableView.stock_data_copy.loc[j,'涨跌幅']>0:
                        rise+=1
                    elif self.parent.tableView.stock_data_copy.loc[j,'涨跌幅']<0:
                        fall+=1
                    self.parent.baseInformation.base_info['self.rise_data'].setText(str(int(rise)))
                    self.parent.baseInformation.base_info['self.fall_data'].setText(str(int(fall)))
                    self.num=0
            self.num+=1

        elif globalVariable.getValue()==2:
            self.parent.tableView.get_us_market()
            self.parent.tableView.init_ui()
            self._signal.emit()
        elif globalVariable.getValue()==5:
            self.parent.tableView.get_hk_market()
            self.parent.tableView.init_ui()
            self._signal.emit()

        elif globalVariable.getValue()==4:
            if globalVariable.subCount==1:
                self.parent.tableView.getRoyalFlushPlateFundFlow(self.parent.period_text.currentText())
            elif globalVariable.subCount==2:
                self.parent.tableView.get_stock_hot_rank_em()
            elif globalVariable.subCount==3:
                self.parent.tableView.stock_yesterday_pool_strong_em(self.parent.dateEdit.dateTime())
            elif globalVariable.subCount==4:
                if self.parent.period_text.currentIndex()==0:
                    self.parent.tableView.getTodayEastPlateFundFlow()
                elif self.parent.period_text.currentIndex()==2:
                    self.parent.tableView.getFiveEastPlateFundFlow()
                elif self.parent.period_text.currentIndex()==3:
                    self.parent.tableView.getTenEastPlateFundFlow()
                else:
                    self._signalErr.emit()
                    return

            elif globalVariable.subCount==5:
                self.parent.tableView.get_high_low_statistics()
            elif globalVariable.subCount==6:
                days={'今日':'1','3日':'3','5日':'5','10日':'10','月':'M','季':'Q','年':'Y'}
                #self.parent.tableView.north_plate_flows(self.parent.north_box.currentText())
                self.parent.tableView.north_plate_flows1(days[self.parent.north_box.currentText()])
            elif globalVariable.subCount==7:
                self.parent.tableView.business_department_rank(self.parent.business_department_text.currentIndex()+1)
            elif globalVariable.subCount==8:
                self.parent.tableView.fund_open_fund_rank()
            elif globalVariable.subCount==9:
                nums={globalVariable.curRecentMarketDay():1,'近3日':3,'近5日':5,'近10日':10,'近30日':30}
                pages={globalVariable.curRecentMarketDay():1,'近3日':1,'近5日':1,'近10日':2,'近30日':4}
                self.parent.tableView.tradedetail(nums[self.parent.tradedetail_text.currentText()],\
                                                  pages[self.parent.tradedetail_text.currentText()])
            self._signal.emit()

#        elif globalVariable.getValue()==3:
#            code=self.parent.stock_code
#            if self.parent.ui.us_market.isChecked()==False and self.parent.ui.hk_market.isChecked()==False:
#                self.parent.data.login_init(code,self.parent.period,self.parent.adjustflag)
#            elif self.parent.ui.us_market.isChecked()==True:
#                self.parent.data.get_us_data_from_east(code,self.parent.period,self.parent.adjustflag)
#            elif self.parent.ui.hk_market.isChecked()==True:
#                if code[0:3]=='sh.' or code[0:3]=='399':
#                    self.parent.data.login_init(code,self.parent.period,self.parent.adjustflag)
#                else:
#                    self.parent.data.get_hk_data_from_east(code,self.parent.period,self.parent.adjustflag)
#            self._signal_draw.emit()
