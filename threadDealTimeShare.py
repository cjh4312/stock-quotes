# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6 import QtCore
from PySide6.QtCore import Signal
import requests
import json
from pandas.core.frame import DataFrame
import globalVariable

class DealTimeShareThread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()

    def __init__(self,parent):
        super(DealTimeShareThread, self).__init__()
        self.parent=parent
        self.isTrue=True

    def deal_time_share_chart(self):
        code=self.parent.stock_code

        if code[0:4]=='100.' or code[0:4]=='103.' or code[0:4]=='104.':
            self.isTrue=False
            (self.parent.pre_close,time_share_list)=self.parent.worldIndex.get_index_time_share_chart(code)
        elif code[0:4]=='105.' or code[0:4]=='106.' or code[0:4]=='107.':
            self.isTrue=False
            (self.parent.pre_close,time_share_list)=self.parent.worldIndex.get_us_hk_time_share_chart(code)
        elif len(code)==5:
            code='116.'+code
            self.isTrue=False
            (self.parent.pre_close,time_share_list)=self.parent.worldIndex.get_us_hk_time_share_chart(code)
        else:
            self.isTrue=True
            if code[0]=='3' or code[0]=='0' or code[0]=='8' or code[0]=='4':
                num=0
            else:
                num=1
                if code[0]=='s' and code[2]=='.' and code[3].isdigit():
                    code=code[3:9]
            (self.parent.pre_close,time_share_list)=self.parent.worldIndex.get_time_share_chart_data5(num,code)
        if len(time_share_list)==0:
            return
        pre_close=self.parent.pre_close

        if self.parent.whichDay>0 and self.parent.whichDay<5:
            self.parent.pre_close=self.parent.data.data.loc[len(self.parent.data.data)-self.parent.whichDay-1,'close']-\
                    self.parent.data.data.loc[len(self.parent.data.data)-self.parent.whichDay-1,'pctVal']
        elif self.parent.whichDay==0:
            self.parent.pre_close=pre_close
        elif self.parent.whichDay>4:
            return

        l1=0
        l2=len(time_share_list)
        if self.isTrue:
            if self.parent.period!='101':
                return
            l1=(4-self.parent.whichDay)*241
            if self.parent.whichDay>0:
                l2=(5-self.parent.whichDay)*241
        self.parent.time_share_chart_data.drop(self.parent.time_share_chart_data.index, inplace=True)

        self.parent.high_low_point=[0]*5
        a=self.parent.pre_close*1.1
        b=self.parent.pre_close*0.9
        from decimal import Decimal, ROUND_HALF_UP
        c=Decimal(str(a)).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)
        d=Decimal(str(b)).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)
        c=Decimal(str(c)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        d=Decimal(str(d)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        self.parent.high_low_point[3]=round((float(c)-self.parent.pre_close)*100/self.parent.pre_close,2)
        self.parent.high_low_point[4]=round((float(d)-self.parent.pre_close)*100/self.parent.pre_close,2)
        for i in range(l1,l2):
            time_share_list[i]=time_share_list[i].split(',',8)

            pd_len=len(self.parent.time_share_chart_data)
            self.parent.time_share_chart_data.loc[pd_len,'Time']=time_share_list[i][0]
            price=round((float(time_share_list[i][2])-self.parent.pre_close)*100/self.parent.pre_close,2)
            price_high=round((float(time_share_list[i][3])-self.parent.pre_close)*100/self.parent.pre_close,2)
            price_low=round((float(time_share_list[i][4])-self.parent.pre_close)*100/self.parent.pre_close,2)
            ave_price=round((float(time_share_list[i][7])-self.parent.pre_close)*100/self.parent.pre_close,2)
            vol=int(time_share_list[i][5])
            if float(time_share_list[i][2])>float(time_share_list[i][1]):
                self.parent.time_share_chart_data.loc[pd_len,'direct']=2
            elif float(time_share_list[i][2])<float(time_share_list[i][1]):
                self.parent.time_share_chart_data.loc[pd_len,'direct']=1
            else:
                self.parent.time_share_chart_data.loc[pd_len,'direct']=3
            if price_high>self.parent.high_low_point[0]:
                self.parent.high_low_point[0]=price_high
            if price_low<self.parent.high_low_point[1]:
                self.parent.high_low_point[1]=price_low
            if vol>self.parent.high_low_point[2]:
                self.parent.high_low_point[2]=vol
            self.parent.time_share_chart_data.loc[pd_len,'vol']=vol
            self.parent.time_share_chart_data.loc[pd_len,'price']=price
            self.parent.time_share_chart_data.loc[pd_len,'ave_price']=ave_price

    def get_earning_and_pe_static(self):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        code=self.parent.stock_code
        stock_code=''
        if globalVariable.marketNum==1 or globalVariable.marketNum==3:
            if code[0:1]=='s' or code[0:3]=='399':
                return
            if code[0] == '6':
                stock_code = 'SH'+code
            elif code[0] in ['4','8']:
                stock_code = 'BJ'+code
            elif code[0] in ['0','3']:
                stock_code = 'SZ'+code

            url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code={}'.format(stock_code)
            df=requests.get(url,headers=headers).content.decode()
            d=DataFrame(json.loads(df)['data'])
            d=d.T
            l=d.loc['REPORT_DATE_NAME',0]
            list={'一季度':1,'中报':2,'三季报':3,'年报':4}
            A={1:'一',2:'二',3:'三',4:'四',5:'五'}
            a=list[l[4:len(l)]]

            self.parent.baseInformation.base_info['self.earnings'].setText(f"收益({A[a]})")
            self.parent.baseInformation.base_info['self.earnings_data'].setText(str(d.loc['EPSJB',0]))
            self.parent.baseInformation.base_info['self.pe_static_data'].setText(str(round(self.parent.now_close/d.loc['EPSJB',a%4],2)))

    def __del__(self):
        self.wait()

    def run(self):
        self.deal_time_share_chart()
        self._signal.emit()
        if self.isTrue:
            self.get_earning_and_pe_static()

