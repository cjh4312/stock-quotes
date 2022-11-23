# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtCore import QAbstractTableModel,Qt
from PySide6.QtGui import QColor,QFont

class ModelTableStock(QAbstractTableModel):
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
            if role == Qt.DisplayRole:
                grid=self._data.iloc[index.row(), index.column()]
                if isinstance(grid,float):
                    if float(grid)>=100000000:
                        return str(round(float(grid)/100000000,2))+'亿'
                    elif float(grid)>=10000:
                        return str(round(float(grid)/10000,2))+'万'
                return str(grid)
            elif role == Qt.ForegroundRole:
                #涨红 跌绿
                if index.column()==3 and self._data.iloc[index.row(), 3]>0:
                    return QColor(Qt.red)
                elif index.column()==3 and self._data.iloc[index.row(), 3]<0:
                    return QColor(0,191,0)
                #成交额大于1个亿或者于10个亿
                elif  index.column()==5 and self._data.iloc[index.row(), 5]>=1000000000:
                    return QColor(153,0,153)
                elif  index.column()==5 and self._data.iloc[index.row(), 5]>=300000000:
                    return QColor(0,191,255)
                #换手大于15
                elif index.column()==4 and self._data.iloc[index.row(), 4]>=15:
                    return QColor(204,204,0)
                #涨速
                elif  index.column()==6 and self._data.iloc[index.row(), 6]>=2:
                    return QColor(153,0,153)
                elif  index.column()==6 and self._data.iloc[index.row(), 6]>0:
                    return QColor(Qt.red)
                elif index.column()==6 and self._data.iloc[index.row(), 6]<0:
                    return QColor(0,191,0)
#                #市值大于100个亿
#                elif index.column()==8 and self._data.iloc[index.row(), 8]>=10000000000:
#                    return QColor(153,0,153)
#                elif index.column()==9 and self._data.iloc[index.row(), 9]>=10000000000:
#                    return QColor(153,0,153)
#                #5分钟涨跌
#                elif  index.column()==15 and self._data.iloc[index.row(), 15]>0:
#                    return QColor(Qt.red)
#                elif index.column()==15 and self._data.iloc[index.row(), 15]<0:
#                    return QColor(0,191,0)
                #60日涨跌
                elif  index.column()==11 and self._data.iloc[index.row(), 11]>0 and self._data.iloc[index.row(), 11]<100:
                    return QColor(255,155,153)
                elif  index.column()==11 and self._data.iloc[index.row(), 11]>=100:
                    return QColor(153,0,153)
                elif index.column()==11 and self._data.iloc[index.row(), 11]<0:
                    return QColor(0,191,0)
                #今年涨跌
                elif  index.column()==10 and self._data.iloc[index.row(), 10]>0 and self._data.iloc[index.row(), 10]<100:
                    return QColor(255,155,153)
                elif  index.column()==10 and self._data.iloc[index.row(), 10]>=100:
                    return QColor(153,0,153)
                elif index.column()==10 and self._data.iloc[index.row(), 10]<0:
                    return QColor(0,191,0)

                #阳线红，阴线绿
                elif (index.column()==2  or index.column()==15)and self._data.iloc[index.row(), 2]>self._data.iloc[index.row(), 15]:
                    return QColor(255,0,255)
                elif (index.column()==2  or index.column()==15)and self._data.iloc[index.row(), 2]<self._data.iloc[index.row(), 15]:
                    return QColor(0,191,0)
                #最高价、最低价高于昨收红，低于昨收绿
                elif index.column()==13 and self._data.iloc[index.row(), 13]>self._data.iloc[index.row(), 16]:
                    return QColor(Qt.red)
                elif index.column()==13 and self._data.iloc[index.row(), 13]<self._data.iloc[index.row(), 16]:
                    return QColor(0,191,0)
                elif index.column()==14 and self._data.iloc[index.row(), 14]>self._data.iloc[index.row(), 16]:
                    return QColor(Qt.red)
                elif index.column()==14 and self._data.iloc[index.row(), 14]<self._data.iloc[index.row(), 16]:
                    return QColor(0,191,0)

            #elif role == Qt.BackgroundRole:
            #    if index.column() == 1:
            #        return QColor(Qt.red)
            elif role == Qt.FontRole:
                boldFont = QFont()
                if index.column() == 1:
                    boldFont.setFamily('宋体')
                if index.column() == 3 or index.column() == 1 or index.column() == 5:
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

