# This Python file uses the following encoding: utf-8
import pandas as pd
# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal, QThread
import globalVariable
import datetime


class TableThread(QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()
    _signalErr = Signal()
    _signal_draw = Signal()

    def __init__(self, parent):
        super(TableThread, self).__init__()
        self.parent = parent
        self.num = 6
        self.code = []
        self.isFirst = True
        self.order = ['代码', '名称', '最新价', '涨跌幅', '换手率', '成交额', '涨速', '市盈率', '总市值', '流通市值',
                 '今年', '60日', '成交量', '最高', '最低', '今开', '昨收']

    def __del__(self):
        self.wait()

    def run(self):
        t = datetime.datetime.now()
        if globalVariable.getValue() == 1:
            # 获取所有A股信息
            self.parent.tableView.get_zh_market()
            # 如果是板块
            if self.parent.isFlashBoard:
                self.parent.tableView.get_industry_concept_board(self.parent.board_code)
                # self.parent.tableView.reflashView()
            self.parent.tableView.init_ui()
            # print(datetime.datetime.now()-t)
            n = len(self.parent.tableView.stock_data_copy)
            for i in range(1, len(self.parent.tableView.my_stock_data) + 1):
                l = 0
                r = n - 1
                while l <= r:
                    mid = (l + r) // 2
                    if self.parent.tableView.stock_data_copy.iat[mid, 0] == self.parent.tableView.my_stock_data.loc[
                        i, '代码']:
                        self.parent.tableView.my_stock_data.loc[i] = self.parent.tableView.stock_data_copy.loc[mid + 1]
                        break
                    elif self.parent.tableView.stock_data_copy.iat[mid, 0] > self.parent.tableView.my_stock_data.loc[
                        i, '代码']:
                        r = mid - 1
                    else:
                        l = mid + 1
            self.parent.tableView.my_stock_data.to_csv('list/my_stock.csv', encoding='gbk', index=False)
            self._signal.emit()
            # print(datetime.datetime.now()-t)
            if self.num == 6:
                rise = 0
                fall = 0
                for j in range(1, len(self.parent.tableView.stock_data_copy) + 1):
                    if self.parent.tableView.stock_data_copy.loc[j, '涨跌幅'] > 0:
                        rise += 1
                    elif self.parent.tableView.stock_data_copy.loc[j, '涨跌幅'] < 0:
                        fall += 1
                    self.parent.baseInformation.base_info['self.rise_data'].setText(str(int(rise)))
                    self.parent.baseInformation.base_info['self.fall_data'].setText(str(int(fall)))
                    self.num = 0
            self.num += 1

            if globalVariable.isZhMarketDay() and str(t)[11:16] >= '09:30':
                if self.isFirst:
                    self.isFirst = False
                    d = pd.read_csv(r'./list/rising_speed.csv', encoding='gbk')
                    for i in d['代码']:
                        self.code.append(i)
                for n, code_tuple in enumerate(zip(self.parent.tableView.rising_speed_data['代码'],
                                                   self.parent.tableView.rising_speed_data['涨速'])):
                    speed = int(code_tuple[1])
                    code = int(code_tuple[0])
                    if speed >= 5:
                        if code not in self.code:
                            dd = pd.DataFrame(columns=self.order)
                            dd.loc[1] = self.parent.tableView.rising_speed_data.loc[n + 1]
                            dd.to_csv(r'./list/rising_speed.csv', encoding='gbk', mode='a', index=False,
                                           header=False)
                            self.code.append(code)
                    elif speed >= 3:
                        if code not in self.code:
                            dd = pd.DataFrame(columns=self.order)
                            dd.loc[1] = self.parent.tableView.rising_speed_data.loc[n + 1]
                            dd.to_csv(r'./list/rising_speed.csv', encoding='gbk', mode='a', index=False,
                                           header=False)
                            self.code.append(code)
        elif globalVariable.getValue() == 2:
            if self.parent.isUsZhStock:
                fs = 'b:mk0201'
            else:
                fs = 'm:105,m:106,m:107'
            self.parent.tableView.get_us_market(fs)
            self.parent.tableView.init_ui()
            self._signal.emit()
        elif globalVariable.getValue() == 5:
            self.parent.tableView.get_hk_market()
            self.parent.tableView.init_ui()
            self._signal.emit()

        elif globalVariable.getValue() == 4:
            if globalVariable.subCount == 0:
                self.parent.tableView.getTbnormalFluctuation()
            elif globalVariable.subCount == 1:
                self.parent.tableView.getRoyalFlushPlateFundFlow(self.parent.period_text.currentText())
            elif globalVariable.subCount == 2:
                self.parent.tableView.get_stock_hot_rank_em()
            elif globalVariable.subCount == 3:
                self.parent.tableView.stock_yesterday_pool_strong_em(self.parent.dateEdit.dateTime())
            elif globalVariable.subCount == 4:
                if self.parent.period_text.currentIndex() == 0:
                    self.parent.tableView.getTodayEastPlateFundFlow()
                elif self.parent.period_text.currentIndex() == 2:
                    self.parent.tableView.getFiveEastPlateFundFlow()
                elif self.parent.period_text.currentIndex() == 3:
                    self.parent.tableView.getTenEastPlateFundFlow()
                else:
                    self._signalErr.emit()
                    return

            elif globalVariable.subCount == 5:
                self.parent.tableView.get_high_low_statistics()
            elif globalVariable.subCount == 6:
                days = {'今日': '1', '3日': '3', '5日': '5', '10日': '10', '月': 'M', '季': 'Q', '年': 'Y'}
                # self.parent.tableView.north_plate_flows(self.parent.north_box.currentText())
                self.parent.tableView.north_plate_flows1(days[self.parent.north_box.currentText()])
            elif globalVariable.subCount == 7:
                self.parent.tableView.business_department_rank(self.parent.business_department_text.currentIndex() + 1)
            elif globalVariable.subCount == 8:
                self.parent.tableView.fund_open_fund_rank()
            elif globalVariable.subCount == 9:
                nums = {str(globalVariable.curRecentMarketDay().date()): 1, '近3日': 3, '近5日': 5, '近10日': 10,
                        '近30日': 30}
                pages = {str(globalVariable.curRecentMarketDay().date()): 1, '近3日': 1, '近5日': 1, '近10日': 2,
                         '近30日': 4}
                self.parent.tableView.trade_detail(nums[self.parent.tradedetail_text.currentText()], \
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
