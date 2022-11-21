# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtCore import QAbstractTableModel,Qt
from PySide6.QtGui import QColor,QFont

class TimeShare(QAbstractTableModel):
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
                return str(self._data.iloc[index.row(), index.column()])
            elif role == Qt.ForegroundRole:
                if self._data.iloc[index.row(), 2]=='合计':
                    return QColor(Qt.red)

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

