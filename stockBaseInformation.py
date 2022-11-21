# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import pandas as pd
import pinyin

class StockBaseInformation():
    def __init__(self,stock_code,name,industry):
        self.stock_code=stock_code
        self.name=name
        self.industry=industry

    def initCode(self):
        if(str(self.stock_code)[0] == '6'):
            self.stock_code = 'sh.'+str(self.stock_code)
        if(str(self.stock_code)[0] in ['0','3']):
            self.stock_code = 'sz.'+str(self.stock_code)

    def get_pinyin_to_code(self):
        stock=pd.read_csv('e:/cjh/Documents/python_stock/stock_industry.csv',encoding="gbk")
        for index,row in stock.iterrows():
            lst = list(row['code_name'])
            charLst = []
            for l in lst:
                if l >= u'\u4e00' and l <= u'\u9fa5':
                    charLst.append(pinyin.get(l)[0])
                else:
                    charLst.append(l)
            if ''.join(charLst)==self.stock_code:
                self.stock_code=row['code']
                self.name=row['code_name']
                self.industry='--'+str(row['industry'])
                if self.industry=='--nan':
                    self.industry=''
                return
        self.name='666'

    def from_pinyin_to_code(self):
        stock=pd.read_csv('e:/cjh/Documents/python_stock/stock_industry.csv',encoding="gbk")
        for index,row in stock.iterrows():
            if self.getPinyin(row['code_name'])==self.code_text.text():

                self.stock_code=row['code']
                self.name=row['code_name']
                self.industry='--'+str(row['industry'])
                if self.industry=='--nan':
                    self.industry=''
                return (self.name,self.industry)
        self.name='666'
        return self.name

    def getNameIndustry(self):
        stock=pd.read_csv('e:/cjh/Documents/python_stock/stock_industry.csv',encoding="gbk")
        n=len(stock)
        l=0
        r=n-1
        while l<=r:
            mid=(l+r)//2
            if stock.loc[mid].iloc[0]==self.stock_code:
                #self.stock_code=str(stock.loc[mid].iloc[0])
                (self.name,self.industry)=(str(stock.loc[mid].iloc[1]),'--'+str(stock.loc[mid].iloc[2]))
                if self.industry=='--nan':
                    self.industry=''
                return (self.name,self.industry)
            elif stock.loc[mid].iloc[0]>self.stock_code:
                r=mid-1
            else:
                l=mid+1
        self.name='666'
        return self.name

    def single_get_first(self,unicode1):
        str1 = unicode1.encode('gbk')
        try:
            ord(str1)
            return str1
        except:
            asc = str1[0] * 256 + str1[1]
            if asc >= 45217 and asc <= 45252:
                return 'a'
            if asc >= 45253 and asc <= 45760:
                return 'b'
            if asc >= 45761 and asc <= 46317:
                return 'c'
            if asc >= 46318 and asc <= 46825:
                return 'd'
            if asc >= 46826 and asc <= 47009:
                return 'e'
            if asc >= 47010 and asc <= 47296:
                return 'f'
            if asc >= 47297 and asc <= 47613:
                return 'g'
            if asc >= 47614 and asc <= 48118:
                return 'h'
            if asc >= 48119 and asc <= 49061:
                return 'j'
            if asc >= 49062 and asc <= 49323:
                return 'k'
            if asc >= 49324 and asc <= 49895:
                return 'l'
            if asc >= 49896 and asc <= 50370:
                return 'm'
            if asc >= 50371 and asc <= 50613:
                return 'n'
            if asc >= 50614 and asc <= 50621:
                return 'o'
            if asc >= 50622 and asc <= 50905:
                return 'p'
            if asc >= 50906 and asc <= 51386:
                return 'q'
            if asc >= 51387 and asc <= 51445:
                return 'r'
            if asc >= 51446 and asc <= 52217:
                return 's'
            if asc >= 52218 and asc <= 52697:
                return 't'
            if asc >= 52698 and asc <= 52979:
                return 'w'
            if asc >= 52980 and asc <= 53688:
                return 'x'
            if asc >= 53689 and asc <= 54480:
                return 'y'
            if asc >= 54481 and asc <= 55289:
                return 'z'
            return ''

    def getPinyin(self,string):
        if string == None:
            return None
        lst = list(string)
        charLst = []
        for l in lst:
            if l >= u'\u4e00' and l <= u'\u9fa5':
                charLst.append(self.single_get_first(l))
            else:
                charLst.append(l)
        return ''.join(charLst)
