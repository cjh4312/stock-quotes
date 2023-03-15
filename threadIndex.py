# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread
import globalVariable
import stockInformation

class IndexThread(QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()
    _finishSignal=Signal()

    def __init__(self,parent):
        super(IndexThread, self).__init__()
        self.parent=parent
        self.isTrue=False
        self.num=0

    def __del__(self):
        self.wait()

    def run(self):
        if self.parent.downloadInfoStart:
            stockInformation.download()
            self.parent.downloadInfoStart=False
            self._finishSignal.emit()
        try:
            #刷新市场对应的指数(亚洲和欧美)
            if globalVariable.marketNum==1 or globalVariable.marketNum==5:
                worldIndexData=self.parent.worldIndex.getAllIndex()
                self.parent.baseInformation.flashLabel(0,worldIndexData)
            elif globalVariable.marketNum==2:
                worldIndexData=self.parent.worldIndex.getAllIndex()
                self.parent.baseInformation.flashLabel(8,worldIndexData)

            self.parent.worldFuturesData=self.parent.worldIndex.get_futures_data()
        except Exception as e:
            print('Reason:', e)
        i=0
        if self.isTrue:
            for j in range(len(self.parent.worldFuturesData)):
                if self.parent.worldFuturesData.iat[j,0]=='小型道指当月连续':
                    i=j
        else:
            for j in range(len(self.parent.worldFuturesData)):
                if self.parent.worldFuturesData.iat[j,0]=='A50期指当月连续':
                    i=j
        self.parent.baseInformation.createVar['self.index8'].setText(self.parent.worldFuturesData.iat[i,0][0:len(self.parent.worldFuturesData.iat[i,0])-4])
        if self.parent.worldFuturesData.iat[i,2]=='-' or self.parent.worldFuturesData.iat[i,2]>=0:
            self.parent.baseInformation.createVar['self.indexData8'].setPalette(globalVariable.pered)
        else:
            self.parent.baseInformation.createVar['self.indexData8'].setPalette(globalVariable.pegreen)
        self.parent.baseInformation.createVar['self.indexData8'].setText(f"{self.parent.worldFuturesData.iat[i,1]}  {self.parent.worldFuturesData.iat[i,2]}%")
        self.isTrue=not self.isTrue

        if globalVariable.getValue()==1 and globalVariable.isZhMarketDay():
            self.parent.stock_data=self.parent.tableView.stock_data_copy
            l=0
            if not self.parent.stock_data.empty:
                l=len(self.parent.stock_data)
            for i in range(l):
                if self.parent.stock_code==self.parent.stock_data.iat[i,0]:
                    self.parent.baseInformation.flash_base_information_click(i,self.parent.stock_data,self.parent.name)
                    return

        elif (globalVariable.getValue()==2 and globalVariable.isUSMarketDay()) or\
                (globalVariable.getValue()==5 and globalVariable.isHKMarketDay()):
            self.parent.stock_data=self.parent.tableView.stock_data
            for i in range(len(self.parent.stock_data)):
                if self.parent.stock_code==self.parent.stock_data.iat[i,0]:
                    self.parent.baseInformation.flash_base_information_click(i,self.parent.stock_data,self.parent.name)
                    return
