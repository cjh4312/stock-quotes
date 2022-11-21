# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import tushare as ts
import pandas as pd
from xpinyin import Pinyin
import requests
import json
import re
from pandas.core.frame import DataFrame

class StockInformation():
    def __init__(self):
        super().__init__()

    def download(self):
        #self.deal_with_index_list()
        self.deal_with_concept_industry()
        self.deal_with_stock_list()

    def deal_with_stock_list(self):
        pro = ts.pro_api('bbe1d68e9a152f87296960ffd981449ed98fff7cfd13b3cf2a50be79')

        #查询当前所有正常上市交易的股票列表

        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        data.sort_values(by=data.columns[0],ascending=True,inplace=True)
        data.index = pd.RangeIndex(start=0, stop=len(data), step=1)
        data.to_csv('list/stock_list.csv',encoding="gbk")
        data1=pd.read_csv('list/abbreviation_index_list.csv',encoding="gbk")
        data1.sort_values(by=data1.columns[0],ascending=True,inplace=True)
        data2=pd.read_csv('list/concept_industry_board.csv',encoding="gbk")
        data2.sort_values(by=data2.columns[0],ascending=True,inplace=True)

        data1=data1[['symbol','name','abbreviation']]
        data2=data2[['symbol','name','abbreviation']]
        for row in range(len(data)):
            #name=globalVariable.getPinyin(data.loc[row,'name'])
            data.loc[row,'abbreviation']=self.get_pinyin_to_abbreviation(data.loc[row,'name'])

        data=pd.concat([data2,data1,data])
        data.sort_values(by=data.columns[2],ascending=True,inplace=True)
        data.index = pd.RangeIndex(start=1, stop=len(data)+1, step=1)
        data.to_csv('list/abbreviation_list.csv',encoding="gbk")

        #print('个股处理完毕')

    def deal_with_index_list(self):
        data = pd.read_html("https://www.joinquant.com/data/dict/indexData")[0]
        data["指数代码"] = data["指数代码"].str.split(".", expand=True)[0]
        data.columns = ["index_code", "display_name", "publish_date", "-", "-"]
        for i in range(len(data)):
            if data.loc[i,'index_code'][0:3]!='399':
                data.loc[i,'index_code']='sh.'+data.loc[i,'index_code']
        data.to_csv('list/index.csv',encoding="gbk")
        for row in range(len(data)):
            #name=globalVariable.getPinyin(data.loc[row,'display_name'])
            data.loc[row,'abbreviation']=self.get_pinyin_to_abbreviation(data.loc[row,'display_name'])
        data.rename(columns={'display_name':'name','index_code':'symbol'},inplace=True)
        data.sort_values(by=data.columns[3],ascending=True,inplace=True)
        data.index = pd.RangeIndex(start=1, stop=len(data)+1, step=1)
        data.to_csv('list/abbreviation_index_list.csv',encoding="gbk")
        print('指数处理完毕')

    def deal_with_concept_industry(self):
        data=self.stock_board_concept_name_em()
        data=data[['板块代码','板块名称']]
        data.rename(columns={'板块名称':'name','板块代码':'symbol'},inplace=True)
        data1=self.stock_board_industry_name_em()
        data1=data1[['板块代码','板块名称']]
        data1.rename(columns={'板块名称':'name','板块代码':'symbol'},inplace=True)
        url='http://72.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405348481540249999_1665566741506&pn=1&pz=20&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:90+t:1+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1665566741514'
        url1='http://72.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405348481540249999_1665566741506&pn=2&pz=20&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:90+t:1+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1665566741514'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        df=requests.get(url,headers=headers).content.decode()
        df1=requests.get(url1,headers=headers).content.decode()
        json_data=re.findall('{"rc":.*}]}}',df)[0]
        json_data1=re.findall('{"rc":.*}]}}',df1)[0]
        data2=DataFrame(json.loads(json_data)['data']['diff'])
        data3=DataFrame(json.loads(json_data1)['data']['diff'])
        data2=data2[['f12','f14']]
        data2.rename(columns={'f12':'symbol','f14':'name'},inplace=True)
        data3=data3[['f12','f14']]
        data3.rename(columns={'f12':'symbol','f14':'name'},inplace=True)
        data=pd.concat([data,data1,data2,data3])

        data.index = pd.RangeIndex(start=0, stop=len(data), step=1)
        for row in range(len(data)):
            #name=globalVariable.getPinyin(data.loc[row,'display_name'])
            data.loc[row,'abbreviation']=self.get_pinyin_to_abbreviation(data.loc[row,'name'])
        data.sort_values(by=data.columns[2],ascending=True,inplace=True)
        data.index = pd.RangeIndex(start=1, stop=len(data)+1, step=1)
        data.to_csv('list/concept_industry_board.csv',encoding='gbk')
        #print('板块处理完毕')

    def get_pinyin_to_abbreviation(self,stock):
        p=Pinyin()
        result1=p.get_pinyin(stock)
        l=[]
        s=result1.split('-')
        for i in range(len(s)):
            if len(s[i])==0:
                continue
            for j in range(len(s[i])):
                    if not s[i][j].islower():
                        l.append(''.join(s[i]).lower())
                        break
                    if j==len(s[i])-1:
                        l.append(''.join(s[i][0]))
                        continue
        return ''.join(l)

    def stock_board_concept_name_em(self):
        """
        东方财富网-沪深板块-概念板块-名称
        http://quote.eastmoney.com/center/boardlist.html#concept_board
        :return: 概念板块-名称
        :rtype: pandas.DataFrame
        """
        url = "http://79.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "2000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:90 t:3 f:!50",
            "fields": "f2,f3,f4,f8,f12,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22,f33,f11,f62,f128,f124,f107,f104,f105,f136",
            "_": "1626075887768",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        temp_df.columns = [
            "排名",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "换手率",
            "_",
            "板块代码",
            "板块名称",
            "_",
            "_",
            "_",
            "_",
            "总市值",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "上涨家数",
            "下跌家数",
            "_",
            "_",
            "领涨股票",
            "_",
            "_",
            "领涨股票-涨跌幅",
        ]
        temp_df = temp_df[
            [
                "排名",
                "板块名称",
                "板块代码",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "总市值",
                "换手率",
                "上涨家数",
                "下跌家数",
                "领涨股票",
                "领涨股票-涨跌幅",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["上涨家数"] = pd.to_numeric(temp_df["上涨家数"], errors="coerce")
        temp_df["下跌家数"] = pd.to_numeric(temp_df["下跌家数"], errors="coerce")
        temp_df["领涨股票-涨跌幅"] = pd.to_numeric(temp_df["领涨股票-涨跌幅"], errors="coerce")
        return temp_df

    def stock_board_industry_name_em(self):
        """
        东方财富网-沪深板块-行业板块-名称
        http://quote.eastmoney.com/center/boardlist.html#industry_board
        :return: 行业板块-名称
        :rtype: pandas.DataFrame
        """
        url = "http://17.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "2000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:90 t:2 f:!50",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222",
            "_": "1626075887768",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = temp_df.index + 1
        temp_df.columns = [
            "排名",
            "-",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "-",
            "_",
            "-",
            "换手率",
            "-",
            "-",
            "-",
            "板块代码",
            "-",
            "板块名称",
            "-",
            "-",
            "-",
            "-",
            "总市值",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "上涨家数",
            "下跌家数",
            "-",
            "-",
            "-",
            "领涨股票",
            "-",
            "-",
            "领涨股票-涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "板块名称",
                "板块代码",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "总市值",
                "换手率",
                "上涨家数",
                "下跌家数",
                "领涨股票",
                "领涨股票-涨跌幅",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["上涨家数"] = pd.to_numeric(temp_df["上涨家数"], errors="coerce")
        temp_df["下跌家数"] = pd.to_numeric(temp_df["下跌家数"], errors="coerce")
        temp_df["领涨股票-涨跌幅"] = pd.to_numeric(temp_df["领涨股票-涨跌幅"], errors="coerce")
        return temp_df
