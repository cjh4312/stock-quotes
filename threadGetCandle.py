# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread

class GetCandle(QThread):
    #  通过类成员对象定义信号对象
    _signal = Signal()

    def __init__(self,parent):
        super(GetCandle, self).__init__()
        self.parent=parent

    def __del__(self):
        self.wait()

    def run(self):
        code=self.parent.stock_code
        if self.parent.ui.us_market.isChecked()==False and self.parent.ui.hk_market.isChecked()==False:
            self.parent.data.login_init(code,self.parent.period,self.parent.adjustflag)
        elif self.parent.ui.us_market.isChecked()==True:
            self.parent.data.get_us_data_from_east(code,self.parent.period,self.parent.adjustflag)
        elif self.parent.ui.hk_market.isChecked()==True:
            if code[0:3]=='sh.' or code[0:3]=='399':
                self.parent.data.login_init(code,self.parent.period,self.parent.adjustflag)
            else:
                self.parent.data.get_hk_data_from_east(code,self.parent.period,self.parent.adjustflag)
        self._signal.emit()
