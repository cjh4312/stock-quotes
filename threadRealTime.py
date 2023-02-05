# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread
import globalVariable
import pandas as pd
import requests

class RealTimeThread(QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()

    def __init__(self,parent):
        super(RealTimeThread, self).__init__()
        self.parent=parent

    def __del__(self):
        self.wait()

#    def get_time_share_tick_data(self):
#        code=self.parent.stock_code
#        self.isIndex=False
#        if code[0]=='3' or code[0]=='0' or code[0]=='8' or code[0]=='4':
#            num=0
#            if code[0:3]=='399':
#                self.isIndex=True
#        else:
#            num=1
#            if code[0]=='s' and code[2]=='.' and code[3].isdigit():
#                self.pre_stock_code=code
#                code=code[3:9]

#                self.isIndex=True
#        self.parent.tableView.get_time_share_tick(num,code)

    def get_time_share_tick_data(self):
        code=self.parent.stock_code
        self.data=pd.DataFrame()
        self.isIndex=False
        if code[0:4]=='100.' or code[0:4]=='103.' or code[0:4]=='104.' or not code[0:2].isdigit():
            self.parent.time_share_data=self.data
            self._signal.emit()
            return

        if globalVariable.marketNum==1 or globalVariable.marketNum==3:
            if code[0:4]=='105.' or code[0:4]=='106.' or code[0:4]=='107.':
                return
            if code[0]=='3' or code[0]=='0' or code[0]=='8' or code[0]=='4':
                num=0
                if code[0:3]=='399':
                    self.isIndex=True
            else:
                num=1
                if code[0]=='s' and code[2]=='.' and code[3].isdigit():
                    self.pre_stock_code=code
                    code=code[3:9]
                    self.isIndex=True
            (self.parent.pre_close,self.data)=self.parent.worldIndex.get_time_share_tick(num,code)
        elif globalVariable.marketNum==2 or globalVariable.marketNum==4:
            if code[0:4]=='105.' or code[0:4]=='106.' or code[0:4]=='107.':
                (self.parent.pre_close,self.data)=self.parent.worldIndex.get_us_time_share_tick(code)

    def deal_with_time_share_tick_data(self):
        self.parent.time_share_data=''
        j=0
        l=len(self.data)
        self.parent.price=[0]*l
        self.parent.price_len=[0]*l
        self.parent.flag_direction=[0]*l
        self.parent.flag_pos=[0]*(l+1)
        self.parent.line_len=[0]*(l+1)
        if not globalVariable.isZhMarketDay():
            self.parent.text_count=l
        elif l<14:
            self.parent.text_count=l
        else:
            self.parent.text_count=14
        for i in range(l-self.parent.text_count,l):
            ok=self.data[i].split(",", 5)
            if ok[4]=='2':
                flag='B'
            elif ok[4]=='1':
                flag='S'
            else:
                flag='  '
            a=len(ok[2])
            b=len(ok[3])
            if not self.isIndex:
                if i!=l-1:
                    self.parent.time_share_data=f"{self.parent.time_share_data}{'{0:<12}'.format(ok[0])}{ok[1]}  {format(ok[2], '>15')[a:15]}{flag}  {format(ok[3], '>8')[b:8]}\n"
                    self.parent.price[j]=float(ok[1])
                    self.parent.price_len[j]=len(ok[1])
                    self.parent.flag_direction[j]=int(ok[4])
                    j=j+1
                else:
                    self.parent.time_share_data=f"{self.parent.time_share_data}{'{0:<12}'.format(ok[0])}{ok[1]}  {format(ok[2], '>15')[a:15]}{flag}  {format(ok[3], '>8')[b:8]}"
                    self.parent.price[j]=float(ok[1])
                    self.parent.price_len[j]=len(ok[1])
                    self.parent.flag_direction[j]=int(ok[4])
                    self.parent.now_close=float(ok[1])
                    if self.parent.now_close<self.parent.pre_close:
                        self.parent.baseInformation.base_info['self.now_price_data'].setPalette(globalVariable.pegreen)
                        self.parent.baseInformation.base_info['self.pctChg_data'].setPalette(globalVariable.pegreen)
                    else:
                        self.parent.baseInformation.base_info['self.now_price_data'].setPalette(globalVariable.pered)
                        self.parent.baseInformation.base_info['self.pctChg_data'].setPalette(globalVariable.pered)
                    self.parent.baseInformation.base_info['self.now_price_data'].setText(str(self.parent.now_close))
                    self.parent.baseInformation.base_info['self.pctChg_data'].setText(f"{round(((self.parent.now_close-self.parent.pre_close)*100/self.parent.pre_close),2)}%")
            else:
                if i!=len(self.data)-1:
                    self.parent.time_share_data=f"{self.parent.time_share_data}{'{0:<12}'.format(ok[0])+ok[1]}   {format(ok[2], '>18')[a:18]}{flag}\n"
                    self.parent.price[j]=float(ok[1])
                    self.parent.price_len[j]=len(ok[1])
                    self.parent.flag_direction[j]=int(ok[4])
                    j=j+1
                else:
                    self.parent.time_share_data=f"{self.parent.time_share_data}{'{0:<12}'.format(ok[0])+ok[1]}   {format(ok[2], '>18')[a:18]}{flag}"
                    self.parent.price[j]=float(ok[1])
                    self.parent.price_len[j]=len(ok[1])
                    self.parent.flag_direction[j]=int(ok[4])
                    self.parent.now_close=float(ok[1])
        j=0
        #print(self.parent.time_share_data)
        for i in range(len(self.parent.time_share_data)):
            if self.parent.time_share_data[i]=='S' or self.parent.time_share_data[i]=='B':
                self.parent.flag_pos[j+1]=i+1
            if self.parent.time_share_data[i]=='\n':
                self.parent.line_len[j+1]=i+1
                j=j+1
            #self.parent.text_count=j+1

    def flash_buy_sell_and_capital(self):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        code=self.parent.stock_code

        if globalVariable.marketNum==1 or globalVariable.marketNum==3:
            if code[0:1]=='s' or code[0:3]=='399'  or code[0:2]=='BK' or code[0:2]=='10' or not code[0:2].isdigit():
                return
            num=0
            if code[0] == '6':
                num=1

            url='http://25.push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f116,f84,f85,f162,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f20,f19,f18,f17,f16,f15,f14,f13,f12,f11,f531&secid={}.{}&_=1666089246963'.format(num,code)
            data=requests.get(url=url,headers=headers).json()['data']
            for i in range(0,10,2):
                if data[f'f{i+31}']!='' and data[f'f{i+31}']!='-':
                    if data[f'f{i+31}']>self.parent.pre_close:
                        self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setPalette(globalVariable.pered)
                    elif data[f'f{i+31}']<self.parent.pre_close:
                        self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setPalette(globalVariable.pegreen)
                    else:
                        self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setPalette(globalVariable.peblack)
                    self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setText(str(data['f'+str(i+31)]))
                else:
                    self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setText('')

                if data[f'f{i+11}']!=''  and data[f'f{i+11}']!='-':
                    if data[f'f{i+11}']>self.parent.pre_close:
                        self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setPalette(globalVariable.pered)
                    elif data[f'f{i+11}']<self.parent.pre_close:
                        self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setPalette(globalVariable.pegreen)
                    else:
                        self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setPalette(globalVariable.peblack)
                    self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setText(str(data['f'+str(i+11)]))
                else:
                    self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setText('')
                sc=''
                if data[f'f{i+32}']!='' and data[f'f{i+32}']!='-':
                    sc=str(round(data[f'f{i+32}']))
                self.parent.baseInformation.buy_sell_Var[f'self.sell_num{5-i//2}'].setText(sc)
                sc=''
                if data[f'f{i+12}']!='' and data[f'f{i+12}']!='-':
                    sc=str(round(data[f'f{i+12}']))
                self.parent.baseInformation.buy_sell_Var[f'self.buy_num{5-i//2}'].setText(sc)

            self.parent.baseInformation.base_info['self.Issued_Capital_data'].setText(globalVariable.format_conversion(data['f84']))
            self.parent.baseInformation.base_info['self.Negotiable_Capital_data'].setText(globalVariable.format_conversion(data['f85']))
            self.parent.baseInformation.base_info['self.total_captial_data'].setText(globalVariable.format_conversion(data['f116']))
            self.parent.baseInformation.base_info['self.pe_data'].setText(str(data['f162']))

        else:
            for i in range(0,10,2):
                self.parent.baseInformation.buy_sell_Var[f'self.sell_price{5-i//2}'].setText('')
                self.parent.baseInformation.buy_sell_Var[f'self.sell_num{5-i//2}'].setText('')
                self.parent.baseInformation.buy_sell_Var[f'self.buy_price{5-i//2}'].setText('')
                self.parent.baseInformation.buy_sell_Var[f'self.buy_num{5-i//2}'].setText('')

    def run(self):
            self.get_time_share_tick_data()
            self.deal_with_time_share_tick_data()
            self._signal.emit()
            self.flash_buy_sell_and_capital()
