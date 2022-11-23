# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import os
import pandas as pd
import getEastData
from PySide6.QtWidgets import QTableView,QAbstractItemView,QMessageBox
import modelTableStock
#import modelZHTableStock
import modelAnalysisTable
import modelTimeShare
import globalVariable
import requests
import json
import re
#import jsonpath
#import math
from pandas.core.frame import DataFrame
import urllib

class TableStock(QTableView):
    def __init__(self):
        super(TableStock, self).__init__()
        self.sort_bool=[False]*20
        self.pre_index=3

        self.sort_bool[self.pre_index]=True
        self.view = QTableView()
        self.view.setMinimumHeight(946)
        self.view.verticalScrollBar().setStyleSheet("QScrollBar{width:9px;}")
        self.view.horizontalScrollBar().setStyleSheet("QScrollBar{width:0px;}")
        #self.view.setSelectionMode(QAbstractItemView.NoSelection)
        self.view2=QTableView()
        self.view3=QTableView()
        self.view_rising_speed=QTableView()
        self.view_rising_speed.verticalScrollBar().setStyleSheet("QScrollBar{width:0px;}")
        self.view_rising_speed.horizontalScrollBar().setStyleSheet("QScrollBar{width:0px;}")
        self.view_my_stock=QTableView()
        self.view_my_stock.verticalScrollBar().setStyleSheet("QScrollBar{width:0px;}")
        self.view_my_stock.horizontalScrollBar().setStyleSheet("QScrollBar{width:0px;}")

        #self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.view2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.verticalHeader().setMinimumSectionSize(21)
        self.view.verticalHeader().setDefaultSectionSize(21)
        self.view_rising_speed.verticalHeader().setMinimumSectionSize(25)
        self.view_rising_speed.verticalHeader().setDefaultSectionSize(25)
        self.view_my_stock.verticalHeader().setMaximumSectionSize(25)
        self.view_my_stock.verticalHeader().setDefaultSectionSize(25)
        self.view3.verticalHeader().setMinimumSectionSize(20)
        self.view3.verticalHeader().setDefaultSectionSize(20)
        #表格标题字体加粗
        font = self.view.horizontalHeader().font()
        font.setBold(True)
        font.setPixelSize(18)
        self.view.horizontalHeader().setFont(font)

        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(False)
        self.view_rising_speed.setShowGrid(False)
        self.view_my_stock.setShowGrid(False)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view_rising_speed.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view_my_stock.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stock_data_copy=self.stock_data=pd.DataFrame

        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        self.period1='2022-09-30%2C2022-06-30%2C2022-03-31%2C2021-12-31%2C2021-09-30'
        self.period2='2021-06-30%2C2021-03-31%2C2020-12-31%2C2020-09-30%2C2020-06-30'

    def get_hk_market(self):
        url='http://87.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124013838806870658193_1667966922146&pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=7111416627128474|0|1|0|web&fid=f3&fs=m:116+t:3,m:116+t:4,m:116+t:1,m:116+t:2&fields=f2,f3,f5,f6,f8,f9,f12,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22&_=1667966922156'
        order=['代码','名称','最新价','涨跌幅','换手率','成交额','涨速','市盈率',\
                 '总市值','流通市值','今年','60日','成交量','最高','最低','今开','昨收']
        df=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        self.stock_data=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data.rename(columns={'f12':'代码','f14':'名称','f15':'最高','f2':'最新价','f3':'涨跌幅',\
              'f5':'成交量','f6':'成交额','f16':'最低','f17':'今开','f8':'换手率','f9':'市盈率','f18':'昨收',\
              'f20':'总市值','f21':'流通市值','f22':'涨速','f24':'60日','f25':'今年'},inplace=True)
        #self.stock_data.rename(columns={'市盈率-动态':'市盈率','年初至今涨跌幅':'今年','60日涨跌幅':'60日'},inplace=True)
        self.stock_data=self.stock_data[order]
        self.stock_data=self.stock_data.replace('-',0)
        self.stock_data[self.stock_data.columns[2:]]=self.stock_data[self.stock_data.columns[2:]].astype(float)

    def get_us_market(self):
        order=['代码','名称','最新价','涨跌幅','换手率','成交额','涨速','市盈率',\
                 '总市值','流通市值','今年','60日','成交量','最高','最低','今开','昨收']
        url='http://3.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022612904122108612_1667962034365&pn=1&pz=13000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=7111416627128474|0|1|0|web&fid=f3&fs=m:105,m:106,m:107&fields=f2,f3,f5,f6,f8,f9,f12,f13,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22&_=1667962034515'
        df=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        self.stock_data=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data.rename(columns={'f14':'名称','f15':'最高','f2':'最新价','f3':'涨跌幅',\
              'f5':'成交量','f6':'成交额','f16':'最低','f17':'今开','f8':'换手率','f9':'市盈率','f18':'昨收',\
              'f20':'总市值','f21':'流通市值','f22':'涨速','f24':'60日','f25':'今年'},inplace=True)
        self.stock_data['代码']=self.stock_data['f13'].map(str)+'.'+self.stock_data['f12']
        self.stock_data=self.stock_data[order]
        self.stock_data=self.stock_data.replace('-',0)
        self.stock_data[self.stock_data.columns[2:]]=self.stock_data[self.stock_data.columns[2:]].astype(float)

    def get_zh_market(self):

        order=['代码','名称','最新价','涨跌幅','换手率','成交额','涨速','市盈率',\
                 '总市值','流通市值','今年','60日','成交量','最高','最低','今开','昨收']
        url='http://64.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406735051047749057_1667954879287&pn=1&pz=6000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=1&wbp2u=7111416627128474|0|1|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f2,f3,f5,f6,f8,f9,f12,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22&_=1667954879297'
        df=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        self.stock_data=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data.rename(columns={'f14':'名称','f12':'代码','f15':'最高','f2':'最新价','f3':'涨跌幅',\
              'f5':'成交量','f6':'成交额','f16':'最低','f17':'今开','f8':'换手率','f9':'市盈率','f18':'昨收',\
              'f20':'总市值','f21':'流通市值','f22':'涨速','f24':'60日','f25':'今年'},inplace=True)
        self.stock_data=self.stock_data[order]
        self.stock_data=self.stock_data.replace('-',0)
        self.stock_data[self.stock_data.columns[2:]]=self.stock_data[self.stock_data.columns[2:]].astype(float)
        #self.stock_data[['最新价','涨跌幅','换手率','市盈率','涨速','60日','今年','最高','最低','今开','昨收']]=self.stock_data[['最新价','涨跌幅','换手率','市盈率','涨速','60日','今年','最高','最低','今开','昨收']]/100
        self.stock_data_copy=self.stock_data.copy(deep=True)
        self.stock_data_copy.index = pd.RangeIndex(start=1, stop=len(self.stock_data_copy)+1, step=1)
        if os.path.exists('list/my_stock.csv'):
            self.my_stock_data=pd.read_csv('list/my_stock.csv',encoding="gbk",dtype={'代码':str})
            self.my_stock_data.drop(self.my_stock_data.columns[[0]],axis=1,inplace=True)
            self.my_stock_data.index = pd.RangeIndex(start=1, stop=len(self.my_stock_data)+1, step=1)
        else:
            self.my_stock_data=pd.DataFrame(columns=order)
        self.rising_speed_data=self.stock_data_copy.sort_values(by=self.stock_data_copy.columns[6] , ascending=False,kind="mergesort")
        self.rising_speed_data=self.rising_speed_data.drop(self.rising_speed_data.index[30:len(self.rising_speed_data)])
        #self.rising_speed_data=self.rising_speed_data.drop(self.stock_data_copy.columns[6:17],axis=1)
        self.rising_speed_data.index = pd.RangeIndex(start=1, stop=len(self.rising_speed_data)+1, step=1)

    def pick_stocks(self):
        if globalVariable.getValue()==1:
            order=['代码','名称','最新价','涨跌幅','换手率','成交额','市盈率','成交量',\
                     '总市值','流通市值','今年','60日','涨速','最高','最低','今开','昨收']
            data=pd.DataFrame(columns=order)
            for i in range(1,len(self.stock_data_copy)+1):
                c=self.stock_data_copy.loc[i,'最新价']
                C=self.stock_data_copy.loc[i,'昨收']
                from decimal import Decimal, ROUND_HALF_UP
                if c==0 or float(Decimal(str(C*1.1)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))==c or\
                        float(Decimal(str(C*1.2)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))==c:
                    continue
                H=self.stock_data_copy.loc[i,'最高']
                if (H-c)/c<=0.003 and self.stock_data_copy.loc[i,'涨跌幅']>=2.5:
                    if (self.stock_data_copy.loc[i,'名称'][0:1]!='*' and self.stock_data_copy.loc[i,'名称'][0:1]!='s' and\
                            self.stock_data_copy.loc[i,'名称'][0:1]!='S'):
                        data.loc[len(data)+1]=self.stock_data_copy.loc[i]
            self.stock_data=data.sort_values(by=data.columns[3] , ascending=False,kind="mergesort")
            self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
            self.model = modelTableStock.ModelTableStock(self.stock_data)
            self.view.setModel(self.model)
        else:
            QMessageBox.information(self,"提示","只能选A股或者在主界面",QMessageBox.Ok)

    def get_industry_concept_board(self,code):
        url='http://38.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124026009176356636043_1665552114816&pn=1&pz=2000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:{}+f:!50&fields=f2,f3,f5,f6,f8,f9,f12,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22&_=1665552114833'.format(code)
        df=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        self.stock_data=DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data=self.stock_data.replace('-',0)
        order=['代码','名称','最新价','涨跌幅','换手率','成交额','市盈率','成交量',\
                       '总市值','流通市值','涨速','60日','今年','最高','最低','今开','昨收']
        self.stock_data.rename(columns={'f12':'代码','f14':'名称','f2':'最新价','f3':'涨跌幅',\
                'f5':'成交量','f6':'成交额','f15':'最高','f16':'最低','f17':'今开','f18':'昨收',\
                'f20':'总市值','f21':'流通市值','f8':'换手率','f9':'市盈率','f22':'涨速','f24':'60日',\
                'f25':'今年'},inplace=True)
        self.stock_data=self.stock_data[order]
        self.stock_data[self.stock_data.columns[2:]]=self.stock_data[self.stock_data.columns[2:]].astype(float)
        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
        self.model = modelTableStock.ModelTableStock(self.stock_data)

    def getRoyalFlushPlateFundFlow(self,period):
        a1 = getEastData.stock_fund_flow_concept(period)
        a2 = getEastData.stock_fund_flow_industry(period)
        self.stock_data1=pd.concat([a1,a2])
        self.stock_data1.drop(self.stock_data1.columns[[0]],axis=1,inplace=True)
        if period=='即时':
            column=2
        else:
            column=3
            self.stock_data1['阶段涨跌幅'] = self.stock_data1['阶段涨跌幅'].str.strip("%").astype(float);
        self.stock_data1.sort_values(by=self.stock_data1.columns[column] , ascending=False,kind="mergesort",inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def getTodayEastPlateFundFlow(self):
        url2='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123036618177432266985_1668003086708&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A1&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
        url1='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123036618177432266985_1668003086708&fid=f62&po=1&pz=500&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
        url3='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303648106282688208_1667998184612&fid=f62&po=1&pz=100&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
        df=requests.get(url3,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data1=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url1,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data2=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url2,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data3=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data1=pd.concat([stock_data1,stock_data2,stock_data3])
        self.stock_data1.rename(columns={'f14':'名称','f3':'涨跌幅','f62':'主力净额','f184':'主力净占比','f66':'超大单净额','f69':'超大单净占比','f72':'大单净额','f75':'大单净占比','f78':'中单净额','f81':'中单净占比','f84':'小单净额','f87':'小单净占比','f204':'主力净流入最大股'},inplace=True)
        order=['名称','涨跌幅','主力净额','主力净占比','超大单净额','超大单净占比','大单净额','大单净占比','中单净额','中单净占比','小单净额','小单净占比','主力净流入最大股']
        self.stock_data1=self.stock_data1[order]
        self.stock_data1.sort_values(by=self.stock_data1.columns[1],ascending=False,kind="mergesort",inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def getFiveEastPlateFundFlow(self):
        url1='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525261&fid=f109&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A1&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13'
        url2='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525259&fid=f109&po=1&pz=500&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13'
        url3='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525259&fid=f109&po=1&pz=100&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13'
        df=requests.get(url3,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data1=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url1,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data2=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url2,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data3=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data1=pd.concat([stock_data1,stock_data2,stock_data3])
        self.stock_data1.rename(columns={'f14':'名称','f109':'5日涨跌幅','f164':'主力净额','f165':'主力净占比','f166':'超大单净额','f167':'超大单净占比','f168':'大单净额','f169':'大单净占比','f170':'中单净额','f171':'中单净占比','f172':'小单净额','f173':'小单净占比','f257':'主力净流入最大股'},inplace=True)
        order=['名称','5日涨跌幅','主力净额','主力净占比','超大单净额','超大单净占比','大单净额','大单净占比','中单净额','中单净占比','小单净额','小单净占比','主力净流入最大股']
        self.stock_data1=self.stock_data1[order]
        self.stock_data1.sort_values(by=self.stock_data1.columns[1],ascending=False,kind="mergesort",inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def getTenEastPlateFundFlow(self):
        url3='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525259&fid=f160&po=1&pz=100&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13'
        url1='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525261&fid=f160&po=1&pz=500&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13'
        url2='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309254256237089538_1668582525259&fid=f160&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A1&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13'
        df=requests.get(url3,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data1=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url1,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data2=pd.DataFrame(json.loads(json_data)['data']['diff'])
        df=requests.get(url2,headers=self.headers).text
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        stock_data3=pd.DataFrame(json.loads(json_data)['data']['diff'])
        self.stock_data1=pd.concat([stock_data1,stock_data2,stock_data3])
        self.stock_data1.rename(columns={'f14':'名称','f160':'10日涨跌幅','f174':'主力净额','f175':'主力净占比','f176':'超大单净额','f177':'超大单净占比','f178':'大单净额','f179':'大单净占比','f180':'中单净额','f181':'中单净占比','f182':'小单净额','f183':'小单净占比','f260':'主力净流入最大股'},inplace=True)
        order=['名称','10日涨跌幅','主力净额','主力净占比','超大单净额','超大单净占比','大单净额','大单净占比','中单净额','中单净占比','小单净额','小单净占比','主力净流入最大股']
        self.stock_data1=self.stock_data1[order]
        self.stock_data1.sort_values(by=self.stock_data1.columns[1],ascending=False,kind="mergesort",inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_stock_hot_rank_em(self):
        data1 = getEastData.getStockHot()
        for i in range(len(data1)):
            data1.loc[i,'代码']=data1.loc[i,'代码'][2:8]
        data2 = getEastData.stock_hot_tgb()
        self.stock_data=pd.concat([data1,data2],axis=1)
        self.stock_data.drop(self.stock_data.columns[[0]],axis=1,inplace=True)
        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data)

    def get_high_low_statistics(self):
        #order=['交易日','收盘价','20日新高','20日新低','60日新高','60日新低','120日新高','120日新低']
        url = "https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/all"
        import ssl
        # 使用ssl创建未验证的上下文，在url中传入上下文参数
        context = ssl._create_unverified_context()
        # 将context传入url函数的context参数中
        request =urllib.request.Request(url,headers=self.headers)
        data=urllib.request.urlopen(request,context=context).readline().decode()
        self.stock_data=pd.DataFrame(eval(data))
        self.stock_data["date"] = pd.to_datetime(self.stock_data["date"], unit="ms").dt.date
        del self.stock_data["indexCode"]
        self.stock_data.rename(columns={'date':'交易日','close':'收盘价','high20':'20日新高','low20':'20日新低',
                                    'high60':'60日新高','low60':'60日新低','high120':'120日新高',
                                    'low120':'120日新低'},inplace=True)
        #self.stock_data.sort_values(by=self.stock_data.columns[0],ascending=False,kind="mergesort",inplace=True)
        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data)

    def get_stock_hot_keyword_em(self,code):
        self.stock_data1 = getEastData.get_stock_hot_keyword(code)
        #self.stock_data1.drop(self.stock_data1.columns[[0]],axis=1,inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def stock_yesterday_pool_strong_em(self,date):
        date=date.toString("yyyyMMdd")
        self.stock_data = getEastData.get_stock_pool_strong(date)
        if len(self.stock_data)==0:
            return
        self.stock_data.drop(self.stock_data.columns[[0]],axis=1,inplace=True)
        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
        self.model=modelAnalysisTable.AnalysisTable(self.stock_data)

    def get_main_business_com(self,code):
        self.stock_data1 = getEastData.stock_zygc_ym(code)
        #self.stock_data1.drop(self.stock_data1.columns[[0]],axis=1,inplace=True)
        self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_main_indicator(self,code):
        url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code={}'.format(code)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        df=requests.get(url,headers=headers).content.decode()
        data=DataFrame(json.loads(df)['data'])
        data=data.T
        data.rename(index={'EPSJB':'基本每股收益(元)','EPSKCJB':'扣非每股收益(元)','EPSXS':'稀释每股收益(元)',\
        'BPS':'每股净资产(元)','MGZBGJ':'每股公积金(元)','MGWFPLR':'每股未分配利润(元)','MGJYXJJE':'每股经营现金流(元)',\
        'TOTALOPERATEREVE':'营业总收入(元)','PARENTNETPROFIT':'归属净利润(元)','KCFJCXSYJLR':'扣非净利润(元)',\
        'TOTALOPERATEREVETZ':'营业总收入同比增长(%)','PARENTNETPROFITTZ':'归属净利润同比增长(%)','TOTALDEPOSITS':'存款总额(元)',\
        'KCFJCXSYJLRTZ':'扣非净利润同比增长(%)','YYZSRGDHBZC':'营业总收入滚动环比增长(%)','GROSSLOANS':'贷款总额(元)',\
        'NETPROFITRPHBZC':'归属净利润滚动环比增长(%)','KFJLRGDHBZC':'扣非净利润滚动环比增长(%)','LTDRR':'存贷款比例',\
        'ROEJQ':'净资产收益率(加权)(%)','ROEKCJQ':'净资产收益率(扣非/加权)(%)','ZZCJLL':'净资产收益率(扣非/加权)(%)',\
        'XSJLL':'净利率(%)','XSMLL':'毛利率(%)','LD':'流动比率','SD':'速动比率','XJLLB':'现金流量比率','NEWCAPITALADER':'资本充足率(%)',\
        'ZCFZL':'资产负债率(%)','QYCS':'权益乘数','CQBL':'产权比率','ZZCZZTS':'总资产周转天数(天)','HXYJBCZL':'核心资本充足率(%)',\
        'CHZZTS':'存货周转天数(天)','YSZKZZTS':'应收账款周转天数(天)','TOAZZL':'总资产周转率(次)','NONPERLOAN':'不良贷款率(%)',\
        'CHZZL':'存货周转率(次)','YSZKZZL':'应收账款周转率(次)','BLDKBBL':'不良贷款拨备覆盖率(%)','NZBJE':'资本净额(元)'},inplace=True)
        data = data.reset_index()
        for i in range(len(data)):
                    if data[1][i]==None:
                        data.drop(labels=[i],inplace=True)
        for i in range(len(data.columns)-1):
                    data=data.rename(columns={i:data[i][7]})
        data.drop(labels=range(0,12),inplace=True)
        self.stock_data1 = data.reset_index(drop=True)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_asset_liability(self,code):
        url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period1,code)
        url1='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period2,code)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        df=requests.get(url,headers=headers).content.decode()
        df1=requests.get(url1,headers=headers).content.decode()
        data=DataFrame(json.loads(df)['data'])
        data1=DataFrame(json.loads(df1)['data'])
        data=pd.concat([data,data1],ignore_index=True)
        data=data.T
        data.rename(index={'MONETARYFUNDS':'货币资金','LEND_FUND':'拆出资金','NOTE_ACCOUNTS_RECE':'应收票据及应收账款','ACCOUNTS_RECE':'应收账款',\
        'NOTE_RECE':'其中:应收票据','PREPAYMENT':'预付款项','TOTAL_OTHER_RECE':'其他应收款合计','CURRENT_ASSET_BALANCE':'流动资产平衡项目','NONCURRENT_ASSET_BALANCE':'非流动资产平衡项目',\
        'INVENTORY':'存货','OTHER_CURRENT_ASSET':'其他流动资产','TOTAL_CURRENT_ASSETS':'流动资产合计','DIVIDEND_RECE':'应收股利','BUY_RESALE_FINASSET':'买入返售金融资产',\
        'LOAN_ADVANCE':'发放贷款及垫款','CREDITOR_INVEST':'债权投资','OTHER_NONCURRENT_FINASSET':'其他非流动金融资产',\
        'INVEST_REALESTATE':'投资性房地产','FIXED_ASSET':'固定资产','CIP':'在建工程','TRADE_FINASSET_NOTFVTPL':'交易性金融资产',\
        'USERIGHT_ASSET':'使用权资产','INTANGIBLE_ASSET':'无形资产','DEVELOP_EXPENSE':'开发支出','DERIVE_FINASSET':'衍生金融资产',\
        'LONG_PREPAID_EXPENSE':'长期待摊费用','DEFER_TAX_ASSET':'递延所得税资产','OTHER_NONCURRENT_ASSET':'其他非流动资产',\
        'TOTAL_NONCURRENT_ASSETS':'非流动资产合计','TOTAL_ASSETS':'资产总计','ACCOUNTS_PAYABLE':'其中:应付账款','ADVANCE_RECEIVABLES':'预收款项',\
        'NOTE_ACCOUNTS_PAYABLE':'应付票据及应付账款','CONTRACT_LIAB':'合同负债','STAFF_SALARY_PAYABLE':'应付职工薪酬',\
        'TAX_PAYABLE':'应交税费','TOTAL_OTHER_PAYABLE':'其他应付款合计','DIVIDEND_PAYABLE':'其中:应付股利','GOODWILL':'商誉',\
        'NONCURRENT_LIAB_1YEAR':'一年内到期的非流动负债','OTHER_CURRENT_LIAB':'其他流动负债','DEFER_INCOME':'递延收益',\
        'TOTAL_CURRENT_LIAB':'流动负债合计','TOTAL_NONCURRENT_LIAB':'非流动负债合计','LEASE_LIAB':'租赁负债','LONG_EQUITY_INVEST':'长期股权投资',\
        'DEFER_TAX_LIAB':'递延所得税负债','TOTAL_LIABILITIES':'负债合计','SHARE_CAPITAL':'实收资本（或股本）','SHORT_LOAN':'短期借款',\
        'CAPITAL_RESERVE':'资本公积','OTHER_COMPRE_INCOME':'其他综合收益','SURPLUS_RESERVE':'盈余公积','LONG_STAFFSALARY_PAYABLE':'长期应付职工薪酬',\
        'GENERAL_RISK_RESERVE':'一般风险准备','UNASSIGN_RPOFIT':'未分配利润',\
        'TOTAL_PARENT_EQUITY':'归属于母公司股东权益总计','MINORITY_EQUITY':'少数股东权益',\
        'TOTAL_EQUITY':'股东权益合计','TOTAL_LIAB_EQUITY':'负债和股东权益总计'},inplace=True)
        data = data.reset_index()
        for i in range(len(data)):
            if data[1][i]==None:
                data.drop(labels=[i],inplace=True)
        for i in range(len(data.columns)-1):
            data=data.rename(columns={i:data[i][7]})
        data.drop(labels=range(0,12),inplace=True)
        self.stock_data1 = data.reset_index(drop=True)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_Income(self,code):
        url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period1,code)
        url1='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period2,code)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        df=requests.get(url,headers=headers).content.decode()
        df1=requests.get(url1,headers=headers).content.decode()
        data=DataFrame(json.loads(df)['data'])
        data1=DataFrame(json.loads(df1)['data'])
        data=pd.concat([data,data1],ignore_index=True)
        data=data.T
        data.rename(index={'TOTAL_OPERATE_INCOME':'营业总收入','OPERATE_INCOME':'营业收入','FEE_COMMISSION_INCOME':'其中:手续费及佣金收入',\
        'INTEREST_INCOME':'利息收入','TOTAL_OPERATE_COST':'营业总成本','OPERATE_COST':'营业成本','ASSET_IMPAIRMENT_INCOME':'资产减值损失(新)',\
        'INTEREST_EXPENSE':'利息支出','FEE_COMMISSION_EXPENSE':'手续费及佣金支出',\
        'OPERATE_TAX_ADD':'税金及附加','SALE_EXPENSE':'销售费用','MANAGE_EXPENSE':'管理费用','OTHER_BUSINESS_COST':'其他业务成本','ASSET_IMPAIRMENT_LOSS':'资产减值损失',\
        'RESEARCH_EXPENSE':'研发费用','FINANCE_EXPENSE':'财务费用','FE_INTEREST_EXPENSE':'其中:利息费用','OTHER_COMPRE_INCOME':'其他综合收益',\
        'FE_INTEREST_INCOME':'利息收入','FAIRVALUE_CHANGE_INCOME':'加:公允价值变动收益','EXCHANGE_INCOME':'汇兑损失','OTHER_BUSINESS_INCOME':'其他业务收入',\
        'INVEST_INCOME':'投资收益','INVEST_JOINT_INCOME':'其中:对联营企业和合营企业的投资收益/（损失）','ASSET_DISPOSAL_INCOME':'资产处置收益',\
        'CREDIT_IMPAIRMENT_INCOME':'信用减值损失(新)','OTHER_INCOME':'其他收益','OPERATE_PROFIT':'营业利润','MINORITY_OCI':'归属于少数股东的其他综合收益',\
        'NONBUSINESS_INCOME':'加:营业外收入','NONBUSINESS_EXPENSE':'减:营业外支出','TOTAL_PROFIT':'利润总额','OPERATE_PROFIT_BALANCE':'营业利润平衡项目',\
        'INCOME_TAX':'减:所得税','NETPROFIT':'净利润','CONTINUED_NETPROFIT':'持续经营净利润','TOTAL_PROFIT_BALANCE':'利润总额平衡项目',\
        'PARENT_NETPROFIT':'归属于母公司股东的净利润','MINORITY_INTEREST':'少数股东损益',\
        'DEDUCT_PARENT_NETPROFIT':'扣除非经常性损益后的净利润','BASIC_EPS':'基本每股收益',\
        'DILUTED_EPS':'稀释每股收益','PARENT_OCI':'归属于母公司股东的其他综合收益',\
        'TOTAL_COMPRE_INCOME':'综合收益总额','MINORITY_TCI':'归属于少数股东的综合收益总额','PARENT_TCI':'归属于母公司股东的综合收益总额',\
        'TOTAL_OPERATE_INCOME_YOY':'同比营业总收入','OPERATE_INCOME_YOY':'同比营业收入','FEE_COMMISSION_INCOME_YOY':'同比其中:手续费及佣金收入',\
        'INTEREST_INCOME_YOY':'同比利息收入','TOTAL_OPERATE_COST_YOY':'同比营业总成本','OPERATE_COST_YOY':'同比营业成本','ASSET_IMPAIRMENT_IMCOME_YOY':'同比资产减值损失(新)',\
        'INTEREST_EXPENSE_YOY':'同比利息支出','FEE_COMMISSION_EXPENSE_YOY':'同比手续费及佣金支出','ASSET_IMPAIRMENT_INCOME_YOY':'同比资产减值损失(新)',\
        'OPERATE_TAX_ADD_YOY':'同比税金及附加','SALE_EXPENSE_YOY':'同比销售费用','MANAGE_EXPENSE_YOY':'同比管理费用','OTHER_BUSINESS_COST_YOY':'同比其他业务成本',\
        'RESEARCH_EXPENSE_YOY':'同比研发费用','FINANCE_EXPENSE_YOY':'同比财务费用','FE_INTEREST_EXPENSE_YOY':'同比其中:利息费用','OTHER_COMPRE_INCOME_YOY':'同比其他综合收益',\
        'FE_INTEREST_INCOME_YOY':'同比利息收入','FAIRVALUE_CHANGE_INCOME_YOY':'同比加:公允价值变动收益','EXCHANGE_INCOME_YOY':'同比汇兑损失','OTHER_BUSINESS_INCOME_YOY':'同比其他业务收入',\
        'INVEST_INCOME_YOY':'同比投资收益','INVEST_JOINT_INCOME_YOY':'同比其中:对联营企业和合营企业的投资收益/（损失）','ASSET_DISPOSAL_INCOME_YOY':'同比资产处置收益',\
        'CREDIT_IMPAIRMENT_INCOME_YOY':'同比信用减值损失(新)','OTHER_INCOME_YOY':'同比其他收益','OPERATE_PROFIT_YOY':'同比营业利润','MINORITY_OCI_YOY':'同比归属于少数股东的其他综合收益',\
        'NONBUSINESS_INCOME_YOY':'同比加:营业外收入','NONBUSINESS_EXPENSE_YOY':'同比减:营业外支出','TOTAL_PROFIT_YOY':'同比利润总额','OPERATE_PROFIT_BALANCE_YOY':'同比营业利润平衡项目',\
        'INCOME_TAX_YOY':'同比减:所得税','NETPROFIT_YOY':'同比净利润','CONTINUED_NETPROFIT_YOY':'同比持续经营净利润','TOTAL_PROFIT_BALANCE_YOY':'同比利润总额平衡项目',\
        'PARENT_NETPROFIT_YOY':'同比归属于母公司股东的净利润','MINORITY_INTEREST_YOY':'同比少数股东损益',\
        'DEDUCT_PARENT_NETPROFIT_YOY':'同比扣除非经常性损益后的净利润','BASIC_EPS_YOY':'同比基本每股收益',\
        'DILUTED_EPS_YOY':'同比稀释每股收益','PARENT_OCI_YOY':'同比归属于母公司股东的其他综合收益',\
        'TOTAL_COMPRE_INCOME_YOY':'同比综合收益总额','MINORITY_TCI_YOY':'同比归属于少数股东的综合收益总额',\
        'PARENT_TCI_YOY':'同比归属于母公司股东的综合收益总额'},inplace=True)
        data = data.reset_index()
        for i in range(len(data)):
            if data[1][i]==None:
                data.drop(labels=[i],inplace=True)
        for i in range(len(data.columns)-1):
            data=data.rename(columns={i:data[i][7]})
        data.drop(labels=range(0,12),inplace=True)
        self.stock_data1 = data.reset_index(drop=True)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_cash_flow(self,code):
        url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period1,code)
        url1='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbAjaxNew?companyType=4&reportDateType=0&reportType=1&dates={}&code={}'.format(self.period2,code)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        df=requests.get(url,headers=headers).content.decode()
        df1=requests.get(url1,headers=headers).content.decode()
        data=DataFrame(json.loads(df)['data'])
        data1=DataFrame(json.loads(df1)['data'])
        data=pd.concat([data,data1],ignore_index=True)
        data=data.T
        data.rename(index={'SALES_SERVICES':'销售商品、提供劳务收到的现金','DEPOSIT_INTERBANK_ADD':'客户存款和同业存放款项净增加额',\
        'RECEIVE_INTEREST_COMMISSION':'收取利息、手续费及佣金的现金','RECEIVE_OTHER_OPERATE':'收到其他与经营活动有关的现金',\
        'TOTAL_OPERATE_INFLOW':'经营活动现金流入小计','BUY_SERVICES':'购买商品、接受劳务支付的现金',\
        'OBTAIN_SUBSIDIARY_OTHER':'取得子公司及其他营业单位支付的现金净额','ACCEPT_INVEST_CASH':'吸收投资收到的现金',\
        'SUBSIDIARY_ACCEPT_INVEST':'其中:子公司吸收少数股东投资收到的现金','RECEIVE_OTHER_FINANCE':'收到的其他与筹资活动有关的现金',\
        'LOAN_ADVANCE_ADD':'客户贷款及垫款净增加额','PBC_INTERBANK_ADD':'存放中央银行和同业款项净增加额',\
        'PAY_INTEREST_COMMISSION':'支付利息、手续费及佣金的现金','PAY_STAFF_CASH':'支付给职工以及为职工支付的现金',\
        'PAY_ALL_TAX':'支付的各项税费','PAY_OTHER_OPERATE':'支付其他与经营活动有关的现金','OPERATE_OUTFLOW_OTHER':'经营活动现金流出的其他项目',\
        'TOTAL_OPERATE_OUTFLOW':'经营活动现金流出小计','NETCASH_OPERATE':'经营活动产生的现金流量净额',\
        'WITHDRAW_INVEST':'收回投资收到的现金','RECEIVE_INVEST_INCOME':'取得投资收益收到的现金','TOTAL_FINANCE_INFLOW':'筹资活动现金流入小计',\
        'DISPOSAL_LONG_ASSET':'处置固定资产、无形资产和其他长期资产收回的现金净额','RECEIVE_TAX_REFUND':'收到的税收返还',\
        'RECEIVE_OTHER_INVEST':'收到的其他与投资活动有关的现金','TOTAL_INVEST_INFLOW':'投资活动现金流入小计',\
        'CONSTRUCT_LONG_ASSET':'购建固定资产、无形资产和其他长期资产支付的现金','INVEST_PAY_CASH':'投资支付的现金',\
        'PAY_OTHER_INVEST':'支付其他与投资活动有关的现金','TOTAL_INVEST_OUTFLOW':'投资活动现金流出小计',\
        'NETCASH_INVEST':'投资活动产生的现金流量净额','ASSIGN_DIVIDEND_PORFIT':'分配股利、利润或偿付利息支付的现金',\
        'SUBSIDIARY_PAY_DIVIDEND':'其中:子公司支付给少数股东的股利、利润','PAY_OTHER_FINANCE':'支付的其他与筹资活动有关的现金',\
        'TOTAL_FINANCE_OUTFLOW':'筹资活动现金流出小计','NETCASH_FINANCE':'筹资活动产生的现金流量净额',\
        'RATE_CHANGE_EFFECT':'汇率变动对现金及现金等价物的影响','CCE_ADD':'现金及现金等价物净增加额','ASSET_IMPAIRMENT':'资产减值准备',\
        'BEGIN_CCE':'加:期初现金及现金等价物余额','END_CCE':'期末现金及现金等价物余额','NETPROFIT':'净利润',\
        'FA_IR_DEPR':'固定资产和投资性房地产折旧','OILGAS_BIOLOGY_DEPR':'其中:固定资产折旧、油气资产折耗、生产性生物资产折旧',\
        'IA_AMORTIZE':'无形资产摊销','LPE_AMORTIZE':'长期待摊费用摊销','DISPOSAL_LONGASSET_LOSS':'处置固定资产、无形资产和其他长期资产的损失',\
        'FA_SCRAP_LOSS':'固定资产报废损失','FAIRVALUE_CHANGE_LOSS':'公允价值变动损失','FINANCE_EXPENSE':'财务费用',\
        'INVEST_LOSS':'投资损失','DEFER_TAX':'递延所得税','DT_ASSET_REDUCE':'其中:递延所得税资产减少',\
        'DT_LIAB_ADD':'递延所得税负债增加','INVENTORY_REDUCE':'存货的减少','OPERATE_RECE_REDUCE':'经营性应收项目的减少',\
        'OPERATE_PAYABLE_ADD':'经营性应付项目的增加','NETCASH_OPERATENOTE':'经营活动产生的现金流量净额',\
        'END_CASH':'现金的期末余额','BEGIN_CASH':'减:现金的期初余额','CCE_ADDNOTE':'现金及现金等价物的净增加额'},inplace=True)
        data = data.reset_index()
        for i in range(len(data)):
            if data[1][i]==None:
                data.drop(labels=[i],inplace=True)
        for i in range(len(data.columns)-1):
            data=data.rename(columns={i:data[i][7]})
        data.drop(labels=range(0,12),inplace=True)
        self.stock_data1 = data.reset_index(drop=True)
        self.model2=modelAnalysisTable.AnalysisTable(self.stock_data1)

    def get_time_share_tick(self,num,code):
        import urllib.request
        url='http://16.push2.eastmoney.com/api/qt/stock/details/sse?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-0&secid={num}.{code}'.format(num=num,code=code)
        myURL=urllib.request.urlopen(url=url)
        data=myURL.readline().decode().lstrip('data:')
        df=pd.DataFrame(eval(data)['data'])
        df=df['details'].str.split(',',expand=True)
        for i in range(len(df)):
            if df[4][i]=='1':
                df[4][i]='B'
            elif df[4][i]=='2':
                df[4][i]='S'
        self.time_share=df.rename(columns={0:'time',1:'price',2:'trade',3:'vol',4:'direction'})

        self.model3=modelTimeShare.TimeShare(self.time_share)

    def init_ui(self):
        self.stock_data.sort_values(by=self.stock_data.columns[self.pre_index] , ascending=not self.sort_bool[self.pre_index],kind="mergesort",inplace=True)
        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)

        self.model = modelTableStock.ModelTableStock(self.stock_data)
        if globalVariable.getValue()==1:
            self.model_rising_speed=modelTableStock.ModelTableStock(self.rising_speed_data)
            self.model_my_stock=modelTableStock.ModelTableStock(self.my_stock_data)

    def reflash_my_stock(self):
        self.model_my_stock=modelTableStock.ModelTableStock(self.my_stock_data)
        self.view_my_stock.setModel(self.model_my_stock)

    def reflashView3(self):
        self.view3.horizontalHeader().hide()
        self.view3.verticalHeader().hide()
        self.view3.setColumnWidth(0,70)
        self.view3.setColumnWidth(1,70)
        self.view3.setColumnWidth(2,10)
        self.view3.setColumnWidth(3,10)
        self.view3.setColumnWidth(4,10)
        self.view3.setModel(self.model3)

    def reflashView2(self):
        self.view2.setModel(self.model2)
        self.view2.resizeColumnsToContents()

    def reflashView(self):
        if globalVariable.getValue()==1:
#            if self.stock_data.shape[1]<self.pre_index:
#                self.pre_index=3
#            self.stock_data.sort_values(by=self.stock_data.columns[self.pre_index] , ascending=not self.sort_bool[self.pre_index],kind="mergesort",inplace=True)
#            self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
            self.view_rising_speed.setModel(self.model_rising_speed)
            self.view_my_stock.setModel(self.model_my_stock)
        self.view.setModel(self.model)

        if globalVariable.PreInterface!=globalVariable.getValue():
            if globalVariable.PreInterface==0:
                globalVariable.PreInterface=1
        self.setViewWidth()

    def setViewWidth(self):
        #self.view.verticalHeader().setDefaultSectionSize(10)
        #self.view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        #self.view.resizeColumnsToContents()
        if globalVariable.getValue()==5 or globalVariable.getValue()==2:
            self.view.setColumnWidth(0,80)
            self.view.setColumnWidth(1,200)
            self.view.setColumnWidth(2,70)
            self.view.setColumnWidth(3,70)
            self.view.setColumnWidth(4,60)
            self.view.setColumnWidth(5,80)
            self.view.setColumnWidth(6,65)
            self.view.setColumnWidth(7,80)
            self.view.setColumnWidth(8,90)
            self.view.setColumnWidth(9,90)
            self.view.setColumnWidth(10,70)
            self.view.setColumnWidth(11,70)
            self.view.setColumnWidth(12,70)
            self.view.setColumnWidth(13,70)
            self.view.setColumnWidth(14,70)
            self.view.setColumnWidth(15,70)
            self.view.setColumnWidth(16,70)

        elif globalVariable.getValue()==1:
            self.view.setColumnWidth(0,70)
            self.view.setColumnWidth(1,95)
            self.view.setColumnWidth(2,70)
            self.view.setColumnWidth(3,70)
            self.view.setColumnWidth(4,60)
            self.view.setColumnWidth(5,85)
            self.view.setColumnWidth(6,65)
            self.view.setColumnWidth(7,70)
            self.view.setColumnWidth(8,90)
            self.view.setColumnWidth(9,90)
            self.view.setColumnWidth(10,70)
            self.view.setColumnWidth(11,70)
            self.view.setColumnWidth(12,70)
            self.view.setColumnWidth(13,70)
            self.view.setColumnWidth(14,70)
            self.view.setColumnWidth(15,70)
            self.view.setColumnWidth(16,70)
            self.view_rising_speed.setColumnWidth(0,70)
            self.view_rising_speed.setColumnWidth(1,95)
            self.view_rising_speed.setColumnWidth(2,60)
            self.view_rising_speed.setColumnWidth(3,60)
            self.view_rising_speed.setColumnWidth(4,60)
            self.view_rising_speed.setColumnWidth(5,85)
            self.view_rising_speed.setColumnWidth(6,65)
            self.view_rising_speed.setColumnWidth(7,70)
            self.view_rising_speed.setColumnWidth(8,90)
            self.view_rising_speed.setColumnWidth(9,90)
            self.view_rising_speed.setColumnWidth(10,70)
            self.view_rising_speed.setColumnWidth(11,70)
            self.view_rising_speed.setColumnWidth(12,70)
            self.view_rising_speed.setColumnWidth(13,70)
            self.view_rising_speed.setColumnWidth(14,70)
            self.view_rising_speed.setColumnWidth(15,70)
            self.view_rising_speed.setColumnWidth(16,70)
            self.view_my_stock.setColumnWidth(0,70)
            self.view_my_stock.setColumnWidth(1,95)
            self.view_my_stock.setColumnWidth(2,70)
            self.view_my_stock.setColumnWidth(3,60)
            self.view_my_stock.setColumnWidth(4,60)
            self.view_my_stock.setColumnWidth(5,85)
            self.view_my_stock.setColumnWidth(6,65)
            self.view_my_stock.setColumnWidth(7,70)
            self.view_my_stock.setColumnWidth(8,90)
            self.view_my_stock.setColumnWidth(9,90)
            self.view_my_stock.setColumnWidth(10,70)
            self.view_my_stock.setColumnWidth(11,70)
            self.view_my_stock.setColumnWidth(12,70)
            self.view_my_stock.setColumnWidth(13,70)
            self.view_my_stock.setColumnWidth(14,70)
            self.view_my_stock.setColumnWidth(15,70)
            self.view_my_stock.setColumnWidth(16,70)
        elif globalVariable.getValue()==4:
            if globalVariable.isBoardWidth:
                self.view.setColumnWidth(0,70)
                self.view.setColumnWidth(1,95)
                self.view.setColumnWidth(2,70)
                self.view.setColumnWidth(3,70)
                self.view.setColumnWidth(4,60)
                self.view.setColumnWidth(5,80)
                self.view.setColumnWidth(6,65)
                self.view.setColumnWidth(7,70)
                self.view.setColumnWidth(8,90)
                self.view.setColumnWidth(9,90)
                self.view.setColumnWidth(10,70)
                self.view.setColumnWidth(11,70)
                self.view.setColumnWidth(12,70)
                self.view.setColumnWidth(13,70)
                self.view.setColumnWidth(14,70)
                self.view.setColumnWidth(15,70)
                self.view.setColumnWidth(16,70)
            else:
                self.view.setColumnWidth(0,120)
                self.view.setColumnWidth(1,100)
                self.view.setColumnWidth(2,100)
                self.view.setColumnWidth(3,100)
                self.view.setColumnWidth(4,100)
                self.view.setColumnWidth(5,120)
                self.view.setColumnWidth(6,100)
                self.view.setColumnWidth(7,100)
                self.view.setColumnWidth(8,100)
                self.view.setColumnWidth(9,100)
                self.view.setColumnWidth(10,100)
                self.view.setColumnWidth(11,100)
                self.view.setColumnWidth(12,150)
    #            self.view.resizeColumnsToContents()

    def stock_sort(self,index):
        self.stock_data.sort_values(by=self.stock_data.columns[index] , ascending=self.sort_bool[index],kind="mergesort",inplace=True)

        if self.pre_index!=index:
            self.sort_bool[self.pre_index]=False
            self.pre_index=index
        self.sort_bool[index]=not self.sort_bool[index]

        self.stock_data.index = pd.RangeIndex(start=1, stop=len(self.stock_data)+1, step=1)
        if globalVariable.getValue()==2 or globalVariable.getValue()==5 or globalVariable.getValue()==1:
            self.model = modelTableStock.ModelTableStock(self.stock_data)
        else:
            if globalVariable.subCount==4:
                if globalVariable.isBoardWidth:
                    self.model = modelTableStock.ModelTableStock(self.stock_data)
                else:
                    self.stock_data1.sort_values(by=self.stock_data1.columns[index] , ascending=self.sort_bool[index],kind="mergesort",inplace=True)
                    self.stock_data1.index = pd.RangeIndex(start=1, stop=len(self.stock_data1)+1, step=1)
                    self.model = modelAnalysisTable.AnalysisTable(self.stock_data1)
            else:
                self.model = modelAnalysisTable.AnalysisTable(self.stock_data)
        self.view.setModel(self.model)
        #self.view.show()


