# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import pandas as pd
import datetime
import requests
from pandas.core.frame import DataFrame

class GetData():
    def __init__(self,code,freq,adjustflag):

        self.data=pd.DataFrame(columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn'])
        self.issave=True
        self.data_time_share=''
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        self.end_date=(datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y%m%d")
        self.login_init(code,freq,adjustflag)

    def login_init(self,code,freq,adjustflag):
        #print(code,freq)
#        area=''
#        if str(code)[0] in ['6','s']:
#            area = 'sh'
#        elif str(code)[0] in ['4','8']:
#            area = 'bj'
#        elif str(code)[0] in ['0','3']:
#            area = 'sz'
#        data1=pd.DataFrame(columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn'])
#        self.start_date=(datetime.date.today()+datetime.timedelta(days=-365)).strftime("%Y%m%d")
#        if freq=='weekly':
#            self.start_date=(datetime.date.today()+datetime.timedelta(days=-1260)).strftime("%Y%m%d")
#        elif freq=='monthly':
#            self.start_date=(datetime.date.today()+datetime.timedelta(days=-5400)).strftime("%Y%m%d")

        if code[0]=='3' or code[0]=='0' or code[0]=='8' or code[0]=='4':
            num=0
        else:
            num=1
        if (code[0]=='s' and code[2]=='.' and code[3].isdigit()) or code[0:3]=='399':
            if code[0]=='s' and code[2]=='.' and code[3].isdigit():
                code=code[3:9]
#            if os.path.exists('data/index/%s/%s/%s_%s.csv'
#                                    %(area,freq,code, freq)):
#                data1=pd.read_csv('data/index/%s/%s/%s_%s.csv'
#                                    %(area,freq,code, freq),encoding="gbk")
#                data1.drop(data1.columns[[0]],axis=1,inplace=True)
#                self.start_date='20221001'
#            self.data=ak.index_zh_a_hist(symbol=code,
#                                            start_date=self.start_date,
#                                            end_date=self.end_date,
#                                            period=freq)
#            if len(self.data)!=0:
#                self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
#            self.data=pd.concat([data1,self.data],ignore_index=True)

            adjust='0'
            self.get_zh_data_from_east(num,code,freq,adjust)
            self.deal_with_data(self.data)
        else:
            if code[0]=='S' and code[2].isdigit():
                code=code[2:8]
#            if os.path.exists('data/%s/%s/%s_%s.csv'
#                                        %(area,freq,code, freq)) and adjustflag=='' and freq=='daily':
#                    data1=pd.read_csv('data/%s/%s/%s_%s.csv'
#                                    %(area,freq,code, freq),encoding="gbk")
#                    data1.drop(data1.columns[[0]],axis=1,inplace=True)
#                    self.start_date='20221001'
            if code[0]=='3' or code[0]=='0' or code[0]=='8' or code[0]=='4':
                num=0
            else:
                num=1

            self.get_zh_data_from_east(num,code,freq,adjustflag)
            self.deal_with_data(self.data)

    def get_zh_data_from_east(self,num,code,freq,adjustflag):
        self.start_date=(datetime.date.today()+datetime.timedelta(days=-1080)).strftime("%Y%m%d")
        if freq=='102':
            self.start_date=(datetime.date.today()+datetime.timedelta(days=-5400)).strftime("%Y%m%d")
        elif freq=='103':
            self.start_date=(datetime.date.today()+datetime.timedelta(days=-20000)).strftime("%Y%m%d")
        url='http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg={}&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid={}.{}&klt={}&fqt={}'.format(self.start_date,num,code,freq,adjustflag)
        data_list=requests.get(url,headers=self.headers).json()['data']['klines']
        df=pd.DataFrame(data_list)
        self.data=df[0].str.split(',',expand = True)
        self.data.iloc[:,1:]=self.data.iloc[:,1:].astype(float)
        self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
        self.deal_with_data(self.data)

    def get_us_data_from_east(self,code,freq,adjustflag):
        day=1080
        url='http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt={}&fqt={}&end=20500101&lmt={}&_=1667035995818'.format(code,freq,adjustflag,day)
        data_list=requests.get(url,headers=self.headers).json()['data']['klines']
        df=pd.DataFrame(data_list)
        self.data=df[0].str.split(',',expand = True)
        self.data.iloc[:,1:]=self.data.iloc[:,1:].astype(float)
        self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
        self.deal_with_data(self.data)

    def get_hk_data_from_east(self,code,freq,adjustflag):
        self.start_date=(datetime.date.today()+datetime.timedelta(days=-1080)).strftime("%Y%m%d")
        if freq=='102':
            self.start_date=(datetime.date.today()+datetime.timedelta(days=-5400)).strftime("%Y%m%d")
        elif freq=='103':
            self.start_date=(datetime.date.today()+datetime.timedelta(days=-20000)).strftime("%Y%m%d")
        url='http://push2his.eastmoney.com/api/qt/stock/kline/get?secid=116.{}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt={}&fqt={}&beg={}&end=20500101&smplmt=860.818&lmt=1000000&_=1667037417533'.format(code,freq,adjustflag,self.start_date)
        data_list=requests.get(url,headers=self.headers).json()['data']['klines']
        df=pd.DataFrame(data_list)
        self.data=df[0].str.split(',',expand = True)
        self.data.iloc[:,1:]=self.data.iloc[:,1:].astype(float)
        self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
        self.deal_with_data(self.data)

    def deal_with_data(self,data):
        data['MA5'] = data['close'].rolling(window=5).mean()
        data['MA10'] = data['close'].rolling(window=10).mean()
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA60'] = data['close'].rolling(window=60).mean()

        data['VMA5'] = data['volume'].rolling(window=5).mean()/500
        data['VMA10'] = data['volume'].rolling(window=10).mean()/500

    def get_other_index(self,code,freq):
        days=1365
        url='http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={}&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&lmt={}&klt={}&fqt=1&end=30000101&ut=4f1862fc3b5e77c150a2b985b12db0fd&cb_1665195942532_53072773=cb_1665195942532_53072773'.format(code,days,freq)
        json_data=requests.get(url,headers=self.headers).json()['data']['klines']
        for i in range(len(json_data)):
            json_data[i]=json_data[i].split(',',11)
        self.data=pd.DataFrame(json_data)
        self.data.columns=['date','open','close','high','low','volume','amount','turn','pctChg','pctVal','amplitude']
        self.data.iloc[:,1:]=self.data.iloc[:,1:].astype(float)
        self.deal_with_data(self.data)

    def get_main_indicator_data(self,code):
        if code[0] == '6':
            stock_code = 'SH'+code
        elif code[0] in ['4','8']:
            stock_code = 'BJ'+code
        elif code[0] in ['0','3']:
            stock_code = 'SZ'+code
        url='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code={}'.format(stock_code)
        df=requests.get(url,headers=self.headers)
        data=DataFrame(df.json()['data'])
        data=data.T
        return data

#    def download_akshare_all_stock(self):
#        if globalVariable.getIsNet()==1 or self.issave==False:
#            print('网络未连接')
#            return
#        if globalVariable.isZhMarketDay():
#            print('请休市后下载')
#            return
#        if not os.path.exists('data/index/sh/daily'):
#            os.makedirs('data/index/sh/daily')
#        if not os.path.exists('data/index/sz/daily'):
#            os.makedirs('data/index/sz/daily')

#        if not os.path.exists('data/sh/daily'):
#            os.makedirs('data/sh/daily')
#        if not os.path.exists('data/sz/daily'):
#            os.makedirs('data/sz/daily')
#        if not os.path.exists('data/bj/daily'):
#            os.makedirs('data/bj/daily')

#        stock=pd.read_csv('list/index_list.csv',encoding="gbk",dtype={'index_code':str})
#        stock.drop(stock.columns[[0]],axis=1,inplace=True)
#        for row in range(0,len(stock)):
#            for freq in ['daily']:
#                code=stock.loc[row,'index_code']
#                if(str(code)[0] == '3'):
#                    area = 'sz'
#                else:
#                    area = 'sh'
#                if os.path.exists('data/index/%s/%s/%s_%s.csv'
#                                    %(area,freq,code, freq)):
#                    continue
#                else:
#                    self.start_date='19901219'
#                    self.end_date='20220930'

#                print('{:.2%}'.format(row/len(stock)))
#                print(code+' '+freq)
#                self.data=ak.index_zh_a_hist(symbol=code,
#                                                start_date=self.start_date,
#                                                end_date=self.end_date,
#                                                period=freq)
#                self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
#                self.data.to_csv('data/index/%s/%s/%s_%s.csv'
#                             %(area,freq,code, freq),encoding="gbk")
#        print('指数下载完毕')

#        stock=pd.read_csv('list/stock_list.csv',encoding="gbk",dtype={'symbol':str})
#        for row in range(0,len(stock)):
#            for freq in ['daily']:
#                code=stock.loc[row,'symbol']
#                if code=='430685':
#                    continue
#                if(str(code)[0] == '6'):
#                    area = 'sh'
#                elif(str(code)[0] in ['4','8']):
#                    area = 'bj'
#                elif(str(code)[0] in ['0','3']):
#                    area = 'sz'
#                if os.path.exists('data/%s/%s/%s_%s.csv'
#                                    %(area,freq,code, freq)):
#                    continue
#                else:
#                    self.start_date='19901219'
#                    self.end_date='20220930'
#                    #print(code,self.start_date,self.end_date)

#                print('{:.2%}'.format(row/len(stock)))
#                self.data=ak.stock_zh_a_hist(symbol=code,
#                                                start_date=self.start_date,
#                                                end_date=self.end_date,
#                                                period='daily',
#                                                adjust='0')
#                self.data.columns=['date','open','close','high','low','volume','amount','amplitude','pctChg','pctVal','turn']
#                self.data.to_csv('data/%s/%s/%s_%s.csv'
#                    %(area,freq,code, freq),encoding="gbk")
#                print(code+' '+freq)
#        print('个股下载完毕')
