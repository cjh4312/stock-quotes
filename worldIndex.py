# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import requests
import pandas as pd
from memory_profiler import profile
class WorldIndex():
    def __init__(self):
        super().__init__()
        self.data=pd.DataFrame()
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}

    def getAllIndex(self):
        url='http://push2.eastmoney.com/api/qt/ulist.np/get?fid=f3&pi=0&pz=40&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&fields=f14,f12,f2,f3&np=1&secids=1.000001%2C0.399001%2C0.399006%2C100.HSI%2c100.TWII%2C100.N225%2C100.KS11%2C100.SENSEX%2C100.DJIA%2C100.SPX%2C100.NDX%2C100.FTSE%2C100.GDAXI%2C100.FCHI%2C100.RTS%2C100.AS51%2C1.000688&_=1662857186403'
        data=pd.DataFrame(requests.get(url,headers=self.headers,timeout=3).json()['data']['diff'])
        data['f2']=data['f2'].astype(float)
        for i in range(len(data)):
            if not data.loc[i,'f12'].isdigit():
                data.loc[i,'f12']='100.'+data.loc[i,'f12']
            if data.loc[i,'f12'][0:1]=='0':
                data.loc[i,'f12']='sh.'+data.loc[i,'f12']
        return data

    def get_futures_data(self):
        url='http://futsseapi.eastmoney.com/list/block?orderBy=name&sort=desc&pageSize=20&pageIndex=0&blockName=financial&_=1666243575249'
        df=pd.DataFrame(requests.get(url,headers=self.headers,timeout=3).json()['list'])
        df=df[['name','p','zdf']]
#        df.sort_values(by=df.columns[0],ascending=False,kind="mergesort",inplace=True)
#        df.index = pd.RangeIndex(start=0, stop=len(df), step=1)
        return df

    def get_time_share_tick(self,num,code):
        url='http://push2.eastmoney.com/api/qt/stock/details/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-0&secid={num}.{code}'.format(num=num,code=code)
        df =requests.get(url,headers=self.headers,timeout=0.3).json()['data']
        pre_close=df['prePrice']
        self.data=df['details']
        return (pre_close,self.data)

    def get_us_time_share_tick(self,code):
        url ="http://push2.eastmoney.com/api/qt/stock/details/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&secid={}&pos=-30&_=1666406840175".format(code)
        json_data=requests.get(url,headers=self.headers).json()['data']
        preClose=json_data['prePrice']
        data_list=json_data['details']
        return (preClose,data_list)

#    def get_time_share_chart_data(self,num,code):
#        url='http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={num}.{code}&ndays=1&iscr=0&iscca=0:formatted'.format(num=num,code=code)
#        json_data=requests.get(url,headers=self.headers).json()['data']
#        preClose=json_data['preClose']
#        data_list=json_data['trends']
#        return (preClose,data_list)

    def get_time_share_chart_data5(self,num,code):
        url5='http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={num}.{code}&ndays=5&iscr=0&iscca=0'.format(num=num,code=code)
        json_data=requests.get(url5,headers=self.headers,timeout=3).json()['data']
        preClose=json_data['preClose']
        data_list=json_data['trends']
        return (preClose,data_list)

    def get_us_hk_time_share_chart(self,code):
        url ="http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&iscr=0&ndays=1&secid={}&_=1666401553893".format(code)
        json_data=requests.get(url,headers=self.headers).json()['data']
        preClose=json_data['preClose']
        data_list=json_data['trends']
        return (preClose,data_list)

    def get_index_time_share_chart(self,code):
        url='http://push2.eastmoney.com/api/qt/stock/trends2/get?secid={}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=e1e6871893c6386c5ff6967026016627&iscr=0&isqhquote=&cb_1665213076163_70435755'.format(code)
        json_data=requests.get(url,headers=self.headers).json()['data']
        preClose=json_data['preClose']
        data_list=json_data['trends']
        return (preClose,data_list)
