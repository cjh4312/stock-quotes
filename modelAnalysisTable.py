# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtCore import QAbstractTableModel,Qt
from PySide6.QtGui import QColor,QFont

class AnalysisTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    # 显示数据
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            grid=self._data.iloc[index.row(), index.column()]
            if role == Qt.DisplayRole:
                if isinstance(grid,float):
                    if float(grid)>=100000000:
                        return str(round(float(grid)/100000000,4))+'亿'
                    elif float(grid)>=10000:
                        return str(round(float(grid)/10000,2))+'万'
                    elif float(grid)<=-100000000:
                        return str(round(float(grid)/100000000,4))+'亿'
                    elif float(grid)<=-10000:
                        return str(round(float(grid)/10000,2))+'万'
                    return round(float(grid),2)
                elif isinstance(grid,int):
                    if int(grid)>=100000000:
                        return str(round(int(grid)/100000000,4))+'亿'
                    elif int(grid)>=10000:
                        return str(round(int(grid)/10000,2))+'万'
                    elif int(grid)<=-100000000:
                        return str(round(int(grid)/100000000,4))+'亿'
                    elif int(grid)<=-10000:
                        return str(round(int(grid)/10000,2))+'万'
                elif str(grid).isdigit():
                    if int(grid)>=100000000:
                        return str(round(int(grid)/100000000,4))+'亿'
                    elif int(grid)>=10000  and index.column()!=0:
                        return str(round(int(grid)/10000,2))+'万'
                    elif int(grid)<=-100000000:
                        return str(round(int(grid)/100000000,4))+'亿'
                    elif int(grid)<=-10000:
                        return str(round(int(grid)/10000,2))+'万'
                return str(grid)
            elif role == Qt.ForegroundRole:
                if self._data.iloc[index.row(), 2]=='合计':
                    return QColor(Qt.red)
                elif self._data.iloc[index.row(), 1]=='按行业分':
                    return QColor(255,185,15)
                elif self._data.iloc[index.row(), 1]=='按地区分':
                    return QColor(Qt.blue)
                elif self._data.iloc[index.row(), 1]=='按产品分':
                    return QColor(255,0,255)
                #涨红 跌绿
                elif isinstance(grid,float):
                   if grid<0:
                       return QColor(0,191,0)

            elif role == Qt.FontRole:
                if self._data.iloc[index.row(), 2]=='合计':
                    boldFont = QFont()
                    boldFont.setBold(True)
                    return boldFont
        return None

    # 显示行和列头
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.axes[0][col]
        return None

