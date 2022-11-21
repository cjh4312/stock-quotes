# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import requests
import pandas as pd
import re
import json
import jsonpath
import math
from pandas.core.frame import DataFrame
import urllib.request

class WorldIndex():
    def __init__(self):
        super().__init__()
        self.data=pd.DataFrame()
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}

    def getAsiaIndex(self):
        url='http://78.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124009704245904437836_1662797945416&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=7111416627128474|0|1|0|web&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1662797945419'
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',data)[0]
        json_data=json.loads(json_data)
        total=jsonpath.jsonpath(json_data,'$..total')[0]
        page=math.ceil(total/20)
        worldIndex=pd.DataFrame(columns=['名称','最新价','涨跌幅'])
        j=0
        for i in range(1,page+1):
            url='http://78.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124009704245904437836_1662797945416&pn={}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=7111416627128474|0|1|0|web&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1662797945419'.format(i)
            data=requests.get(url,headers=self.headers).content.decode()
            j+=1
            new_json_data=re.findall('{"rc":.*}]}}',data)[0]

            json_data=json.loads(new_json_data)
            name=jsonpath.jsonpath(json_data,'$..f14')
            new_price=jsonpath.jsonpath(json_data,'$..f2')
            up_and_down=jsonpath.jsonpath(json_data,'$..f3')
            for i,name in enumerate(name):
                worldIndex.loc[len(worldIndex)]=[name,new_price[i],up_and_down[i]]
        worldIndex.sort_values(by=worldIndex.columns[0],inplace=True)
        #worldIndex.index = pd.RangeIndex(start=1, stop=len(worldIndex)+1, step=1)
        return worldIndex

    def getAllIndex(self):
        url='http://2.push2.eastmoney.com/api/qt/ulist.np/get?fid=f3&pi=0&pz=40&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&fields=f14,f12,f2,f3&np=1&cb=jQuery112405358253239357542_1662857186397&secids=1.000001%2C0.399001%2C0.399006%2C100.HSI%2c100.TWII%2C100.N225%2C100.KS11%2C100.SENSEX%2C100.DJIA%2C100.SPX%2C100.NDX%2C100.FTSE%2C100.GDAXI%2C100.FCHI%2C100.RTS%2C100.AS51%2C1.000688&_=1662857186403'
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',data)[0]
        data=DataFrame(json.loads(json_data)['data']['diff'])
        data['f2']=data['f2'].astype(float)
        for i in range(len(data)):
            if not data.loc[i,'f12'].isdigit():
                data.loc[i,'f12']='100.'+data.loc[i,'f12']
            if data.loc[i,'f12'][0:1]=='0':
                data.loc[i,'f12']='sh.'+data.loc[i,'f12']
        return data

    def get_futures_data(self):
        url='http://futsseapi.eastmoney.com/list/block?cb=aaa_financial&orderBy=zdf&sort=desc&pageSize=20&pageIndex=0&callbackName=aaa_financial&blockName=financial&_=1666243575249'
        request =urllib.request.Request(url,headers=self.headers)
        myURL=urllib.request.urlopen(request)
        data=myURL.readline().decode().lstrip('aaa_financial:')
        df=pd.DataFrame(eval(data)['list'])
        df=df[['name','p','zdf']]
#        df.sort_values(by=df.columns[0],ascending=False,kind="mergesort",inplace=True)
#        df.index = pd.RangeIndex(start=0, stop=len(df), step=1)
        return df

    def get_time_share2(self,code):
        from http.client import HTTPConnection
        http_conn=HTTPConnection('119.3.12.115',80)
        params="/api/qt/stock/details/sse?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-0&secid=0.{}".format(code)
        headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip,deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Host":"97.push2.eastmoney.com",
        "Pragma":"no-cache",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/101.0.4951.67Safari/537.36"
        }
        http_conn.request("GET",params,headers=headers)

        with http_conn.getresponse() as response:
            while (not response.closed):
                for line in response:
                    print(line.decode("utf-8"))

    def get_time_share_tick(self,num,code):
        url='http://16.push2.eastmoney.com/api/qt/stock/details/sse?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-0&secid={num}.{code}'.format(num=num,code=code)
        request =urllib.request.Request(url,headers=self.headers)
        myURL=urllib.request.urlopen(request)
        data=myURL.readline().decode().lstrip('data:')
        d=json.loads(data)['data']
        pre_close=d['prePrice']
        self.data=d['details']
        return (pre_close,self.data)

    def get_us_time_share_tick(self,code):
        url ="http://push2.eastmoney.com/api/qt/stock/details/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&secid={}&pos=-30&cb=jQuery35106760235398818608_1666406840174&_=1666406840175".format(code)
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*]}}',data)[0]
        json_data=json.loads(json_data)
        preClose=float(json_data['data']['prePrice'])
        data_list=json_data['data']['details']
        return (preClose,data_list)

    def get_time_share_chart_data(self,num,code):
        url='http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={num}.{code}&ndays=1&iscr=0&iscca=0&cb=jsonp1664162734310:formatted'.format(num=num,code=code)
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*]}}',data)[0]
        json_data=json.loads(json_data)
        preClose=float(json_data['data']['preClose'])
        data_list=json_data['data']['trends']
        return (preClose,data_list)

    def get_us_hk_time_share_chart(self,code):
        url ="http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&iscr=0&ndays=1&secid={}&cb=jQuery35104150357359209882_1666401553892&_=1666401553893".format(code)
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*]}}',data)[0]
        json_data=json.loads(json_data)
        preClose=float(json_data['data']['preClose'])
        data_list=json_data['data']['trends']
        return (preClose,data_list)

    def get_index_time_share_chart(self,code):
        url='http://push2.eastmoney.com/api/qt/stock/trends2/get?secid={}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=e1e6871893c6386c5ff6967026016627&iscr=0&cb=cb_1665213076163_70435755&isqhquote=&cb_1665213076163_70435755'.format(code)
        data=requests.get(url,headers=self.headers).content.decode()
        json_data=re.findall('{"rc":.*]}}',data)[0]
        json_data=json.loads(json_data)
        preClose=float(json_data['data']['preClose'])
        data_list=json_data['data']['trends']
        return (preClose,data_list)

    def get_time_share_chart_data5(self,num,code):
        url5='http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={num}.{code}&ndays=5&iscr=0&iscca=0&cb=jsonp1664202838782'.format(num=num,code=code)
        data5=requests.get(url5,headers=self.headers).text
        json_data=json.loads(re.findall(r'\((.*)\);', data5)[0])
        preClose=float(json_data['data']['preClose'])
        data_list=json_data['data']['trends']
        return (preClose,data_list)

    def get_market_activity_data(self):
        url='https://legulegu.com/stockdata/market-activity-trend-data?token=a44e82a91eb64a73f1b945dfa21c7ce0'
        df=requests.get(url,headers=self.headers).content.decode()
        data=DataFrame(json.loads(df))
        return (data['totalUp'][len(data)-1],data['totalDown'][len(data)-1])
